from pathlib import Path

import a.b.c.d as tested

DATA = Path(__file__).parent / "data"

def test_another_function_with_args():
    tested.another_function_with_args(args1, args2)


def test_AClass_a_method():
    obj = AClass()
    obj.a_method(arg1, arg2)
