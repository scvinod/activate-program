from __future__ import annotations

import logging
from typing import Any

import httpx
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

from cloud_run_auth import create_cloud_run_mcp_http_client_factory
from config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a friendly Coca-Cola program activation assistant.

Your job is to help end users activate Coca-Cola programs by program ID.

Guidelines:
- Greet users warmly and explain that you can activate Coca-Cola programs.
- When a user provides a program ID, call the activate_program tool with that ID.
- Program IDs are usually uppercase strings such as COKE-SUMMER-2026 or COKE-WELCOME-PROGRAM.
- If activation fails, explain the reason clearly and suggest next steps.
- If activation succeeds, confirm and thank the user.
- Do not invent program IDs or activation results; always use the tool.
- Do not undertake any actions outside of activating programs by ID.
- Keep responses concise and conversational.
"""


class ProgramAgentService:
    def __init__(self) -> None:
        self._client: MultiServerMCPClient | None = None
        self._agent: Any | None = None

    async def startup(self) -> None:
        logger.info("Connecting to MCP server at %s", settings.mcp_endpoint)
        mcp_config: dict = {
            "transport": "http",
            "url": settings.mcp_endpoint,
        }
        if settings.mcp_use_cloud_run_auth:
            mcp_config["httpx_client_factory"] = create_cloud_run_mcp_http_client_factory(
                settings.mcp_server_url
            )
            logger.info("Using Cloud Run identity token auth for MCP requests")

        self._client = MultiServerMCPClient(
            {
                settings.mcp_server_name: mcp_config,
            }
        )
        tools = await self._client.get_tools()
        logger.info("Loaded %s MCP tool(s): %s", len(tools), [tool.name for tool in tools])

        llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            http_client=httpx.Client(verify=settings.openai_http_verify),
            http_async_client=httpx.AsyncClient(verify=settings.openai_http_verify),
        )
        if not settings.openai_ssl_verify:
            logger.warning("OpenAI SSL verification is disabled for local development.")
        self._agent = create_agent(
            llm,
            tools,
            system_prompt=SYSTEM_PROMPT,
        )

    async def shutdown(self) -> None:
        self._client = None
        self._agent = None

    async def chat(self, message: str) -> str:
        if self._agent is None:
            raise RuntimeError("Agent is not initialized.")

        result = await self._agent.ainvoke(
            {"messages": [HumanMessage(content=message)]},
        )

        messages = result.get("messages", [])
        for message_obj in reversed(messages):
            if isinstance(message_obj, AIMessage) and message_obj.content:
                return _content_to_text(message_obj.content)

        return "I could not generate a response. Please try again."


def _content_to_text(content: str | list[str | dict]) -> str:
    if isinstance(content, str):
        return content

    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict) and item.get("type") == "text":
            parts.append(str(item.get("text", "")))

    return "\n".join(part for part in parts if part).strip()


agent_service = ProgramAgentService()
