import textwrap

fill_placeholder = ".................."

def html_to_text(s):
    s = s.replace('</code>', '')
    s = s.replace('<code>', '')
    s = s.replace('<br>', '\n')
    s = s.replace('</strong>', '')
    s = s.replace('<strong>', '')
    s = s.replace('</b>', '')
    s = s.replace('<b>', '')
    s = s.replace('</u>', '')
    s = s.replace('<u>', '')
    s = s.replace('</i>', '')
    s = s.replace('<i>', '')
    return s

def question_header(i):
    header = f'DOMANDA {i}\n'
    # -1 accounts for the '\n' character
    header += '=' * (len(header)-1) + '\n'
    return header


def text_render_choices(q):
    content_text = ''
    content_solution = ''
    text = q._text
    options = q._options
    correct = q._correct
	
    content_text += f'{html_to_text(text)}\n'
    content_solution += f'{html_to_text(text)}\n'
    
    for j in range(len(options)):
        opt = options[j]
        content_text += '\n'.join(textwrap.wrap(
            html_to_text(opt),
            width=80,
            initial_indent=' [ ] ',
            subsequent_indent='     ')
        ) + '\n'
        mark = ' [ ] '
        if correct[j] == 1:
            mark = ' [X] '
        content_solution += '\n'.join(textwrap.wrap(
            html_to_text(opt),
            width=80,
            initial_indent=mark,
            subsequent_indent='     ')
        ) + '\n'
        j += 1
    content_text += '\n'
    content_solution += '\n'
    
    return content_text, content_solution


def text_render_open(q):
    text = '\n'.join(textwrap.wrap(q._text, width=80))
    content_text = text
    content_solution = text
    return content_text, content_solution


def text_render_fill(q):
    content_text = ''
    content_solution = ''
    correct = q._correct
    content_text += f'{html_to_text(q._text)}\n\n'
    content_solution += f'{html_to_text(q._text)}\n\n'
    to_fill = html_to_text(q._to_fill)
    sol_filled = '' + to_fill
    for j in range(len(correct)):
        sol_filled = sol_filled.replace(f'{{{{{j}}}}}', correct[j].upper())
        to_fill = to_fill.replace(f'{{{{{j}}}}}', fill_placeholder)

    content_text += to_fill + '\n\n'
    content_solution += sol_filled + '\n\n'

    return content_text, content_solution

def text_render_exercise(q):
    text = '\n'.join(textwrap.wrap(q._text, width=80)) + '\n'
    content_text = text
    content_solution = text
    for sub_q in q._sub_questions:
        s = '\n'.join(textwrap.wrap(sub_q, width=80, 
            initial_indent='- ', subsequent_indent='  '))
        content_text += s + '\n'
        content_solution += s + '\n'
    return content_text, content_solution

def text_render_composite(q, heading='Esercizio'):
    text = q._text + '\n'
    solution = q._text + '\n'
    i = 1
    for sub_q in q._questions:
        h = heading + ' ' + str(i)
        h += '\n' + '-'*len(h) + '\n'
        text += '\n' + h
        solution += '\n' + h
        sub_text, sub_solution = text_render_by_type(sub_q)
        text += sub_text
        solution + sub_solution
        i += 1
    text += '\n\n'
    solution += '\n\n'
    return text, solution

def text_render_by_type(q):
    text = ''
    solution = ''
    if q._type in ['single', 'multiple', 'invertible', 'multi-variate']:
        text, solution = text_render_choices(q)
    elif q._type == 'open':
        text, solution = text_render_open(q)
    elif q._type == 'fill':
        text, solution = text_render_fill(q)
    elif q._type == 'exercise':
        text, solution = text_render_exercise(q)
    elif q._type == 'composite':
        text, solution = text_render_composite(q)
    return text, solution 


def text_render(questions, template_file, text_file, solution_file, track_n):
    
    text_content = ''
    solved_content = ''
    i = 1
    for q in questions:
        text_content += question_header(i)
        solved_content += question_header(i)
        text, solution = text_render_by_type(q)
        text_content += text
        solved_content += solution
        i += 1

    # Text output
    # out = open(template_file).read()
    # out = out.replace('%%--CONTENT--%%', text_content)
    # out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    out = text_content
    open(text_file, 'w').write(out)

    # Solution output
    # out = open(template_file).read()
    # out = out.replace('%%--CONTENT--%%', solved_content)
    # out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    out = solved_content
    open(solution_file, 'w').write(out)
