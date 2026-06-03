import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from agent_project_memory.app import create_app, main


app = create_app()


if __name__ == "__main__":
    main()
