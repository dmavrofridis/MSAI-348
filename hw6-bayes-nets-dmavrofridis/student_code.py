import copy


def ask(var, value, evidence, bn):
    # finds all of the unknown and known variables
    evidence_copy_1 = evidence.copy()
    evidence_copy_2 = evidence.copy()
    evidence_copy_1[var] = value
    evidence_copy_2[var] = not value

    # Create a variable which will hold the unknown variables(as a list)
    unknown = list(set(bn.variable_names) - set(evidence_copy_1.keys()))

    numerator = recursive_helper(evidence_copy_1, bn, unknown, bn.variable_names.copy())
    denominator = numerator + recursive_helper(evidence_copy_2, bn, unknown, bn.variable_names.copy())

    return numerator / denominator


def recursive_helper(evidence, bn, unknown, v_list):

    # Get the variable from the list of variables
    variable = v_list.pop(0)
    # Check if the variable we just popped from the variable list is included in the unknown list
    if variable in unknown:
        #  if it is we have to sum the values
        # check if the length of the variable list is > 0, if not return 1
        if len(v_list) > 0:

            ev_true = evidence.copy()
            ev_true[variable] = True
            ev_false = evidence.copy()
            ev_false[variable] = False

            v_index = bn.variable_names.index(variable)
            prob_true = bn.variables[v_index].probability(True, ev_true)
            prob_false = bn.variables[v_index].probability(False, ev_false)

            return (prob_true * recursive_helper(ev_true, bn, unknown, v_list.copy())) + (
                    prob_false * recursive_helper(ev_false, bn, unknown, v_list.copy()))
        else:
            return 1
    else:
        # if not, get the index of the current variable from the bn.variable names and get the probability
        v_index = bn.variable_names.index(variable)
        prob = bn.variables[v_index].probability(evidence[variable], evidence)

    if len(v_list) > 0:
        return prob * recursive_helper(evidence, bn, unknown, v_list.copy())
    else:
        return prob
