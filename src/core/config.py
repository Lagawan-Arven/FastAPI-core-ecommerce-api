import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Use ENVIRONMENT for clarity 
ENV = os.getenv("ENVIRONMENT", "local")

env_file_map = {
    "local": ".env.local",
    "docker": ".env.docker",
}

env_file = env_file_map.get(ENV)

# Load .env ONLY for local/docker
if env_file:
    env_path = BASE_DIR / env_file
    if env_path.exists():
        load_dotenv(env_path)

