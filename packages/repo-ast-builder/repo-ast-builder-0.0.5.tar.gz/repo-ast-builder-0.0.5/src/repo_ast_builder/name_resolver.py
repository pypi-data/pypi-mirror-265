import ast


def resolve_name(annotation):
    annotation_map = {
        ast.Name: lambda a: a.id,
        ast.Subscript: lambda a: f"{resolve_name(a.value)}[{resolve_name(a.slice)}]",
        ast.Tuple: lambda a: f"({', '.join([resolve_name(elt) for elt in a.elts])})",
        ast.Attribute: lambda a: f"{resolve_name(a.value)}.{a.attr}",
        ast.List: lambda a: f"List[{resolve_name(a.elts[0]) if a.elts else 'Any'}]",
        ast.Dict: lambda a: f"Dict[{resolve_name(a.keys[0]) if a.keys else 'Any'}, {resolve_name(a.values[0]) if a.values else 'Any'}]",
        ast.Constant: lambda a: str(a.value)
    }
    return annotation_map.get(type(annotation), lambda a: "Any")(annotation)
