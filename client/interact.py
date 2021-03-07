#!/user/bin/python
# -*-coding:UTF-8-*-
"""
@Author:    Night Cruising
@File:      interact.py
@Time:      2021/3/7 0007
@Version:   3.7.3
@Desc:      None
"""
import random
from threading import Thread

from rpc_client import RpcClient


class Client(object):
    def __init__(self):
        self.rpc_client = RpcClient()
        self.tasks: dict = {}

    def run(self):
        while True:
            command = input("input command: ")
            if not command:
                continue
            if command == 'exit':
                break

            command_prefix = command.split()[0]
            if hasattr(self, command_prefix):
                func = getattr(self, command_prefix)
                t = Thread(target=func, args=(command,))
                t.start()
                t.join()
            else:
                print('command error.')

    def execute(self, command: str):
        try:
            command_ls = command.split()
            command_name = command_ls[1]
            hosts = command_ls[2:]
        except:
            print('command error.')
            return

        for host in hosts:
            corr_id, callback_queue = self.rpc_client.send_request(command=command_name, host=host)
            task_id = str(random.randint(1, 1000))
            self.tasks[task_id] = {'corr_id': corr_id, 'queue': callback_queue, 'host': host}
            print('task_id: ', task_id)

    def get(self, command: str):
        try:
            command_ls = command.split()
            task_id = command_ls[1]
        except:
            print("command error.")
            return

        if task_id in self.tasks:
            corr_id = self.tasks[task_id]['corr_id']
            host = self.tasks[task_id]['host']
            callback_queue = self.tasks[task_id]['queue']
            command_result = self.rpc_client.get_response(corr_id=corr_id, callback_queue=callback_queue)
            print(f'task_id: {task_id}, host: {host},command_result:\n{command_result}')
            del self.tasks[task_id]
        else:
            print('No this task.')

    def all_task(self, command: str):
        for task_id in self.tasks:
            print('task_id: ', task_id, end=' ')
        print('\n')