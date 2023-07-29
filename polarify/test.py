import ast
from copy import copy

# TODO: Walruss
# TODO: Switch

def inline_all(expr: ast.expr, assignments: dict[str, ast.expr]) -> ast.expr:
    assignments = copy(assignments)
    if isinstance(expr, ast.Name):
        if expr.id not in assignments:
            raise ValueError(f"Variable {expr.id} not defined")
        return inline_all(assignments[expr.id], assignments)
    elif isinstance(expr, ast.BinOp):
        expr.left = inline_all(expr.left, assignments)
        expr.right = inline_all(expr.right, assignments)
        return expr
    else:
        return expr

def is_returning_body(stmts: list[ast.stmt]) -> bool:
    for s in stmts:
        if isinstance(s, ast.Return):
            return True
        elif isinstance(s, ast.If):
            if is_returning_body(s.body) and is_returning_body(s.orelse):
                return True
            elif is_returning_body(s.body) ^ is_returning_body(s.orelse):
                raise ValueError("All branches of a If statement must either return or not for now")
    return False

def regularize_assign_statement(stmt: ast.Assign, assignments: dict[str, ast.expr]) -> dict[str, ast.expr]:
    assignments_updated = {}
    for t in stmt.targets:
        if isinstance(t, ast.Name):
            assignments_updated[t.id] = inline_all(stmt.value, assignments)
        elif isinstance(t, ast.Tuple):
            for sub_t, sub_v in zip(t.elts, stmt.value.elts):
                if isinstance(sub_t, ast.Name):
                    assignments_updated[sub_t.id] = inline_all(sub_v, assignments)
                else:
                    raise ValueError(
                        f"Unsupported expression type inside of tuple: {type(sub_t)}"
                    )
        else:
            raise ValueError(f"Unsupported expression type: {type(t)}")
    return assignments_updated


def handle_non_returning_if(stmt: ast.If, assignments: dict[str, ast.expr]) -> dict[str, ast.expr]:
    assignments = copy(assignments)
    assert not is_returning_body(stmt.orelse) and not is_returning_body(stmt.body)
    test = inline_all(stmt.test, assignments)

    diff_assignments = dict()
    all_vars_changed_in_body = get_all_vars_changed_in_body(stmt.body, assignments)
    all_vars_changed_in_orelse = get_all_vars_changed_in_body(stmt.orelse, assignments)
    for var in (all_vars_changed_in_body | all_vars_changed_in_orelse).keys():
        expr = build_polars_when_then_otherwise(
            test,
            all_vars_changed_in_body.get(var, assignments[var]),
            all_vars_changed_in_orelse.get(var, assignments[var])
        )
        assignments[var] = expr
        diff_assignments[var] = expr
    return diff_assignments


def get_all_vars_changed_in_body(body: list[ast.stmt], assignments: dict[str, ast.expr]) -> dict[str, ast.expr]:
    assignments = copy(assignments)
    diff_assignments = dict()

    for s in body:
        if isinstance(s, ast.Assign):
            diff = regularize_assign_statement(s, assignments)
            assignments.update(diff)
            diff_assignments.update(diff)
        elif isinstance(s, ast.If):
            if_diff = handle_non_returning_if(s, assignments)
            assignments.update(if_diff)
            diff_assignments.update(if_diff)
        elif isinstance(s, ast.Return):
            raise ValueError("This should not happen.")
        else:
            raise ValueError(f"Unsupported statement type: {type(s)}")

    return diff_assignments

def build_polars_when_then_otherwise(test: ast.expr, then: ast.expr, orelse: ast.expr):
    when_node = ast.Call(
        func=ast.Attribute(
            value=ast.Name(id="pl", ctx=ast.Load()), attr="when", ctx=ast.Load()
        ),
        args=[test],
        keywords=[],
    )
   
    then_node = ast.Call(
        func=ast.Attribute(value=when_node, attr="then", ctx=ast.Load()),
        args=[then],
        keywords=[],
    )
    final_node = ast.Call(
        func=ast.Attribute(value=then_node, attr="otherwise", ctx=ast.Load()),
        args=[orelse],
        keywords=[],
    )
    return final_node

def parse_body(full_body: list[ast.stmt], assignments: dict[str, ast.expr] = {}):
    assignments = copy(assignments)
    assert len(full_body) > 0
    for i, stmt in enumerate(full_body):
        if isinstance(stmt, ast.Assign):
            # update assignments
            assignments.update(regularize_assign_statement(stmt, assignments))
        elif isinstance(stmt, ast.If):
            if is_returning_body(stmt.body) and is_returning_body(stmt.orelse):
                test = inline_all(stmt.test, assignments)
                body = parse_body(stmt.body, assignments)
                orelse = parse_body(stmt.orelse, assignments)
                return build_polars_when_then_otherwise(test, body, orelse)
            elif is_returning_body(stmt.body):
                test = inline_all(stmt.test, assignments)
                body = parse_body(stmt.body, assignments)
                orelse_everything = parse_body(stmt.orelse + full_body[i+1:], assignments)
                return build_polars_when_then_otherwise(test, body, orelse_everything)
            elif is_returning_body(stmt.orelse):
                test = ast.Call(
                    func=ast.Attribute(
                        value=inline_all(stmt.test, assignments),
                        attr="not",
                        ctx=ast.Load()
                    ),
                    args=[],
                    keywords=[],
                )
                orelse = parse_body(stmt.orelse, assignments)
                body_everything = parse_body(stmt.body + full_body[i+1:], assignments)
                return build_polars_when_then_otherwise(test, orelse, body_everything)
            else:
                diff = handle_non_returning_if(stmt, assignments)
                assignments.update(diff)

        elif isinstance(stmt, ast.Return):
            # Handle return statements
            return inline_all(stmt.value, assignments)
        else:
            raise ValueError(f"Unsupported statement type: {type(stmt)}")


code = """
c = d = 2
x, y = pl.col("x") * c, pl.col("y") * d
z = x + y

if z > 0:
    if z > 1:
        return z
    elif z > 0.5:
        return 1
    else:
        return 0.5
else:
    return 0
"""

code = """
k = 0
if x > 0:
    return k
else:
    k = 1

if x > 1:
    k = 2
else:
    return k

if x >= 3:
    return 15

return k * 2
"""

code = """
k = 0
if x > 0:
    k = 1
else:
    k = -1
return k
"""

code = """
k = 0
if x > 0:
    k = 1
elif x < 0:
    k = -1
return k
"""

code = """
k = 0
c = 2
if x > 0:
    k = 1
    c = 0
return k * c
"""

code = """
k = 0
c = 2
if x > 0:
    k = 1
    c = 0
elif x < 0:
    k = -1
return k * c
"""


code = """
k = 0
c = 2
if x > 0:
    k = 1
    c = 0
    if x < 10:
        c = 1
elif x < 0:
    k = -1
return k * c
"""

# TODO
code = """
k = 0
if (k := x) > 0:
    return k
return -1
"""


tree = ast.parse(code)
transformed = parse_body(tree.body)
unparsed = ast.unparse(transformed)

print(unparsed)
