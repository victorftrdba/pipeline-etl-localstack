"""Email notification service for the ETL pipeline."""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import pandas as pd

from config.settings import EmailConfig

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending email notifications via SMTP."""

    def __init__(self, config: EmailConfig):
        """Initialize EmailService with configuration."""
        self.config = config

    def send_processing_error_email(self, error_message: str) -> None:
        """Send email notification for processing errors."""
        subject = f"Processing Error - {pd.Timestamp.now().strftime('%d/%m/%Y')}"
        body = f"""
        <h2>Processing Error</h2>
        <p>{error_message}</p>
        <br>
        <p><i>Automatically sent by your Kubernetes Pipeline.</i></p>
        """
        self._send_email(subject, body)

    def send_empty_queue_email(self) -> None:
        """Send email notification when queue is empty."""
        subject = f"Empty Queue - {pd.Timestamp.now().strftime('%d/%m/%Y')}"
        body = """
        <h2>Empty Queue</h2>
        <p>The queue is empty.</p>
        <br>
        <p><i>Automatically sent by your Kubernetes Pipeline.</i></p>
        """
        self._send_email(subject, body)

    def send_data_quality_report_email(self, stats: Dict[str, float]) -> None:
        """Send data quality report email with statistics."""
        subject = f"Data Quality Report - {pd.Timestamp.now().strftime('%d/%m/%Y')}"
        body = f"""
        <h2>Data Validation Report</h2>
        <p>The pipeline successfully processed a new Parquet file.</p>
        <ul>
            <li><b>Total Rows:</b> {stats['rows']}</li>
            <li><b>Total Value:</b> ${stats['total_val']:.2f}</li>
            <li><b>Average Price:</b> ${stats['avg_val']:.2f}</li>
            <li><b>Schema Status:</b> OK</li>
        </ul>
        <br>
        <p><i>Automatically sent by your Kubernetes Pipeline.</i></p>
        """
        self._send_email(subject, body)

    def _send_email(self, subject: str, body: str) -> None:
        """Internal method to send email via SMTP."""
        msg = MIMEMultipart()
        msg['From'] = self.config.email_from
        msg['To'] = self.config.email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                server.send_message(msg)
            logger.info("Email sent successfully to Mailpit!")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

