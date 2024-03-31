import ast

from repo_ast_builder.general_node_walking import walk_node
from repo_ast_builder.name_resolver import resolve_name
from repo_ast_builder.options import INCLUDE_ANY_TYPE

function_dict = {}


def get_function_dict(filepath: str, root: ast.AST):
    if filepath in function_dict:
        return function_dict[filepath]

    call_walker = FunctionCallWalker(filepath)
    walk_node(root, root, call_walker.walk)
    function_dict[filepath] = call_walker.dict
    return call_walker.dict


def walk_node_to_create_hints(start_node: ast.AST, root: ast.AST, file_path: str, directory: str):
    hints = []

    def create_body_field(node: ast.AST):
        children_info = []
        for sub_node in node.body:
            children_hints = walk_node_to_create_hints(sub_node, root, file_path, directory)
            children_info.extend(children_hints)
        return children_info

    def visitor(node: ast.AST):
        # Handle functions and classes
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            info = {
                "type": "def",
                "name": node.name,
                "argument_names": [arg.arg for arg in node.args.args],
                "body": create_body_field(node)
            }
            if node.returns:
                info["return_type"] = resolve_name(node.returns)
            elif INCLUDE_ANY_TYPE:
                info["return_type"] = "Any"
            hints.append(info)
        elif isinstance(node, ast.ClassDef):
            info = {
                "type": "class",
                "method_name": (node.name),
                "bases": [resolve_name(base) for base in node.bases],
                "body": create_body_field(node)
            }
            hints.append(info)

        # Handle import and calls
        elif isinstance(node, ast.Import):
            hints.extend([{
                "type": "import",
                "name": name.name,
                "asname": name.asname,
                "module": name.name
            } for name in node.names])
        elif isinstance(node, ast.ImportFrom):
            hints.extend([{
                "type": "import",
                "name": name.name,
                "asname": name.asname,
                "module": node.module
            } for name in node.names])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                function_dict = get_function_dict(file_path, root)
                if node.func.id in function_dict:
                    call_hint = {"type": "unassigend call", "method_name": f"{resolve_name(node.func)}"}
                    call_hint["method_name"] = function_dict[node.func.id]
                    call_hint["type"] = "call"
                    if call_hint not in hints:
                        hints.append(call_hint)
            return False
        else:
            return False
        return True

    walk_node(start_node, root, visitor)
    return hints


class FunctionCallWalker:
    def __init__(self, filepath):
        self.dict = {}
        self.filepath = filepath

    def walk(self, node: ast.AST):

        if isinstance(node, ast.FunctionDef):
            self.dict[node.name] = [self.filepath, node.name]

        if isinstance(node, ast.Import):
            for name in node.names:
                asname = name.asname if name.asname else name.name
                self.dict[asname] = [str(name.name), asname]

        if isinstance(node, ast.ImportFrom):
            for name in node.names:
                asname = name.asname if name.asname else name.name
                self.dict[asname] = [str(node.module), asname]

        return False
