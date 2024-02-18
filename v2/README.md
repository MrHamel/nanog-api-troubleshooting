# V2

## Goals

Strike a balance between organization and high performance while securely interacting with many network devices concurrently.

## How does this project work?

The `lib` folder contain utility classes with static methods that a main script will include as part of a boilerplate (see `example.py`), when a script needs to interact with a device, the `Device` class will auto detect the vendor and return the appropriate class. Vendor class functions will return Pydantic models (located in `models/data`), which can be passed into output functions (located in `models/outputs`).

The implementation of the `Credentials` and `Log` are very customizable.

## Dependencies

- [aioeapi](https://github.com/jeremyschulman/aio-eapi) - Arista vendor library
- [aiosnmp](https://github.com/hh-h/aiosnmp) - Async SNMP querying
- [asyncio](https://docs.python.org/3/library/asyncio.html) - Asynchronous functionality
- [netaddr](https://netaddr.readthedocs.io/en/latest/) - Manipulate IP CIDRs
- [numpy](https://numpy.org) - Intense math calculations
- [pydantic](https://docs.pydantic.dev/latest/) - Data modelling
- [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation) - Config file data structure parsing
- [rich](https://rich.readthedocs.io/en/stable/index.html) - Terminal data formatting
- [termcolor](https://github.com/termcolor/termcolor) - Terminal coloring
- [uvloop](https://github.com/MagicStack/uvloop) - libuv event loop

## Authors

- Cat Gurinsky
- Ryan Hamel