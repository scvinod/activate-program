import asyncio
import logging
import os

from fastmcp import FastMCP

from program_service import program_store

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("Coca-Cola Program Activation MCP Server")


@mcp.tool(
    name="activate_program",
    description=(
        "Activate a Coca-Cola program for an end user. "
        "Use this when the user provides a program ID to enroll or activate."
    ),
)
def activate_program(program_id: str) -> dict:
    """Activate a Coca-Cola program by its ID.

    Args:
        program_id: The unique program identifier entered by the user.

    Returns:
        A structured result describing whether activation succeeded.
    """
    logger.info("activate_program called for program_id=%s", program_id)
    result = program_store.activate(program_id)
    logger.info(
        "activate_program result for program_id=%s success=%s status=%s",
        result.program_id,
        result.success,
        result.status.value,
    )
    return result.to_dict()


def run_server() -> None:
    port = int(os.getenv("PORT", "8080"))
    transport = os.getenv("MCP_TRANSPORT", "streamable-http")

    if transport == "stdio":
        logger.info("Starting MCP server with stdio transport")
        mcp.run(transport="stdio")
        return

    logger.info("Starting MCP server on 0.0.0.0:%s with %s transport", port, transport)
    asyncio.run(
        mcp.run_async(
            transport=transport,
            host="0.0.0.0",
            port=port,
        )
    )


if __name__ == "__main__":
    run_server()
