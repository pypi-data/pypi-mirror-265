from pathlib import Path

from repo_ast_builder.file_walking import walk_repository
import json


def read_ast(path: str) -> str:
    return json.dumps(walk_repository(Path(path)))
