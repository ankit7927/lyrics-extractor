import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
format_handler = logging.Formatter(
    "{asctime} - {levelname} - {message}",
     style="{",
     datefmt="%Y-%m-%d %H:%M",
)

logger.addHandler(format_handler)
logger.addHandler(file_handler)
