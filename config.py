from pathlib import Path


BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"

CSV_FILE = DATA_DIR / "employees.csv"


MODEL_NAME = "qwen3:8b"

TEMPERATURE = 0