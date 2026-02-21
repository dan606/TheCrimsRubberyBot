from config import *

import logging
import sys

logging.basicConfig(
    level=logging.getLevelName(Log_Level),
    format=Log_Format,
    handlers=[
        logging.FileHandler("log.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger()
