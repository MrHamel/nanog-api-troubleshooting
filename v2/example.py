#!/usr/bin/env python3

import asyncio
from logging import Logger
from pprint import pprint
import uvloop

'''
Everything is broken down into many libraries and static methods for
organizational purposes.
'''

from lib.arg_parser import Arg_Parser
from lib.config import Config
from lib.credentials import Credentials
from lib.device import Device
from lib.log import Log

'''
Semaphores are very important for limiting how many devices a script will
'touch' at any given time.
'''
device_task_limit = asyncio.Semaphore(64)

async def task_thread(device_task_limit: asyncio.Semaphore, switch,
                        cfg: dict, log: Logger):
    '''
    Providing the semaphore will allow this method/task to run, this is
    where the script logic will live (connecting to a device, retrieve
    facts, execute necessary code, output the result, and optionally
    log the result)
    '''
    async with device_task_limit:
        switch = await Device.get(switch, Credentials.get())
        facts  = await switch.get_facts()
        
        pprint(facts.__dict__)
        pprint(facts.__repr__)

async def main(sem: asyncio.Semaphore, switches: list):
    '''
    This is the asyncio loop starting point, which turns the list of
    devices into independent asyncio tasks.
    '''
    cfg: dict = Config.get()
    log: Logger = Log.get()

    tasks: list = []

    '''
    Appending async functions will not run them, but return a coroutine for
    asyncio to process in the next for loop.
    '''
    for switch in switches:
        tasks.append(task_thread(sem, switch, cfg, log))

    '''
    asyncio.as_completed will run all the tasks in the specified list, when
    a task is awaited, it will return that tasks result. At the moment it
    does not expect anything to return, but can be very easily changed.
    '''
    for task in asyncio.as_completed(tasks):
        await task

if __name__ == "__main__":
    '''
    This is where the magic starts, when a script is started it will do all
    things the original boilerplate scripts did, but abstracted it all way
    into classes in lib/ using static non-async methods, except for uvloop.

    uvloop Summary from https://uvloop.readthedocs.io :

    uvloop is a fast, drop-in replacement of the built-in asyncio event
    loop. uvloop is released under the MIT license.

    uvloop makes asyncio fast. In fact, it is at least 2x faster than
    nodejs, gevent, as well as any other Python asynchronous framework.
    The performance of uvloop-based asyncio is close to that of Go
    programs.
    '''

    switches, script_function, output_dir = Arg_Parser.parse_args()

    Credentials.set()
    Log.start(script_function, output_dir)
    uvloop.run(main(device_task_limit, switches))
    Log.end()
