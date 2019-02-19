from IPython.core.display import display, HTML


def parse_simple_eqn(q):
    """ Return TeX equivalent of a command 
    without parentheses. """
    # Define replacement rules.
    simple_replacements = [[' ', ''], ['**', '^'], ['*', ' \\cdot '], ['math.', ''], ['np.', ''], ['pi', '\\pi'] , ['cos', '\\cos'], ['sin', '\\sin'], ['csc', '\\csc'], ['cot', '\\cot'], ['tan', '\\tan'], ['sec', '\\sec']]  #['tan', '\\tan'], ['sec', '\\sec']
    complex_replacements = [['^', '{{{i1}}}^{{{i2}}}'], ['_', '{{{i1}}}_{{{i2}}}'], ['/', '\\frac{{{i1}}}{{{i2}}}'], ['sqrt','\\sqrt{{{i2}}}']]
    # Carry out simple replacements
    for pair in simple_replacements:
        q = q.replace(pair[0], pair[1])
    # Now complex replacements
    for item in ['*', '/', '+', '-', '^', '_', ',', 'sqrt']:
        q = q.replace(item, ' ' + item + ' ')
    q_split = q.split()
    for index, item in enumerate(q_split):
        for pair in complex_replacements:
            if item == pair[0]:
                if item == 'sqrt':
                    match_str = " ".join(q_split[index:index+2])
                else:
                    match_str = " ".join(q_split[index-1:index+2])
                q = q.replace(match_str, pair[1].format(
                    i1=q_split[index-1], i2=q_split[index+1]))
    return q

def command_to_latex(q, index=0):
    """ Recursively eliminate parentheses. Once
    removed, apply parse_simple_eqn.        """
    open_index, close_index = -1, -1
    for q_index, i in enumerate(q):
        if i == '(':
            open_index = q_index
        elif i == ')':
            close_index = q_index
            break
    if open_index != -1:
        o = q[:open_index] + '@' + str(index) + q[close_index + 1:]
        m = q[open_index + 1:close_index]
        o_tex  = command_to_latex(o, index + 1)
        m_tex  = command_to_latex(m, index + 1)
        # Clean up redundant parentheses at recombination
        r_index = o_tex.find('@' + str(index))
        # if o_tex[r_index - 1] == '{':
        #     return o_tex.replace('@'+str(index), m_tex)
        # else:
        return o_tex.replace('@'+str(index), 
                                 ' \\left (' + m_tex + ' \\right )')
    else:
        return parse_simple_eqn(q)

def pretty_print_latex(q):
    q_tex = command_to_latex(q)
    # print q_tex
    # return HTML("<h1>$" + q_tex + "$</h1>" )
    return q_tex
   
# s = 'f(x_123, 2) / (2 + 3/(1 + z(np.sqrt((x + 3)/3)))) + np.sqrt(2 ** w) * np.tanh(2 * math.pi* x)'
# pretty_print_latex(s)