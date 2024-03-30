import ast

from repo_ast_builder.general_node_walking import walk_node
from repo_ast_builder.name_resolver import resolve_name
from repo_ast_builder.options import INCLUDE_ANY_TYPE


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
            call_hint = {"type": "call", "method_name": f"{resolve_name(node.func)}"}
            if isinstance(node.func, ast.Name):
                walker = FunctionCallWalker(node.func.id)
                walk_node(root, root, walker.walk)
                if walker.has_found():
                    call_hint["method_name"] = (file_path if walker.thisfile else walker.otherfile, node.func.id)
                else:
                    call_hint["type"] = "unassigend call"
            else:
                call_hint["type"] = "unassigend call"

            if call_hint not in hints:
                hints.append(call_hint)
            return False
        else:
            return False
        return True

    walk_node(start_node, root, visitor)
    return hints

class FunctionCallWalker:
    def __init__(self, name):
        self.name = name
        self.type = "unknown"
        self.thisfile = False
        self.otherfile = None

    def walk(self, node: ast.AST):

        if isinstance(node, ast.FunctionDef):
            if node.name == self.name:
                self.thisfile = True

        if isinstance(node, ast.Import):
            for name in node.names:
                asname = name.asname if name.asname else name.name
                if asname == self.name:
                    self.otherfile = str(name.name)

        if isinstance(node, ast.ImportFrom):
            for name in node.names:
                asname = name.asname if name.asname else name.name
                if asname == self.name:
                    self.otherfile = str(node.module)

        return self.has_found()

    def has_found(self):
        return self.thisfile or self.otherfile is not None