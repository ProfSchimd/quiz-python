import textwrap

def question_header(i):
    header = f'DOMANDA {i}\n'
    # -1 accounts for the '\n' character
    header += '=' * (len(header)-1) + '\n'
    return header


def text_render_choices(q):
    text = ''
    solution = ''
    return text, solution


def text_render_open(q):
    text = '\n'.join(textwrap.wrap(q._text, width=80))
    content_text = text
    content_solution = text
    return content_text, content_solution


def text_render_fill(q):
    text = ''
    solution = ''
    return text, solution

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


def text_render(questions, template_file, text_file, solution_file, track_n):
    text_content = ''
    solved_content = ''
    i = 1
    for q in questions:
        text_content += question_header(i)
        solved_content += question_header(i)
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
        text_content += text
        solved_content += solution
        i += 1

    # Text output
    # out = open(template_file).read()
    # out = out.replace('%%--CONTENT--%%', text_content)
    # out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    out = text_content
    open(text_file + '.txt', 'w').write(out)

    # Solution output
    # out = open(template_file).read()
    # out = out.replace('%%--CONTENT--%%', solved_content)
    # out = out.replace('%%--FOOTRIGHT--%%', f'T:{track_n}')
    out = solved_content
    open(solution_file + '.txt', 'w').write(out)
