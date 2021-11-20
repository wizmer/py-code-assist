import inspect
import re

from code_assist.testing import corresponding_module_name

def combine_parts(args, body):
    header = 'TODO: fill the func header'
    params = [f'    {arg}: ' for arg in args]
    if params:
        params = 'Args:\n' + '\n'.join(params)
    return '\n\n'.join(filter(None, (header, body, params)))

def generate_docstring(filename, func_name):
    module_name = corresponding_module_name(filename)
    module = __import__(module_name, fromlist=[""])
    the_func = module.__dict__[func_name]
    args = inspect.getfullargspec(the_func).args

    return combine_parts(args, '')

class Docstring:
    def __init__(self, header, params):
        pass

def get_existing_docstring(filename, func_name):
    module_name = corresponding_module_name(filename)
    module = __import__(module_name, fromlist=[""])
    the_func = module.__dict__[func_name]

    print('\n')
    print(the_func.__doc__)
    DOCSTRING_REGEX = re.compile('(.*?)\n+ *Args:(?:\n+ *(.*?): *(.*)$)+', re.DOTALL)
    m = DOCSTRING_REGEX.match(the_func.__doc__)
    assert m
    print(m.groups())

