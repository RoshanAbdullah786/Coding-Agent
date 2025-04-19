import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init

path = "Agents/logg"
# Initialize colorama
init(autoreset=True)

# Create log folder if not exists
os.makedirs('Agents/logg', exist_ok=True)

logger = logging.getLogger('Agents Logger')
logger.setLevel(logging.DEBUG)

# Formatter without colors (for file)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Colored Formatter for console
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Style.DIM,
        'INFO': Fore.GREEN,
        'WARNING': Fore.BLUE,      # <<< WARNING = BLUE
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }
    
    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        message = super().format(record)
        return color + message + Style.RESET_ALL

# File Handler (save everything in UTF-8)
file_handler = RotatingFileHandler(f'{path}/saved_logs/agent.log', maxBytes=5*1024*1024, backupCount=7, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

# Safe Console Handler
class SafeConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding) + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

# Console Handler
console_handler = SafeConsoleHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)
