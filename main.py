import sys

from src.application import Application

from src.shared.logger import load_logger_config

if __name__ == "__main__":
    load_logger_config()
    
    app = Application()
    sys.exit(app.exec())