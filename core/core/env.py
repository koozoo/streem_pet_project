from dotenv import load_dotenv
import os


load_dotenv()

secret_key = os.getenv('SECRET_KEY')
redis_config = {
    'REDIS_HOST': os.environ.get('REDIS_HOST'),
    'REDIS_PORT': os.environ.get('REDIS_PORT')
}
