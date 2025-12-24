"""Pipeline producer for data ingestion and SQS notification."""
import io
import json
import logging
import pandas as pd
from typing import Any

from services.data_generator import DataGenerator
from config.settings import AWSConfig

logger = logging.getLogger(__name__)


class PipelineProducer:
    """Producer for executing the ETL pipeline (data generation, S3 upload, SQS notification)."""

    def __init__(
        self,
        s3_client: Any,
        sqs_client: Any,
        data_generator: DataGenerator,
        aws_config: AWSConfig
    ):
        """Initialize PipelineProducer with dependencies."""
        self.s3_client = s3_client
        self.sqs_client = sqs_client
        self.data_generator = data_generator
        self.aws_config = aws_config

    def execute_pipeline(self) -> None:
        """Execute the complete pipeline: generate data, upload to S3, and notify via SQS."""
        try:
            # Generate mock data
            df = self.data_generator.generate_mock_dataframe()

            # Convert DataFrame to Parquet format
            logger.info("Converting DataFrame to Parquet format...")
            parquet_buffer = io.BytesIO()
            df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
            parquet_buffer.seek(0)

            # Generate S3 file key
            file_key = f"processamento/vendas_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.parquet"

            # Upload to S3
            logger.info(f"Uploading to s3://{self.aws_config.bucket_name}/{file_key}...")
            self.s3_client.put_object(
                Bucket=self.aws_config.bucket_name,
                Key=file_key,
                Body=parquet_buffer,
                ContentType='application/octet-stream'
            )

            # Get SQS queue URL
            logger.info("Retrieving SQS queue URL...")
            queue_url = self.sqs_client.get_queue_url(QueueName=self.aws_config.queue_name)['QueueUrl']

            # Prepare message payload
            message_payload = {
                "event": "DATA_INGESTION_COMPLETE",
                "bucket": self.aws_config.bucket_name,
                "s3_path": file_key,
                "rows_processed": len(df)
            }

            # Send notification to SQS
            logger.info("Sending notification to queue...")
            self.sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_payload)
            )

            logger.info("Pipeline executed successfully!")

        except Exception as e:
            logger.error(f"Critical error in pipeline: {str(e)}")
            raise

