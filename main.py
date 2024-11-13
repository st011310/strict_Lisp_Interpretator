class LispException(Exception):
    def __init__(self, string):
        super(Exception, self)


lisp_false = 'NIL'
lisp_true = 'T'


PRINT_ALL = False



def lisp_nil():
    return lisp_false

def lisp_t():
    return lisp_true


def run(arg: list | str):
    if isinstance(arg, str):
        arg = arg.lower()
        if arg[0] == '\'':
            return arg[1:]
        else:
            ans = arg
            try:
                arg = eval(f'lisp_{arg}')
                ans = arg()
            except:
                raise LispException(f'Can\'t execute atom "{ans}"!')
            return ans
    if not arg:
        return lisp_false
    if not isinstance(arg, list):
        raise LispException('func_name should\'nt be a list!')
    if len(arg) == 0:
        return lisp_false
    
    func = arg[0]
    
    if not isinstance(func, str):
        raise LispException('Function name should be a string!')

    func = func.lower()

    try:
        func = eval('lisp_' + func)
    except:
        raise LispException(f'No function with name "{func.upper()}".')
    

    return func(*arg[1:])


    
def lisp_car(*args):
    func_name = 'CAR'
    if PRINT_ALL: print(func_name)
    if len(args) > 1:
        raise LispException('CAR have only 1 argument!')
    if len(args) < 1:
        raise LispException('CAR have 1 argument!')
    arg = args[0]
    arg = run(arg)
    if not isinstance(arg, list):
        raise LispException('CAR argument should ba a list!')
    if len(arg) == 0:
        raise LispException('CAR argument can\'t be emtpy!')
    return arg[0]
    
    
def test_lisp_car():
    f = lambda x: lisp_car(['quote', x])
    assert f([1,2,3]) == 1
    assert f([2,1,3]) == 2
    assert f([2]) == 2
    assert f([80, 4]) == 80



def lisp_cdr(*args):
    func_name = 'CDR'
    if PRINT_ALL: print(func_name)
    if len(args) > 1:
        raise LispException(f'{func_name} have only 1 argument!')
    if len(args) < 1:
        raise LispException(f'{func_name} have 1 argument!')
    arg = args[0]
    arg = run(arg)
    if not isinstance(arg, list):
        raise LispException(f'{func_name} argument should ba a list!')
    if len(arg) == 0:
        raise LispException(f'{func_name} argument can\'t be emtpy!')
    if len(arg) == 1:
        return lisp_false
    return arg[1:]


def test_lisp_cdr():
    f = lambda x: lisp_cdr(['quote', x])
    assert f([1,2,3]) == [2, 3]
    assert f([2,1,3]) == [1, 3]
    assert f([2]) == lisp_false


def lisp_quote(*args):
    func_name = 'QUOTE'
    if PRINT_ALL: print(func_name)
    if len(args) > 1:
        raise LispException(f'QUOTE have only 1 argument! Given {len(args)}')
    if len(args) < 1:
        raise LispException('QUOTE have 1 argument!')
    body = args[0]

    return body

def test_lisp_quote():
    f = lisp_quote
    assert f([1,2,3]) == [1,2,3]
    assert f(1) == 1
    assert f([]) == []
    assert f('T') == 'T'



def lisp_cons(*args):
    func_name = 'CONS'
    if PRINT_ALL: print(func_name)
    if len(args) > 2:
        raise LispException(f'{func_name} have only 2 arguments!')
    if len(args) < 2:
        raise LispException(f'{func_name} have 2 arguments!')
    atom = args[0]
    lst = args[1]
    atom = run(atom)
    lst = run(lst)
    if lst == lisp_false:
        lst = []
    if not isinstance(lst, list):
        raise LispException(f'{func_name} second argument should ba a list!')
    return [atom] + lst



def test_lisp_cons():
    f = lambda x1, x2: lisp_cons(['quote', x1], ['quote', x2])
    assert f(5, [1,2,3]) == [5, 1, 2, 3]
    assert f(lisp_false,[2,1,3]) == [lisp_false, 2, 1, 3]
    assert f(lisp_false, lisp_false) == [lisp_false]
    assert f('a',['b','c']) == ['a', 'b','c']



def lisp_atom(*args):
    func_name = 'ATOM'
    if PRINT_ALL: print(func_name)
    if len(args) > 1:
        raise LispException(f'{func_name} have only 1 argument!')
    if len(args) < 1:
        raise LispException(f'{func_name} have 1 argument!')
    atom = args[0]
    atom = run(atom)
    if isinstance(atom, list):
        if atom:
            return lisp_false
        else:
            return lisp_true
    return lisp_true

def test_lisp_atom():
    f = lambda x: lisp_atom(['quote', x])
    assert f(5) == lisp_true
    assert f('5') == lisp_true
    assert f([1]) == lisp_false
    assert f([]) == lisp_true
    assert f(lisp_true) == lisp_true
    assert f(lisp_false) == lisp_true



def lisp_condition(cond):
    if isinstance(cond, list):
        return cond != []
    if isinstance(cond, str):
        return cond.lower() != 'nil'
    return cond != lisp_false





def lisp_eq(*args):
    func_name = 'EQ'
    if PRINT_ALL: print(func_name)
    if len(args) > 2:
        raise LispException(f'{func_name} have only 2 arguments!')
    if len(args) < 2:
        raise LispException(f'{func_name} have 2 arguments!')
    atom1 = args[0]
    atom2 = args[1]
    atom1 = run(atom1)
    atom2 = run(atom2)
    
    cond1 = isinstance(atom1, list)
    cond2 = isinstance(atom2, list)
    if cond1 and cond2:
        raise LispException(f'{func_name} can\'t compare two lists!')
    if lisp_condition(atom1) == lisp_condition(atom2) == False:
        return lisp_true
    if cond1 or cond2:
        return lisp_false
    if isinstance(atom1, str) and isinstance(atom2, str):
        atom1 = atom1.lower()
        atom2 = atom2.lower()
    if atom1 == atom2:
        return lisp_true
    else:
        return lisp_false

def test_lisp_eq():
    f = lambda a1,a2: lisp_eq(['quote', a1], ['quote', a2])
    assert f(5, [1,2,3]) == lisp_false
    assert f(lisp_false, []) == lisp_true
    assert f(1, 2) == lisp_false
    assert f('2', 3) == lisp_false
    assert f(3, 3) == lisp_true




def lisp_cond(*args):
    func_name = 'COND'
    if PRINT_ALL: print(func_name)
    ans = lisp_false
    for lst in args:
        if not isinstance(lst, list):
            raise LispException(f'{func_name} arguments should be lists!')
        if len(lst) == 0:
            raise LispException(f'Any list argument in {func_name} can\'t be empty!')
        ans = lst[0]
        ans = run(ans)
        if lisp_condition(ans):
            body = lst[1:]
            for statement in body:
                ans = run(statement)
            break
    return ans



def test_lisp_cond():
    f = lisp_cond
    assert f([lisp_true]) == lisp_true, f([lisp_true])
    assert f([lisp_false]) == lisp_false
    assert f([lisp_false], [lisp_false]) == lisp_false
    assert f([lisp_false], [lisp_true]) == lisp_true
    assert f([lisp_false],
                    [lisp_true, lisp_false]) == lisp_false



def lisp_eval(*args):
    func_name = 'EVAL'
    if PRINT_ALL: print(func_name)
    if len(args) > 1:
        raise LispException(f'{func_name} have only 1 argument!')
    if len(args) < 1:
        raise LispException(f'{func_name} have 1 argument!')
    body = args[0]
    body = run(body)
    body = run(body)
    return body

def test_lisp_eval():
    
    f = lambda x: lisp_eval(['quote', x])
    assert f(['CAR', ['CDR', ['quote',[1,2,3,4,5]]]]) == 2
    
    f = lambda x: lisp_eval(['quote', ['quote', x]])
    ans = ['CAR', ['CDR', ['quote',[1,2,3,4,5]]]]
    assert f(ans) == ans
 
def lisp_defun(*args):
    func_name = 'DEFUN'
    if PRINT_ALL: print(func_name)
    if len(args) != 3:
        raise LispException(f'{func_name} syntax error!\n Correct tamplate: (DEFUN func params_list body).')
    
    subfunc_name = args[0]
    if type(subfunc_name) is not str:
        raise LispException(f'First argument in {func_name} should be an atom!')
    subfunc_name = subfunc_name.lower()

    func_params = args[1]
    if type(func_params) is not list:
        raise LispException(f'Second argument in {func_name} should be a list!')
    
    func_body = args[2]
    if type(func_body) is not list:
        raise LispException(f'Third argument in {func_name} should be an executable list!')
    
    execute_str = ""
    execute_str += f"def lisp_{subfunc_name}(*args):\n"
    execute_str +=      f"\tpass\n"
    try:
        exec(execute_str)
        # print(execute_str, end = '\n\n')
    except:
        print(f"This interpritator can't create function with name {subfunc_name.upper()}")
        
    execute_str = f'del lisp_{subfunc_name}\n'
    execute_str += f'def lisp_{subfunc_name}(*args):\n'

    for param_index in range(len(func_params)):
        param = func_params[param_index]
        if type(param) is not str:
            raise LispException(f'{func_name}: All params in param_list should be an atom!')
        execute_str += f'\tdef lisp_{param}():\n'
        execute_str += f'\t\treturn run(args[{param_index}])\n'
    for param in func_params:
        execute_str += f'\tmemory = dict()\n'
        execute_str += f"\tif 'lisp_{param}' in globals():\n"
        execute_str += f"\t\tmemory['lisp_{param}'] = globals()['lisp_{param}']\n"
        execute_str += f"\tglobals()['lisp_{param}'] = lisp_{param}\n"
        
    execute_str += f"\tans = run({func_body})\n"
    
    for param in func_params:
        execute_str += f"\tif 'lisp_{param}' in memory:\n"
        execute_str += f"\t\tglobals()['lisp_{param}'] = memory['lisp_{param}']\n"
        execute_str += f"\telse:\n"
        execute_str += f"\t\tdel globals()['lisp_{param}']\n"
    execute_str += f"\treturn ans\n"
    
    try:
        exec(execute_str)
    except Exception as e:
        print(e)
        print(f"This interpritator can't create function with name {subfunc_name.upper()}")
        
    globals()[f"lisp_{subfunc_name}"] = eval(f"lisp_{subfunc_name}")

    return lisp_false

def test_lisp_defun():
    
    lisp_defun('caar', ['x'], ['CAR', ['CAR', 'x']])
    caar = lambda x: run(['CAAR', ['QUOTE', x]])
    assert caar([[2]]) == 2
    assert caar([[2], 3, [4]]) == 2

    lisp_defun('cadr', ['x'], ['CAR', ['CdR', 'x']])
    cadr = lambda x: run(['CADR', ['QUOTE', x]])
    assert cadr([[2], 3, [4]]) == 3
    assert cadr([['a'], [2], [4]]) == [2]
 

test_lisp_quote()
test_lisp_car()
test_lisp_cdr()
test_lisp_cons()
test_lisp_atom()
test_lisp_eq()
test_lisp_cond()
test_lisp_eval()
test_lisp_defun()
