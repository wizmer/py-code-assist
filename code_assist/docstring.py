import ast
import importlib.util
import inspect
import re
from inspect import getfullargspec
from itertools import chain

from more_itertools.more import first, one, split_at, split_before

from code_assist.testing import corresponding_module_name


def combine_parts(args, body):
    header = "TODO: fill the func header"
    params = [f"    {arg}: " for arg in args]
    if params:
        params = "Args:\n" + "\n".join(params)
    return "\n\n".join(filter(None, (header, body, params)))


def generate_docstring(filename, func_name):
    module_name = corresponding_module_name(filename)
    module = __import__(module_name, fromlist=[""])
    the_func = module.__dict__[func_name]
    args = inspect.getfullargspec(the_func).args

    return combine_parts(args, "")


class Docstring:
    def __init__(self, header, params):
        pass


def parse_params(param_paragraph):
    params = param_paragraph.split("\n")[1:]
    regex = r"^\s*([a-zA-Z0-9_]+):"
    return {
        re.match(regex, lines[0]).group(1): "\n".join(lines)
        for lines in split_before(params, lambda s: re.match(regex, s))
    }


def get_docstring_line_numbers(filename, func_name):
    with open(filename) as f:
        tree = ast.parse(f.read())
    node = one(
        [
            x
            for x in ast.walk(tree)
            if isinstance(x, ast.FunctionDef) and x.name == func_name
        ]
    )

    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Str)
    ):
        return (
            node.body[0].value.lineno - node.body[0].value.s.count("\n") - 1,
            node.body[0].value.lineno,
        )
    return node.lineno, None


def get_docstring(filename, func_name):
    spec = importlib.util.spec_from_file_location("module.name", filename)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)

    func = foo.__dict__[func_name]
    docstring = inspect.getdoc(func)
    docstring = func.__doc__
    paragraphs = docstring.split("\n\n")
    param_paragraph_index = first(
        [
            index
            for index, paragraph in enumerate(paragraphs)
            if paragraph.lstrip().startswith("Args:")
        ],
        default=None,
    )

    params = parse_params(paragraphs[param_paragraph_index])
    updated_params = ["    Args:"] + [
        params.get(arg, f"        {arg}:") for arg in getfullargspec(func).args
    ]
    docstring = "\n\n".join(
        chain(
            paragraphs[:param_paragraph_index],
            ["\n".join(updated_params)],
            paragraphs[param_paragraph_index + 1 :],
        )
    )

    return '    """' + docstring + '"""\n', get_docstring_line_numbers(
        filename, func_name
    )
