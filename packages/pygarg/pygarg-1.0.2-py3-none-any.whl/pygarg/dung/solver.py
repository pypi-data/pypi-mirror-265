import sys
from pysat.solvers import Solver
from pysat.examples.lbx import LBX
from pysat.formula import WCNF
from pysat.formula import CNF
from pygarg.dung import encoding


def get_attackers(args, atts, arg):
    """Provide the attackers of an argument as a list.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    arg -- the target argument
    """
    attackers = []
    for potential_attacker in args:
        if [potential_attacker, arg] in atts:
            attackers.append(potential_attacker)
    return attackers


def argset_from_model(model, args):
    """Convert a model into the corresponding list of arguments.

    Arguments:
    model -- the model to convert
    args -- the arguments in the AF
    """
    extension = []
    for literal in model:
        int_literal = int(literal)
        if int_literal > 0 and int_literal <= len(args):
            arg_name = ""
            arg_name = args[int_literal - 1]
            extension.append(arg_name)
    return extension


def negate_model(model):
    """Create the clause corresponding to the negation of a model.

    Argument:
    model -- the model that must be negated
    """
    negation_clause = []
    for literal in model:
        negation_clause.append(-literal)
    return negation_clause


def get_encoding(args, atts, semantics):
    """Provide the SAT encoding of a semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    semantics -- the semantics of interest
    """
    if semantics == "CF":
        return encoding.conflict_free(args, atts)
    if semantics == "AD":
        return encoding.admissibility(args, atts)
    if semantics == "ST":
        return encoding.stable(args, atts)
    if semantics == "CO":
        return encoding.complete(args, atts)
    sys.exit(f"No SAT encoding for the semantics : {semantics}")


def credulous_acceptability(args, atts, argname, semantics):
    """Determine the credulous acceptability of an argument

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    argname -- the query argument
    semantics -- the semantics
    """
    if args == []:
        return False, None

    if semantics == "ID":
        id_extension = compute_ideal_extension(args, atts)
        if argname in id_extension:
            return True, id_extension
        else:
            return False, id_extension

    if semantics == "GR":
        gr_extension = compute_grounded_extension(args, atts)
        if argname in gr_extension:
            return True, gr_extension
        else:
            return False, gr_extension

    if semantics == "SST":
        return semistable_credulous_acceptability(args, atts, argname)

    if semantics == "PR":
        semantics = "AD"
    n_vars, clauses = get_encoding(args, atts, semantics)
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)

    s.add_clause([arg_var])

    if s.solve():
        model = s.get_model()
        s.delete()
        return True, argset_from_model(model, args)
    s.delete()
    return False, None


def preferred_skeptical_acceptability(args, atts, argname):
    """Determine the skeptical acceptability under the preferred semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    argname -- the query argument
    """
    n_vars, clauses = get_encoding(args, atts, "AD")
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    for mcs in lbx.enumerate():
        lbx.block(mcs)
        if arg_var in mcs:
            return False, argset_from_model(get_mss_from_mcs(mcs, args), args)

    return True, None


def compute_some_preferred_extension(args, atts):
    """Compute one extension under the preferred semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    """
    n_vars, clauses = get_encoding(args, atts, "AD")

    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    result = argset_from_model(get_mss_from_mcs(lbx.compute(), args), args)
    lbx.delete()
    return result


def get_unattacked_arguments(args, atts):
    """Provide the unattacked arguments as a list.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    """
    unattacked = []

    for arg in args:
        is_unattacked = True
        for attack in atts:
            if attack[1] == arg:
                is_unattacked = False
        if is_unattacked:
            unattacked.append(arg)

    return unattacked


def get_defended_set(args, atts, arg_set):
    """Provide the arguments defended by a given set of arguments.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    arg_set -- the set of defending arguments
    """
    if arg_set == []:
        return get_unattacked_arguments(args, atts)
    else:
        defended = []
        for arg in args:
            defended_against_all = True
            for attacker in get_attackers(args, atts, arg):
                defenders = get_attackers(args, atts, attacker)
                defended_against_this_one = False
                for defender in defenders:
                    if defender in arg_set:
                        defended_against_this_one = True
                if not defended_against_this_one:
                    defended_against_all = False
            if defended_against_all:
                defended.append(arg)
        return defended


def compute_grounded_extension(args, atts):
    """Compute the grounded extension."""
    extension = []
    defended = get_defended_set(args, atts, extension)

    while defended != extension:
        extension = defended
        defended = get_defended_set(args, atts, extension)

    return extension


def intersection(lst1, lst2):
    """Compute the intersection of two lists."""
    return list(set(lst1) & set(lst2))


def intersection_all(args, extensions):
    """Compute the intersection of a set of extensions."""
    result = args
    for extension in extensions:
        result = intersection(result, extension)
    return result


def compute_ideal_extension(args, atts):
    """Provide the ideal extension."""
    preferred_extensions = extension_enumeration(args, atts, "PR")

    skeptical_pr_arguments = intersection_all(args, preferred_extensions)

    n_vars, clauses = get_encoding(args, atts, "AD")

    for arg in args:
        if arg not in skeptical_pr_arguments:
            clauses.append([-encoding.sat_var_from_arg_name(arg, args)])

    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    result = argset_from_model(get_mss_from_mcs(lbx.compute(), args), args)
    lbx.delete()
    return result


def get_range_mss_from_mcs(mcs, args):
    """Transform a MCS into the corresponding range."""
    mss = []

    for arg in args:
        if encoding.sat_var_from_arg_name(arg, args) not in mcs:
            mss.append(encoding.sat_var_from_arg_name(arg, args))

    return mss


def get_extension_from_range(mcs, args):
    """Get an extension from the Boolean variables encoding its range."""
    mss = get_range_mss_from_mcs(mcs, args)
    extension = []
    for arg in args:
        if encoding.sat_var_from_arg_name(arg, args) in mss:
            extension.append(arg)
    return extension


def compute_some_semistable_extension(args, atts):
    """Compute one semi-stable extension."""
    n_vars, clauses = get_encoding(args, atts, "CO")

    soft_clauses = []

    wcnf = WCNF()
    cnf = CNF()
    for clause in clauses:
        cnf.append(clause)
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args),
                    encoding.sat_var_Pa_from_arg_name(argument, args)],
                    weight=1)
        soft_clauses.append([encoding.sat_var_from_arg_name(argument, args),
                            encoding.sat_var_Pa_from_arg_name(argument, args)])

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    mcs = lbx.compute()
    lbx.delete()

    mss = []
    for clause_index in range(1, len(soft_clauses)+1):
        if clause_index not in mcs:
            mss.append(clause_index)

    for clause_index in mss:
        cnf.append(soft_clauses[clause_index-1])

    s = Solver(name='g4')
    for clause in cnf.clauses:
        s.add_clause(clause)

    if s.solve():
        model = s.get_model()
        s.delete()
        return argset_from_model(model, args)

    s.delete()
    sys.exit("There cannot be no semi-stable extension.")


def compute_some_extension(args, atts, semantics):
    """Compute an extension under a given semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    semantics -- the chosen semantics
    """
    if args == []:
        return []

    if semantics == "PR":
        return compute_some_preferred_extension(args, atts)

    if semantics == "GR":
        return compute_grounded_extension(args, atts)

    if semantics == "ID":
        return compute_ideal_extension(args, atts)

    if semantics == "SST":
        return compute_some_semistable_extension(args, atts)

    n_vars, clauses = get_encoding(args, atts, semantics)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)

    if s.solve():
        model = s.get_model()
        s.delete()
        return argset_from_model(model, args)

    return "NO"


def get_mss_from_mcs(mcs, args):
    """Transform a minimal correction set into a maximal satisfiable set."""
    mss = []
    for arg in args:
        if encoding.sat_var_from_arg_name(arg, args) not in mcs:
            mss.append(encoding.sat_var_from_arg_name(arg, args))
    return mss


def preferred_extension_enumeration(args, atts):
    """Enumerate the preferred extensions."""
    n_vars, clauses = get_encoding(args, atts, "AD")

    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args)], weight=1)

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    extensions = []
    for mcs in lbx.enumerate():
        lbx.block(mcs)
        extensions.append(argset_from_model(get_mss_from_mcs(mcs, args), args))

    return extensions


def get_semistable_extensions_from_MCS(args, atts, mcs,
                                       hard_clauses, soft_clauses):
    """Transform a MCS into a semi-stable extension.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    mcs -- the MCS
    hard_clauses -- the hard clauses in the encoding
    soft clauses -- the soft clauses in the encoding
    """
    extensions = []

    # Get MSS from MCS
    mss = []
    for clause_index in range(1, len(soft_clauses)+1):
        if clause_index not in mcs:
            mss.append(clause_index)

    # Add the soft clauses from the MSS to the set of hard clauses
    for clause_index in mss:
        hard_clauses.append(soft_clauses[clause_index-1])

    s = Solver(name='g4')
    for clause in hard_clauses:
        s.add_clause(clause)

    for model in s.enum_models():
        extensions.append(argset_from_model(model, args))

    return extensions


def semistable_extension_enumeration(args, atts):
    """Enumerate the semi-stable extensions."""
    n_vars, clauses = get_encoding(args, atts, "CO")

    soft_clauses = []
    wcnf = WCNF()
    for clause in clauses:
        wcnf.append(clause)
    for argument in args:
        wcnf.append([encoding.sat_var_from_arg_name(argument, args),
                    encoding.sat_var_Pa_from_arg_name(argument, args)],
                    weight=1)
        soft_clauses.append([encoding.sat_var_from_arg_name(argument, args),
                            encoding.sat_var_Pa_from_arg_name(argument, args)])

    lbx = LBX(wcnf, use_cld=True, solver_name='g4')
    extensions = []
    for mcs in lbx.enumerate():
        lbx.block(mcs)
        extensions += get_semistable_extensions_from_MCS(args, atts,
                                                         mcs, clauses,
                                                         soft_clauses)

    lbx.delete()

    return extensions


def semistable_skeptical_acceptability(args, atts, argname):
    """Determine skeptical acceptability under the semi-stable semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    argname -- the query argument
    """
    extensions = semistable_extension_enumeration(args, atts)
    for extension in extensions:
        if argname not in extension:
            return False, extension

    return True, None


def semistable_credulous_acceptability(args, atts, argname):
    """Determine credulous acceptability under the semi-stable semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    argname -- the query argument
    """
    extensions = semistable_extension_enumeration(args, atts)
    for extension in extensions:
        if argname in extension:
            return True, extension

    return False, None


def extension_enumeration(args, atts, semantics):
    """Enumerate the extensions under a given semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    semantics -- the chosen semantics
    """
    if args == []:
        return [[]]

    if semantics == "PR":
        return preferred_extension_enumeration(args, atts)
    if semantics == "ID":
        return [compute_ideal_extension(args, atts)]
    if semantics == "GR":
        return [compute_grounded_extension(args, atts)]
    if semantics == "SST":
        return semistable_extension_enumeration(args, atts)
    n_vars, clauses = get_encoding(args, atts, semantics)
    extensions = []

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)

    for model in s.enum_models():
        extensions.append(argset_from_model(model, args))

    s.delete()
    return extensions


def extension_counting(args, atts, semantics):
    """Count the number of extensions for a given semantics.

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    semantics -- the chosen semantics
    """
    if args == [] or semantics == "ID" or semantics == "GR":
        return 1
    return len(extension_enumeration(args, atts, semantics))


def print_witness_extension(extension):
    """Print an extension."""
    print("w ", end='')
    for argname in extension:
        print(f"{argname} ", end='')
    print("")


def skeptical_acceptability(args, atts, argname, semantics):
    """Determine the skeptical acceptability of an argument

    Arguments:
    args -- the arguments in the AF
    atts -- the attacks in the AF
    argname -- the query argument
    semantics -- the semantics
    """
    if args == []:
        return False, []

    if semantics == "PR":
        return preferred_skeptical_acceptability(args, atts, argname)

    if semantics == "SST":
        return semistable_skeptical_acceptability(args, atts, argname)

    if semantics == "ID":
        id_extension = compute_ideal_extension(args, atts)
        if argname in id_extension:
            return True, id_extension
        else:
            return False, id_extension

    if semantics == "GR" or semantics == "CO":
        gr_extension = compute_grounded_extension(args, atts)
        if argname in gr_extension:
            return True, gr_extension
        else:
            return False, gr_extension

    n_vars, clauses = get_encoding(args, atts, semantics)
    arg_var = encoding.sat_var_from_arg_name(argname, args)

    s = Solver(name='g4')
    for clause in clauses:
        s.add_clause(clause)

    s.add_clause([-arg_var])

    if s.solve():
        model = s.get_model()
        s.delete()
        return False, argset_from_model(model, args)
    s.delete()
    return True, None
