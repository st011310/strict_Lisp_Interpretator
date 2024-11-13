def string2lisp(s: str):
    pass

def test_string2lisp():
    f = string2lisp
    assert f('(car)') == ['car']
    assert f('(asd-as)') == ['asd-as']
    assert f('(asd-as 1)') == ['asd-as', 1]

test_string2lisp()