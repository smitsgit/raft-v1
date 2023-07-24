from multiprocessing import Pool, Condition, Process
from threading import Thread
from resettabletimer import ResettableTimer
import random

import json
from time import sleep

import logging, logging.handlers
import utils

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',
                                               utils.LOGGER_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)


def rpc_worker(server_id, timer, logger):
    pass


def timer_expired(server_id, logger):
    logger.debug(f'{server_id}: Timer expired')
    logger.info(f'{server_id}: Start the election')


def get_random_election_timeout():
    # It should be between 150ms to 300ms
    return random.randint(5, 10)


def raft_replica_worker(server_id, condition):
    logger = logging.getLogger(server_id)
    logger.debug(f'waiting')
    with condition:
        print(f"Waiting to be woken up ")
        condition.wait()

    election_timeout = get_random_election_timeout()
    logger.debug(f'Election Timeout is {election_timeout}')
    timer = ResettableTimer(election_timeout, timer_expired, args=(server_id, logger))
    Thread(target=rpc_worker, args=(server_id, timer, logger), daemon=True, name=f'rpc-thread-{server_id}').start()
    timer.start()
    sleep(15)


def main():
    condition = Condition()
    processes = []
    with open("config.json") as fp:
        config = json.loads(fp.read())
        for key, value in config["servers"].items():
            processes.append(Process(target=raft_replica_worker, args=(config["servers"][key]["name"], condition)))

    sleep(2)
    for process in processes:
        process.start()

    sleep(5)
    with condition:
        condition.notify_all()

    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
