# ruff: noqa
# ruff must not change the AST of the test functions, even if they are semantically equivalent.


def signum(x):
    s = 0
    if x > 0:
        s = 1
    elif x < 0:
        s = -1
    return s

def match_signum(x):
    s = 0
    match x:
        case 0:
            s = 1
        case 2:
            s = -1
        case 3:
            s = 0
    return s


def signum_no_default(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def nested_partial_return_with_assignments(x):
    if x > 0:
        s = 1
        if x > 1:
            s = 2
            return s + x
        else:
            s = -1
    else:
        return -5 - x
    return s * x

def match_nested_partial_return_with_assignments(x):
    match x:
        case 0:
            return -5 - x
        case 1:
            return 1 * x
        case 2:
            return 2 + x
    return -1 * x


def early_return(x):
    if x > 0:
        return 1
    return 0


def assign_both_branches(x):
    if x > 0:
        s = 1
    else:
        s = -1
    return s


def unary_expr(x):
    s = -x
    return s


def call_target_identity(x):
    return x


def call_expr(x):
    k = x * 2
    s = call_target_identity(k + 3)
    return s


def if_expr(x):
    s = 1 if x > 0 else -1
    return s


def if_expr2(x):
    s = 1 + (x if x > 0 else -1)
    return s


def if_expr3(x):
    s = 1 + ((3 if x < 10 else 5) if x > 0 else -1)
    return s


def compare_expr(x):
    if (0 < x) & (x < 10):
        s = 1
    else:
        s = 2
    return s

def match_compare_expr(x):
    match x:
        case 0:
            return 2
        case 1:
            return 1
        case 10:
            return 2
    return 1

def bool_op(x):
    if (0 < x) and (x < 10):
        return 0
    else:
        return 1


def chained_compare_expr(x):
    if 0 < x < 10:
        s = 1
    else:
        s = 2
    return s


def walrus_expr(x):
    if (y := x + 1) > 0:
        s = 1
    else:
        s = -1
    return s * y


def multiple_if_else(x):
    if x > 0:
        s = 1
    elif x < 0:
        s = -1
    else:
        s = 0
    return s


def nested_if_else(x):
    if x > 0:
        if x > 1:
            s = 2
        else:
            s = 1
    elif x < 0:
        s = -1
    else:
        s = 0
    return s

def nested_match(x):
    match x:
        case 0:
            match x:
                case 0:
                    return 1
                case 1:
                    return 2
            return 3
        case 1:
            return 4
    return 5

def nested_if_else_expr(x):
    if x > 0:
        s = 2 if x > 1 else 1
    elif x < 0:
        s = -1
    else:
        s = 0
    return s


def assignments_inside_branch(x):
    if x > 0:
        s = 1
        s = s + 1
        s = x * s
    elif x < 0:
        s = -1
        s = s - 1
        s = x
    else:
        s = 0
    return s


def match_assignments_inside_branch(x):
    match x:
        case 0:
            return 0
        case 1:
            return 2 * x
        case 2:
            return 3 * x
    return x


def override_default(x):
    s = 0
    if x > 0:
        s = 10
    return x * s


def no_if_else(x):
    s = x * 10
    k = x - 3
    k = k * 2
    return s * k


def two_if_expr(x):
    a = 1 if x > 0 else 5
    b = 2 if x < 0 else 2
    return a + b


def multiple_equals(x):
    a = b = 1
    return x + a + b


functions = [
    signum,
    early_return,
    assign_both_branches,
    unary_expr,
    call_expr,
    if_expr,
    if_expr2,
    if_expr3,
    compare_expr,
    multiple_if_else,
    nested_if_else,
    nested_if_else_expr,
    assignments_inside_branch,
    override_default,
    no_if_else,
    two_if_expr,
    signum_no_default,
    nested_partial_return_with_assignments,
    multiple_equals,
    nested_match,
    match_assignments_inside_branch,
    match_signum,
    match_nested_partial_return_with_assignments,
    match_compare_expr,
]

xfail_functions = [
    walrus_expr,
]

unsupported_functions = [
    # function, match string in error message
    (chained_compare_expr, "Polars can't handle chained comparisons"),
    (bool_op, "ast.BoolOp"),  # TODO: make error message more specific
]
