import asyncio

from agent import agent_service


async def main() -> None:
    await agent_service.startup()
    response = await agent_service.chat("Please activate program COKE-WELCOME-PROGRAM")
    print(response)
    await agent_service.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
