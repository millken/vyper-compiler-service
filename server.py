from concurrent import futures
import logging
import os,sys
from proto import vyper_pb2,vyper_pb2_grpc
import grpc
from grpc_reflection.v1alpha import reflection


_HOST = '0.0.0.0'
_PORT = '5994'

class VyperCompilerServicer(vyper_pb2_grpc.VyperServicer):
    def compiler(self, request, context):
        logging.debug('request: %s', request)
        source = request.source
        if source.name == '' or source.content == '':
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("InvalidSource")

        cache_modules = dict([
        (key, value) for key, value in sys.modules.items()
        if key.startswith('vyper')])

        for key in cache_modules:
            del sys.modules[key]
        
        version = request.version
        baseDir = os.path.dirname(os.path.abspath(__file__))
        vyperDir = os.path.join(baseDir, 'vyper', version)
        if version == '' or not os.path.exists(vyperDir):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("InvalidVersion '" + version + "'")

        sys.path.insert(0, vyperDir)
        import vyper
        from vyper.compiler import compile_code
        from vyper.exceptions import VyperException
        sys.path.pop(0)

        try:
            compileRes = compile_code(source.content, ['abi', 'bytecode', 'bytecode_runtime', 'ir', 'method_identifiers'])
            compileRes['ir'] = str(compileRes['ir'])
        except VyperException as e:
            return vyper_pb2.VyperResponse(content=str(e))
        
        vr = vyper_pb2.VyperResponse(compileOK=True)
        verify_code = request.verifyBytecode
        if verify_code != '':
            if not verify_code.startswith('0x'):
                verify_code = '0x' + verify_code
            if compileRes['bytecode_runtime'] == verify_code:
                vr.verifyOK = True
        vr.content = str(compileRes)
        return vr


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vyper_pb2_grpc.add_VyperServicer_to_server(
        VyperCompilerServicer(), server)
    reflection.enable_server_reflection([h.service_name() for h in server._state.generic_handlers], server)
    server.add_insecure_port(_HOST + ':' + _PORT)
    server.start()
    logging.info('Vyper Compiler Server start listen on ' + _HOST + ':' + _PORT)
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(filename)s %(levelname)s %(message)s",
    datefmt='%a %d %b %Y %H:%M:%S')
    serve()