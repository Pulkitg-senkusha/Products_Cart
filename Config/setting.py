import os
from dataclasses import dataclass
from dotenv import load_dotenv
from logger import logger  # ✅ Add logger

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """Application configuration using dataclass"""
    amazon_api_host: str
    database_url: str
    api_port: int
    api_key: str
    api_host: str
    product_base_url: str = "https://real-time-amazon-data.p.rapidapi.com/"

    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables"""
        config = cls(
            amazon_api_host=os.getenv('RAPIDAPI_HOST', ''),
            database_url=os.getenv('DATABASE_URL', ''),
            api_port=int(os.getenv('API_PORT', 8000)),
            api_key=os.getenv('RAPIDAPI_KEY', ''),
            api_host=os.getenv('API_HOST', '0.0.0.0'),
        )
        
        logger.info("Configuration loaded from environment variables")

        if not config.api_key or not config.database_url:
            logger.error("Missing critical config values: API_KEY or DATABASE_URL")
            raise ValueError("Missing critical environment variables: API_KEY or DATABASE_URL")

        return config

config = Config.from_env()
