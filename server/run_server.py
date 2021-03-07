#!/user/bin/python
# -*-coding:UTF-8-*-
"""
@Author:    Night Cruising
@File:      run_server.py
@Time:      2021/3/7 0007
@Version:   3.7.3
@Desc:      None
"""
from rpc_server import RpcServer

if __name__ == '__main__':
    rpc_server = RpcServer()
    rpc_server.channel.start_consuming()