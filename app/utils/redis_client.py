import os
from dotenv import load_dotenv
import redis
from redis.connection import SSLConnection

# Load biến môi trường từ .env (nếu chưa load ở chỗ khác)
load_dotenv()

def get_redis_client():
    return redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        username=os.getenv("REDIS_USERNAME"),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True,
    )
