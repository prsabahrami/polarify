# ruff: noqa
# ruff must not change the AST of the test functions, even if they are semantically equivalent.


def match_case(x):
    s = 0
    match x:
        case 0:
            s = 1
        case 2:
            s = -1
        case _:
            s = 0
    return s


def match_with_or(x):
    match x:
        case 0 | 1:
            return 0
        case 2:
            return 2 * x
        case 3:
            return 3 * x
    return x


def match_sequence(x):
    match x:
        case 0, 1:
            return 0
        case 2:
            return 2 * x
        case 3:
            return 3 * x
    return x


def match_sequence_with_brackets(x):
    match x:
        case [0, 1]:
            return 0
        case 2:
            return 2 * x
        case 3:
            return 3 * x
    return x


def match_assignments_inside_branch(x):
    match x:
        case 0:
            return 0
        case 1:
            return 2 * x
        case 2:
            return 3 * x
    return x


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


def match_compare_expr(x):
    match x:
        case 0:
            return 2
        case 1:
            return 1
        case 10:
            return 2
    return 1


def match_nested_partial_return_with_assignments(x):
    match x:
        case 0:
            return -5 - x
        case 1:
            return 1 * x
        case 2:
            return 2 + x
    return -1 * x


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


def match_sequence_star(x):
    match x:
        case 0, *other:
            return other
        case 1:
            return 1
        case 2:
            return 2
    return x


def match_multiple_variables(x):
    y = 3
    match x, y:
        case 1, 3:
            return 1
        case _:
            return 5


def match_with_guard(x):
    match x:
        case 5 if x > 3:
            return 1
        case _:
            return 5


def match_with_guard_variable(x):
    match x:
        case y if y > 5:
            return 1
        case _:
            return 5


def match_with_guard_multiple_variable(x):
    y = 3
    match x, y:
        case 1, z if z > 3:
            return 1
        case z, 3 if z > 3:
            return 2
        case _:
            return 5


def match_sequence_incomplete(x):
    y = 2
    z = 3
    match x, y, z:
        case 0, 1, 2:
            return 0
        case 1, 2:
            return 1
        case 2:
            return 2
    return x


def match_mapping(x):
    match x:
        case {1: 2}:
            return 1
        case _:
            return x


def multiple_match(x):
    match x:
        case 0:
            return 1
        case 1:
            return 2
    match x:
        case 0:
            return 3
        case 1:
            return 4
    return x


def match_with_assignment(x):
    match x:
        case y if x > 1:
            y = y * 2
            return y
        case _:
            return x


def match_with_assignment_hard(x):
    match x:
        case y if x > 1:
            y = y * 2
        case _:
            return x

    return y + 2


def match_complex_subject(x):
    match x + 2:
        case 3:
            return 1
        case _:
            return x


def match_guarded_match_as_no_return(x):
    match x:
        case 1:
            return 0
        case _ if x > 1:
            return 2


def match_guarded_match_as(x):
    match x:
        case 1:
            return 0
        case _ if x > 1:
            return 2

    return 3


def match_sequence_unmatchable_case_smaller(x):
    y = 2
    z = None

    match x, y, z:
        case 1, 2:
            return 1
        case _:
            return x


def match_sequence_unmatchable_case_larger(x):
    y = 2
    z = None

    match x, y:
        case 1, 2, 3:
            return 1
        case _:
            return x * 2


def match_sequence_unmatchable_case_smaller_return(x):
    y = 1
    z = 2

    match x, y, z:
        case 1, 2:
            x = 4
            return 1
    return x


def match_sequence_unmatchable_case(x):
    y = 1
    z = 2

    match x, y, z:
        case 1, 2:
            return 1
        case 3, 4:
            return -1
        case 1, 2, 3:
            return 2
    return x


def match_guard_no_assignation(x):
    match x:
        case _ if x > 1:
            return 0
        case _:
            return 2


functions_310 = [
    nested_match,
    match_assignments_inside_branch,
    match_signum,
    match_nested_partial_return_with_assignments,
    match_compare_expr,
    match_case,
    match_with_or,
    match_multiple_variables,
    match_with_guard,
    match_with_guard_variable,
    match_with_guard_multiple_variable,
    match_sequence_incomplete,
    multiple_match,
    match_with_assignment,
    match_with_assignment_hard,
    match_complex_subject,
    match_guarded_match_as,
    match_guard_no_assignation,
    match_sequence_unmatchable_case,
    match_sequence_unmatchable_case_smaller,
    match_sequence_unmatchable_case_smaller_return,
    match_sequence_unmatchable_case_larger,
]

unsupported_functions_310 = [
    (match_mapping, "ast.MatchMapping"),
    (match_sequence_star, "starred patterns are not supported."),
    (match_sequence, "Matching lists is not supported."),
    (match_sequence_with_brackets, "Matching lists is not supported."),
    (match_guarded_match_as_no_return, "Not all branches return"),
]
