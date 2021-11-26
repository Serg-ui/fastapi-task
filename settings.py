from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv('DATABASE_USER')
DB_HOST = os.getenv('DATABASE_HOST')
DB_PASS = os.getenv('DATABASE_PASSWORD', '')
DB_NAME = os.getenv('DATABASE_NAME')
