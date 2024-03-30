import ast
from pathlib import Path

from repo_ast_builder.node_walking import walk_node_to_create_hints


def walk_repository(directory: Path) -> dict:
    repository_info = {}

    for file_path in directory.rglob("*.py"):
        relative_path = file_path.relative_to(directory)
        if ".venv" in str(relative_path):
            continue

        try:
            with file_path.open("r") as f:
                tree = ast.parse(f.read())

            repository_info[str(relative_path)] = walk_node_to_create_hints(tree, tree,str(file_path), str(directory))
        except SyntaxError as e:
            print(f"Skipping file {file_path} due to syntax error: {str(e)}")
            continue
        except UnicodeDecodeError as e:
            print(f"Error decoding file {file_path}: {str(e)}")
            continue

    return repository_info
