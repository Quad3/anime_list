import os
import secrets

from dotenv import load_dotenv

load_dotenv()

TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASS = os.environ.get("TEST_DB_PASS")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

DOMAIN: str = "localhost:5000"
API_V1_STR: str = "/api/v1"

SECRET_KEY: str = secrets.token_urlsafe(32)
# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
