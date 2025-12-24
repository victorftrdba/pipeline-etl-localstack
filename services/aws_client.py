"""AWS client factory for the ETL pipeline."""
import boto3
from typing import Tuple, Any

from config.settings import AWSConfig


class AWSClientFactory:
    """Factory for creating AWS service clients."""

    def __init__(self, config: AWSConfig):
        """Initialize AWSClientFactory with configuration."""
        self.config = config

    def create_s3_client(self) -> Any:
        """Create and return an S3 client."""
        client_kwargs = {
            'endpoint_url': self.config.endpoint_url,
            'region_name': self.config.region,
        }
        
        if self.config.access_key_id and self.config.secret_access_key:
            client_kwargs['aws_access_key_id'] = self.config.access_key_id
            client_kwargs['aws_secret_access_key'] = self.config.secret_access_key

        return boto3.client('s3', **client_kwargs)

    def create_sqs_client(self) -> Any:
        """Create and return an SQS client."""
        client_kwargs = {
            'endpoint_url': self.config.endpoint_url,
            'region_name': self.config.region,
        }
        
        if self.config.access_key_id and self.config.secret_access_key:
            client_kwargs['aws_access_key_id'] = self.config.access_key_id
            client_kwargs['aws_secret_access_key'] = self.config.secret_access_key

        return boto3.client('sqs', **client_kwargs)

    def create_clients(self) -> Tuple[Any, Any]:
        """Create and return both S3 and SQS clients."""
        return self.create_s3_client(), self.create_sqs_client()

