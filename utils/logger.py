import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("jira_summarizer")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

console = logging.StreamHandler()
console.setFormatter(formatter)

file = logging.FileHandler(
    LOG_DIR / "application.log",
    encoding="utf-8"
)

file.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file)