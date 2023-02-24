import html

fill_placeholder ='<input type="textbox" style="padding: 1px">'

def question_header(i):
    return f'<h2>Domanda {i}</h2>\n'

def html_render_choices(q):
    content_text = ''
    content_solution = ''
    text = q._text
    options = q._options
    correct = q._correct
	
    content_text += f'<p>{text}</p>\n'
    content_solution += f'<p>{text}</p>\n'
    
    for j in range(len(options)):
        opt = f'<p class="option"><input type="checkbox" id="ans-{j}">\n<label for="ans-{j}">{options[j]}</label></p>'
        content_text += opt
        checked = 'checked' if correct[j] == 1 else ''
        opt = f'<p class="option"><input type="checkbox" id="ans-{j}" disabled {checked}>\n<label for="ans-{j}">{options[j]}</label></p>'
        content_solution += opt
        j += 1
    content_text += '\n'
    content_solution += '\n'
    
    return content_text, content_solution

def html_render_open(q):
    content_text = q._text
    content_solution = q._text
    return content_text, content_solution
    
def html_render_fill(q):
    content_text = ''
    content_solution = ''
    correct = q._correct
    content_text += f'<p>{q._text}</p>\n\n'
    content_solution += f'<p>{q._text}</p>\n\n'
    to_fill = q._to_fill
    sol_filled = to_fill
    for j in range(len(correct)):
        sol_filled = sol_filled.replace(f'{{{{{j}}}}}', correct[j].upper())
        to_fill = to_fill.replace(f'{{{{{j}}}}}', fill_placeholder)

    content_text += f'<p>{to_fill}</p>\n\n'
    content_solution += f'<p>{sol_filled}</p>\n\n'

    return content_text, content_solution

def html_render_exercise(q):
    content_text = q._text
    content_solution = q._text
    
    content_text += '<ol>\n'
    content_solution += '<ol>\n'
    for sub_q in q._sub_questions:
        content_text += f'<li>{sub_q}</li>\n'
        content_solution += f'<li>{sub_q}</li>\n'
    content_text += '</ol>\n'
    content_solution += '</ol>\n'
    
    return content_text, content_solution

def html_render_composite(q, heading='Esercizio'):
    text = q._text + '\n'
    solution = q._text + '\n'
    i = 1
    for sub_q in q._questions:
        score = f'({sub_q._weight} Punti)'
        text += f'<h3>{heading} {i} {score}</h3>\n'
        solution += f'<h3>{heading} {i}</h3>\n'
        sub_text, sub_solution = html_render_by_type(sub_q)
        text += sub_text
        solution += sub_solution
        i += 1
    return text, solution

def html_render_by_type(q):
    text = ''
    solution = ''
    if q._type in ['single', 'multiple', 'invertible', 'multi-variate']:
        text, solution = html_render_choices(q)
    elif q._type == 'open':
        text, solution = html_render_open(q)
    elif q._type == 'fill':
        text, solution = html_render_fill(q)
    elif q._type =='exercise':
        text, solution = html_render_exercise(q)
    elif q._type == 'composite':
        text, solution = html_render_composite(q)
    return text, solution


def html_render(questions, template_file, text_file, solution_file, track_n):
    text_content = ''
    solved_content = ''
    i = 1
    for q in questions:
        text_content += question_header(i)
        solved_content += question_header(i)
        text, solution = html_render_by_type(q)
        text_content += text
        solved_content += solution
        i += 1

    # Text output
    out = open(template_file).read()
    out = out.replace('{% CONTENT %}', text_content)
    # out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    open(text_file, 'w').write(out)

    # Solution output
    out = open(template_file).read()
    out = out.replace('{% CONTENT %}', solved_content)
    # out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    open(solution_file, 'w').write(out)


