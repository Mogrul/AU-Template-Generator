from pathlib import Path

from src.backend.logger import load_logger_config
from src.backend.template import Template

if __name__ == "__main__":
    load_logger_config()
    template = Template(Path("data/templates/config.hpp"))
    template.build()
    