"""Configuration management for the ETL pipeline."""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class AWSConfig:
    """AWS configuration settings."""
    endpoint_url: str
    bucket_name: str
    queue_name: str
    region: str
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "AWSConfig":
        """Create AWSConfig from environment variables."""
        return cls(
            endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"),
            bucket_name=os.getenv("S3_BUCKET_NAME", "projeto-cloud-brasil-bucket"),
            queue_name=os.getenv("SQS_QUEUE_NAME", "projeto-cloud-brasil-queue"),
            region=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        )


@dataclass
class EmailConfig:
    """Email configuration settings."""
    smtp_server: str
    smtp_port: int
    email_from: str
    email_to: str

    @classmethod
    def from_env(cls) -> "EmailConfig":
        """Create EmailConfig from environment variables."""
        return cls(
            smtp_server=os.getenv("SMTP_SERVER", "localhost"),
            smtp_port=int(os.getenv("SMTP_PORT", "1025")),
            email_from=os.getenv("EMAIL_FROM", "analista@cloudbrasil.com.br"),
            email_to=os.getenv("EMAIL_TO", "seu-email@exemplo.com"),
        )


@dataclass
class AppConfig:
    """Application configuration."""
    aws: AWSConfig
    email: EmailConfig

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create AppConfig from environment variables."""
        return cls(
            aws=AWSConfig.from_env(),
            email=EmailConfig.from_env(),
        )

