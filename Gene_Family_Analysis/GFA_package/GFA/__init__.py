_author_ = """"""
_email_ = ''
_version_ = '0.1.0'
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

HOME = Path.home()


# Logging Configuration
logging.basicConfig(filename='progress.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


