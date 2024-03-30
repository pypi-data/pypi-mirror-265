import asyncio


async def abc():
    await asyncio.sleep(1)
    print(asyncio.current_task())


async def main():
    await abc()
    return


asyncio.run(main())
