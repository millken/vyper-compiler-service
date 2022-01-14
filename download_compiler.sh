#!/bin/bash

for Line in $(cat compiler.list)
do 
    if [ ! -d "./vyper/$Line" ]; then
	    pip3 install vyper==$Line -t ./vyper/$Line
    fi
done
