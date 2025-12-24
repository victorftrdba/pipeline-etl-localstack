"""Main entry point for the ETL pipeline."""
import logging

from config.settings import AppConfig
from services.aws_client import AWSClientFactory
from services.email_service import EmailService
from services.data_generator import DataGenerator
from pipeline.consumer import PipelineConsumer
from pipeline.producer import PipelineProducer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the pipeline consumer."""
    try:
        # Load configuration from environment variables
        config = AppConfig.from_env()

        # Initialize AWS client factory
        aws_factory = AWSClientFactory(config.aws)
        s3_client, sqs_client = aws_factory.create_clients()

        # Initialize services
        email_service = EmailService(config.email)
        data_generator = DataGenerator()

        # Initialize pipeline consumer
        consumer = PipelineConsumer(
            sqs_client=sqs_client,
            s3_client=s3_client,
            email_service=email_service,
            aws_config=config.aws
        )

        # Execute consumer pipeline
        consumer.consume_and_validate_messages()

    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}")
        # Try to send error email if possible
        try:
            config = AppConfig.from_env()
            email_service = EmailService(config.email)
            email_service.send_processing_error_email(f"Error: {e}")
        except Exception as email_error:
            logger.error(f"Failed to send error email: {email_error}")
        raise


if __name__ == "__main__":
    main()
