#!/bin/bash

for Line in $(cat compiler.list)
do 
    if [ ! -d "./vyper/$Line" ]; then
	    pip3 install vyper==$Line -t ./vyper/$Line -i https://pypi.tuna.tsinghua.edu.cn/simple
    fi
done
