#!/usr/bin/env python3

import asyncio
from logging import Logger
import uvloop

from lib.arg_parser import Arg_Parser
from lib.config import Config
from lib.credentials import Credentials
from lib.device import Device
from lib.log import Log

async def task_thread(switch, cfg: dict, log: Logger):
    switch = await Device.get(switch, Credentials.get())
    
    print(await switch.dev.cli("show version"))

    pass

async def main(switches):
    cfg: dict = Config.get()
    log: Logger = Log.get()

    tasks: list = []

    for switch in switches:
        tasks.append(task_thread(switch, cfg, log))

    for task in asyncio.as_completed(tasks):
        await task

if __name__ == "__main__":
    switches, script_function, output_dir = Arg_Parser.parse_args()

    Credentials.set()
    Log.start(script_function, output_dir)
    uvloop.install()
    asyncio.run(main(switches))
