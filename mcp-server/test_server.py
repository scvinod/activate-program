import asyncio

from fastmcp import Client


async def test_server() -> None:
    mcp_url = "http://localhost:8080/mcp"
    async with Client(mcp_url) as client:
        tools = await client.list_tools()
        for tool in tools:
            print(f"Tool found: {tool.name}")

        result = await client.call_tool(
            "activate_program",
            {"program_id": "COKE-SUMMER-2026"},
        )
        print(f"Activation result: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(test_server())
