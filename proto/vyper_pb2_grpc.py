# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import vyper_pb2 as proto_dot_vyper__pb2


class VyperStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.compiler = channel.unary_unary(
                '/iotex.Vyper/compiler',
                request_serializer=proto_dot_vyper__pb2.VyperRequest.SerializeToString,
                response_deserializer=proto_dot_vyper__pb2.VyperResponse.FromString,
                )


class VyperServicer(object):
    """Missing associated documentation comment in .proto file."""

    def compiler(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VyperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'compiler': grpc.unary_unary_rpc_method_handler(
                    servicer.compiler,
                    request_deserializer=proto_dot_vyper__pb2.VyperRequest.FromString,
                    response_serializer=proto_dot_vyper__pb2.VyperResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'iotex.Vyper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Vyper(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def compiler(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iotex.Vyper/compiler',
            proto_dot_vyper__pb2.VyperRequest.SerializeToString,
            proto_dot_vyper__pb2.VyperResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
