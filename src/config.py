import urllib.parse
from typing import List, Union
from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8006
    DATABASE_URL: str = Field(
        default="",
        validation_alias=AliasChoices("DATABASE_URL", "SQL_DB", "database_url", "sql_db"),
        description="PostgreSQL Neon database connection URL",
    )
    CATALOG_SERVICE_URL: str = "http://localhost:8001/api/v1"
    CORS_ORIGINS: Union[List[str], str] = ["*"]

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        if not v:
            return v

        # Automatically rewrite standard PostgreSQL schemes for SQLAlchemy asyncpg
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://") and not v.startswith("postgresql+asyncpg://"):
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Parse query parameters to ensure asyncpg compatibility
        parsed = urllib.parse.urlsplit(v)
        if parsed.query:
            qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
            # 1. asyncpg expects 'ssl' parameter instead of 'sslmode'
            if "sslmode" in qs:
                ssl_vals = qs.pop("sslmode")
                if "ssl" not in qs:
                    qs["ssl"] = ssl_vals
            # 2. Strip libpq-specific parameters unsupported by asyncpg
            for unsupported in ["channel_binding", "gssencmode"]:
                qs.pop(unsupported, None)
            new_query = urllib.parse.urlencode(qs, doseq=True)
            v = urllib.parse.urlunsplit(parsed._replace(query=new_query))

        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            import json
            try:
                return json.loads(v)
            except Exception:
                return ["*"]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


settings = Settings()
