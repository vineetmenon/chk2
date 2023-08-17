import re

sql_statement = """
SELECT column1,
       SUM('column2') +
       MAX(ABS('column3')) +
       COUNT('column4', 
             'column5'
            ) AS result
FROM table
WHERE column6 = GETDATE()
"""

def evaluate_function(match, eval_func):
    print(match.group(0))
    func_name = match.group(1)
    args = match.group(2)
    evaluated_args = [evaluate_arg(arg, eval_func) for arg in split_arguments(args)]
    evaluated_result = eval_func(func_name, evaluated_args)
    return evaluated_result

def split_arguments(args):
    return [arg.strip() for arg in re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", args)]


def evaluate_arg(arg, eval_func):
    if arg.startswith("'") and arg.endswith("'"):
        return arg
    elif arg and arg != '':
        return evaluate_function(re.match(r"(\w+)\s*\((.*)\)", arg, re.DOTALL), eval_func)
    else:
        return ''

def replace_function_calls(sql, eval_func):
    pattern = r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(([^()]*)\)"
    while re.search(pattern, sql, re.MULTILINE):
        print(sql)
        sql = re.sub(pattern, lambda match: evaluate_function(match, eval_func), sql, flags=re.MULTILINE)

    return sql

def custom_eval_func(func_name, args):
    if func_name == "SUM":
        return f"ret sum"
    elif func_name == "MAX":
        return f"ret max"
    elif func_name == "COUNT":
        return f"ret count"
    else:
        return f"ret {func_name})"

modified_sql = replace_function_calls(sql_statement, custom_eval_func)

print("Original SQL:", sql_statement)
print("Modified SQL:", modified_sql)
