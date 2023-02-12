import util

fill_placeholder = ".................."

def question_header(i):
    return f'\n\\subsection*{{Domanda {i}}}\n'

def html_to_latex(s):
	s = s.replace('</code>', '}')
	s = s.replace('<code>', '\\texttt{')
	s = s.replace('<br>', '\\\\')
	s = s.replace('</strong>', '}')
	s = s.replace('<strong>', '\\textbf{')
	s = s.replace('</u>', '}')
	s = s.replace('<u>', '\\underline{')
	s = s.replace('</i>', '}')
	s = s.replace('<i>', '\\emph{')
	return s

def latex_render_choices(q):
    content_text = ''
    content_solution = ''
    text = q._text
    options = q._options
    correct = q._correct
	
    content_text += f'{html_to_latex(text)}\n'
    content_solution += f'{html_to_latex(text)}\n'
    content_text += '\\begin{itemize}\n'
    content_solution += '\\begin{itemize}\n'
    for j in range(len(options)):
        opt = options[j]
        content_text += f'  \\item[$\\square$] {html_to_latex(opt)}\n'
        mark = '$\\square$'
        if correct[j] == 1:
            mark = '$\\checkmark$'
        content_solution += f'  \\item[{mark}] {html_to_latex(opt)}\n'
        j += 1

    content_text += '\\end{itemize}\n'
    content_solution += '\\end{itemize}\n'
    return content_text, content_solution

def latex_render_fill(q):
    content_text = ''
    content_solution = ''
    correct = q._correct
    content_text += f'{html_to_latex(q._text)}\n\n\\noindent\n'
    content_solution += f'{html_to_latex(q._text)}\n\n\\noindent\n'
    to_fill = html_to_latex(q._to_fill)
    # in case of code block we better use verbatim environment
    # it is important to check the original _to_fill since the
    # local variabile has already been cleaned with previous call
    if util.is_code_block(q._to_fill):
        to_fill = q._to_fill.replace('<code>', '\\begin{verbatim}\n')
        to_fill = to_fill.replace('</code>', '\n\\end{verbatim}\n')
        to_fill = to_fill.replace('<br>', '\n')
    sol_filled = '' + to_fill
    for j in range(len(correct)):
        # Attention: order of replacements is important
        sol_filled = sol_filled.replace(f'{{{{{j}}}}}', '{\\bf ' + correct[j] + '}')
        to_fill = to_fill.replace(f'{{{{{j}}}}}', fill_placeholder)

    content_text += to_fill
    content_solution += sol_filled

    return content_text, content_solution

def latex_render_open(q):
    content_text = q._text
    content_solution = q._text
    return content_text, content_solution

def latex_render_exercise(q):
    content_text = f'{html_to_latex(q._text)}\n'
    content_solution = f'{html_to_latex(q._text)}\n'
    
    content_text += '\\begin{enumerate}\n'
    content_solution += '\\begin{enumerate}\n'
    for sub_q in q._sub_questions:
        content_text += f'\\item {sub_q}\n'
        content_solution += f'\\item {sub_q}\n'
    content_text += '\\end{enumerate}\n'
    content_solution += '\\end{enumerate}\n'
    
    return content_text, content_solution

def latex_render_composite(q, heading='Esercizio'):
    text = q._text + '\n'
    solution = q._text + '\n'
    i = 1
    for sub_q in q._questions:
        text += f'\\subsection*{{{heading} {i}}}\n'
        solution += f'\\subsection*{{{heading} {i}}}\n'
        sub_text, sub_solution = latex_render_by_type(sub_q)
        text += sub_text
        solution += sub_solution
        i += 1
    return text, solution

def latex_render_by_type(q):
    text = ''
    solution = ''
    if q._type in ['single', 'multiple', 'invertible', 'multi-variate']:
        text, solution = latex_render_choices(q)
    elif q._type == 'open':
        text, solution = latex_render_open(q)
    elif q._type == 'fill':
        text, solution = latex_render_fill(q)
    elif q._type =='exercise':
        text, solution = latex_render_exercise(q)
    elif q._type == 'composite':
        text, solution = latex_render_composite(q)
    return text, solution

def latex_render(questions, template_file, text_file, solution_file, track_n):
    text_content = ''
    solved_content = ''
    i = 1
    for q in questions:
        text_content += question_header(i)
        solved_content += question_header(i)
        text, solution = latex_render_by_type(q)
        text_content += text
        solved_content += solution
        i += 1

    

    # Text output
    out = open(template_file).read()
    out = out.replace('%%--CONTENT--%%', text_content)
    out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    open(text_file + '.tex', 'w').write(out)

    # Solution output
    out = open(template_file).read()
    out = out.replace('%%--CONTENT--%%', solved_content)
    out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    open(solution_file + '.tex', 'w').write(out)

