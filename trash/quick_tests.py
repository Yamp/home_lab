import uuid
import time
import threading
import random
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Message:
    dst_user_id: int = None
    text: str = ""


class MockConn:
    def __init__(self, *args, **kwargs):
        self.id = uuid.uuid4().hex
        self.path = '/'
        self.user_id = random.randint(0, 3)

    def send(self, message):
        print(f'sending message: {message}')

    def receive(self):
        return f'mock message {uuid.uuid4().hex} from conn {self.id.hex}'

    def __iter__(self):
        return [].__iter__()


globalSubs = dict()
user_connections = defaultdict(set)


def send_msg_to_connection(id_, msg: Message):
    """ Sends message to connection id_ """
    try:
        globalSubs[id_].send(msg)
    except Exception as e:
        print(e)


def add_sub(conn, user_id):
    global globalSubs
    # synchronized
    # (
    user_connections[user_id] |= {conn.id}
    globalSubs[conn.id] = conn
    # )


def remove_sub(conn, user_id):
    global globalSubs

    # synchronized
    # (
    del globalSubs[conn.id]
    user_connections[user_id].remove(conn.id)
    if len(user_connections[user_id]) == 0:
        del user_connections[user_id]
    # )


def global_broadcast(message):
    global globalSubs
    for id_, conn in globalSubs.items():
        send_msg_to_connection(id_, message)


def send_msg(msg: Message):
    if msg.dst_user_id is None:
        global_broadcast(msg)
    else:
        for cid in user_connections[msg.dst_user_id]:
            send_msg_to_connection(cid, msg)


def mock_websocket_handler(conn: 'MockConn'):
    user_id = random.randint(0, 3)
    add_sub(conn, user_id)

    try:
        for message in conn:
            print(f'received message: {message}')
        time.sleep(0.5)
    except Exception as e:
        print(e)
    finally:
        remove_sub(conn, user_id)


def main():
    threads = [
        threading.Thread(target=mock_websocket_handler, args=[MockConn()]),
        threading.Thread(target=mock_websocket_handler, args=[MockConn()]),
        threading.Thread(target=mock_websocket_handler, args=[MockConn()]),
    ]

    for thread in threads:
        thread.start()

    try:
        send_msg(Message(2, 'test_msg'))
    except Exception as e:
        print(e)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
