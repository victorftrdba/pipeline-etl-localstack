"""Pipeline consumer for message processing and data validation."""
import io
import json
import logging
import pandas as pd
from typing import Dict, Any

from services.email_service import EmailService
from config.settings import AWSConfig

logger = logging.getLogger(__name__)


class PipelineConsumer:
    """Consumer for processing SQS messages and validating data."""

    def __init__(
        self,
        sqs_client: Any,
        s3_client: Any,
        email_service: EmailService,
        aws_config: AWSConfig
    ):
        """Initialize PipelineConsumer with dependencies."""
        self.sqs_client = sqs_client
        self.s3_client = s3_client
        self.email_service = email_service
        self.aws_config = aws_config

    def consume_and_validate_messages(self) -> None:
        """Consume messages from SQS queue and validate data."""
        try:
            queue_url = self.sqs_client.get_queue_url(QueueName=self.aws_config.queue_name)['QueueUrl']
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1
            )

            if 'Messages' in response:
                message = response['Messages'][0]
                body = json.loads(message['Body'])
                s3_key = body['s3_path'].replace(f"s3://{self.aws_config.bucket_name}/", "")

                # Read Parquet file from S3
                df = self._read_parquet_from_s3(s3_key)

                # Calculate statistics
                stats = self._calculate_statistics(df)

                # Send data quality report email
                self.email_service.send_data_quality_report_email(stats)

                # Delete message from queue
                self.sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
            else:
                logger.info("Queue is empty.")
                self.email_service.send_empty_queue_email()

        except Exception as e:
            error_message = f"Error: {e}"
            self.email_service.send_processing_error_email(error_message)
            raise

    def _read_parquet_from_s3(self, s3_key: str) -> pd.DataFrame:
        """Read Parquet file from S3."""
        obj = self.s3_client.get_object(Bucket=self.aws_config.bucket_name, Key=s3_key)
        return pd.read_parquet(io.BytesIO(obj['Body'].read()))

    def _calculate_statistics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate statistics from DataFrame."""
        return {
            'rows': len(df),
            'total_val': float(df['valor_usd'].sum()),
            'avg_val': float(df['valor_usd'].mean())
        }

