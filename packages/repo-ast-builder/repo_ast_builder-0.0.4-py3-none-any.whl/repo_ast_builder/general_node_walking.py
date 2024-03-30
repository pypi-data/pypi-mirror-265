import ast
from typing import List


def walk_node(node: ast.AST, root, is_handled):
    # Terminal nodes
    if is_handled(node):
        return
    if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
        walk_nodes(node.body, root, is_handled)
    elif isinstance(node, ast.ClassDef):
        walk_nodes(node.body, root, is_handled)

    # Handle import and calls
    elif isinstance(node, ast.Import):
        pass
    elif isinstance(node, ast.ImportFrom):
        pass
    elif isinstance(node, ast.Constant):
        pass
    elif isinstance(node, ast.Name):
        pass
    elif isinstance(node, ast.AnnAssign):
        pass
    elif isinstance(node, ast.Attribute):
        pass
    elif isinstance(node, ast.Assert):
        pass
    elif isinstance(node, ast.Global):
        pass
    elif isinstance(node, ast.Nonlocal):
        pass
    elif isinstance(node, ast.Continue):
        pass
    elif isinstance(node, ast.Pass):
        pass
    elif isinstance(node, ast.Break):
        pass

    # Handle single successor
    elif isinstance(node, ast.Call):
        walk_nodes(node.args, root, is_handled)
    elif isinstance(node, ast.FormattedValue):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Await):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Return):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Starred):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Yield):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.YieldFrom):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Expr):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Assign):
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Compare):
        walk_node(node.left, root, is_handled)
    elif isinstance(node, ast.UnaryOp):
        walk_node(node.operand, root, is_handled)
    elif isinstance(node, ast.Raise):
        walk_node(node.exc, root, is_handled)


    elif isinstance(node, ast.Module):
        walk_nodes(node.body, root, is_handled)
    elif isinstance(node, ast.If):
        walk_nodes(node.body, root, is_handled)
        walk_node(node.test, root, is_handled)
        walk_nodes(node.orelse, root, is_handled)
    elif isinstance(node, ast.BinOp):
        walk_node(node.left, root, is_handled)
        walk_node(node.right, root, is_handled)
    elif isinstance(node, ast.NamedExpr):
        walk_node(node.value, root, is_handled)
        walk_node(node.target, root, is_handled)
    elif isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
        walk_nodes(node.body, root, is_handled)
        walk_node(node.iter, root, is_handled)
        walk_node(node.target, root, is_handled)
    elif isinstance(node, ast.While):
        walk_nodes(node.body, root, is_handled)
        walk_node(node.test, root, is_handled)
    elif isinstance(node, ast.List):
        walk_nodes(node.elts, root, is_handled)
    elif isinstance(node, ast.BoolOp):
        walk_nodes(node.values, root, is_handled)
    elif isinstance(node, ast.Try):
        walk_nodes(node.body, root, is_handled)
        walk_nodes(node.handlers, root, is_handled)
        walk_nodes(node.finalbody, root, is_handled)
    elif isinstance(node, ast.Subscript):
        walk_node(node.slice, root, is_handled)
        walk_node(node.value, root, is_handled)
    elif isinstance(node, ast.Dict):
        walk_nodes(node.keys, root, is_handled)
        walk_nodes(node.values, root, is_handled)
    elif isinstance(node, ast.Delete):
        walk_nodes(node.targets, root, is_handled)
    elif isinstance(node, ast.SetComp):
        walk_node(node.elt, root, is_handled)
        walk_nodes(node.generators, root, is_handled)
    elif isinstance(node, ast.ListComp):
        walk_node(node.elt, root, is_handled)
        walk_nodes(node.generators, root, is_handled)
    elif isinstance(node, ast.DictComp):
        walk_node(node.key, root, is_handled)
        walk_node(node.value, root, is_handled)
        walk_nodes(node.generators, root, is_handled)
    elif isinstance(node, ast.comprehension):
        walk_node(node.iter, root, is_handled)
        walk_node(node.target, root, is_handled)
        walk_nodes(node.ifs, root, is_handled)
    elif isinstance(node, ast.GeneratorExp):
        walk_node(node.elt, root, is_handled)
        walk_nodes(node.generators, root, is_handled)
    elif isinstance(node, ast.Tuple):
        walk_nodes(node.elts, root, is_handled)
    elif isinstance(node, ast.ExceptHandler):
        walk_nodes(node.body, root, is_handled)
    elif isinstance(node, ast.JoinedStr):
        walk_nodes(node.values, root, is_handled)
    elif isinstance(node, ast.Slice):
        walk_node(node.upper, root, is_handled)
        walk_node(node.lower, root, is_handled)
        walk_node(node.step, root, is_handled)
    elif isinstance(node, ast.AugAssign):
        walk_node(node.value, root, is_handled)
        walk_node(node.target, root, is_handled)
    elif isinstance(node, ast.With) or isinstance(node, ast.AsyncWith):
        walk_nodes(node.body, root, is_handled)
        walk_nodes(node.items, root, is_handled)
    elif isinstance(node, ast.Lambda):
        walk_node(node.body, root, is_handled)
    elif isinstance(node, ast.Set):
        walk_nodes(node.elts, root, is_handled)
    elif isinstance(node, ast.withitem):
        walk_node(node.context_expr, root, is_handled)
        walk_node(node.optional_vars, root, is_handled)
    elif node is None:
        pass
    elif isinstance(node, ast.IfExp):
        walk_node(node.body, root, is_handled)
        walk_node(node.test, root, is_handled)
        walk_node(node.orelse, root, is_handled)
    else:
        print("Unsupported node type: " + str(type(node)))


def walk_nodes(nodes: List[ast.AST], root, callback):
    for node in nodes:
        walk_node(node, root, callback)
