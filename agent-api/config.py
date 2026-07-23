from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_ssl_verify: bool = True
    openai_ca_bundle: str | None = None
    mcp_server_url: str = "http://localhost:8080"
    mcp_server_name: str = "program"
    mcp_use_cloud_run_auth: bool = False
    port: int = 8080
    log_level: str = "INFO"

    @property
    def mcp_endpoint(self) -> str:
        return f"{self.mcp_server_url.rstrip('/')}/mcp"

    @property
    def openai_http_verify(self) -> bool | str:
        if self.openai_ca_bundle:
            return self.openai_ca_bundle
        return self.openai_ssl_verify


settings = Settings()
