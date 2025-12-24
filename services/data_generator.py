"""Data generation service for the ETL pipeline."""
import logging
import pandas as pd
from typing import Dict, List

logger = logging.getLogger(__name__)


class DataGenerator:
    """Service for generating mock data for the pipeline."""

    def generate_mock_dataframe(self) -> pd.DataFrame:
        """Generate a mock DataFrame with sample transaction data."""
        logger.info("Generating example DataFrame...")
        data: Dict[str, List] = {
            'id_transacao': [101, 102, 103],
            'produto': ['Cloud Service', 'Terraform Training', 'SRE Consulting'],
            'valor_usd': [1500.0, 299.0, 5000.0],
            'data_processamento': [pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')] * 3
        }
        return pd.DataFrame(data)

