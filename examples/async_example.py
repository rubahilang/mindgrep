import asyncio

async def say_after(delay, msg):
    await asyncio.sleep(delay)
    print(msg)

async def main():
    task = asyncio.create_task(say_after(1, "Hello after 1s"))
    await task

if __name__ == "__main__":
    asyncio.run(main())
