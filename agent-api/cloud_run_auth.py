from __future__ import annotations

from collections.abc import Callable

import httpx
import google.auth.transport.requests
import google.oauth2.id_token


def fetch_identity_token(audience: str) -> str:
    normalized_audience = audience.rstrip("/")
    try:
        metadata_response = httpx.get(
            "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity",
            params={"audience": normalized_audience},
            headers={"Metadata-Flavor": "Google"},
            timeout=10.0,
        )
        metadata_response.raise_for_status()
        return metadata_response.text
    except httpx.HTTPError:
        auth_request = google.auth.transport.requests.Request()
        return google.oauth2.id_token.fetch_id_token(auth_request, normalized_audience)


class CloudRunAuthTransport(httpx.AsyncHTTPTransport):
    """Inject a Cloud Run identity token into every MCP HTTP request."""

    def __init__(self, audience: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.audience = audience.rstrip("/")

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        token = fetch_identity_token(self.audience)
        request.headers["Authorization"] = f"Bearer {token}"
        return await super().handle_async_request(request)


def create_cloud_run_mcp_http_client_factory(audience: str) -> Callable:
    def create_cloud_run_mcp_http_client(*, headers=None, timeout=None, auth=None, **kwargs):
        del auth
        transport = CloudRunAuthTransport(audience=audience)
        return httpx.AsyncClient(headers=headers, timeout=timeout, transport=transport, **kwargs)

    return create_cloud_run_mcp_http_client
