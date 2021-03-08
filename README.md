# rpc_app
*An asynchronous RPC(remote procedure call) implemented using RabbitMq.*

## notice

In order to use this program, you need to install [RabbitMQ](https://www.rabbitmq.com/) first.

## Installation

clone:

```text
git clone https://github.com/night-cruise/rpc_app.git
cd rpc_app
```

Use the pipenv create & activate virtual env and then install dependency:

```text
pipenv install
pipenv shell
```

run server:

```text
cd server
python run_server.py
```

run client:

```text
cd client
python run_client.py
```

## settings

In `client\setttings.py` and `server\settings.py`, configure RabbitMQ's host and port, username and password, and server host.

## command

- `execute comand host1 host2`: execute command.(There can be as many host as you want, separated by spaces.)
- `get task_id`: get the command execution result according to the task id.
- `all_task`: get all task id


## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).