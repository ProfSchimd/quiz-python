import sys
import json
import random

template_file = 'template.tex'
text_out_file = 'text.tex'
solution_out_file = 'solution.tex'
fill_placehold = "\\verb|..................|"

def question_header(i):
	return f'\\subsection*{{Quiz {i}}}\n'

def clean(s):
	# TODO replace other formatting
	s = s.replace('</code>', '}')
	s = s.replace('<code>', '\\texttt{')
	s = s.replace('<br>', '\\\\')
	s = s.replace('</strong>', '}')
	s = s.replace('<strong>', '\\textbf{')
	s = s.replace('</u>', '}')
	s = s.replace('<u>', '\\underline{')
	return s

if __name__ == "__main__":
	question_file = 'questions.json'
	if len(sys.argv) > 1:
		question_file = sys.argv[1]
	fp = open(question_file)
	questions = json.load(fp)
	random.shuffle(questions)
	i = 1
	content = ''
	solved = ''
	for q in questions:
		content += question_header(i)
		solved += question_header(i)

		if q['type'] != 'fill':
			content += f'{clean(q["text"])}\n'
			solved += f'{clean(q["text"])}\n'
			content += '\\begin{itemize}\n'
			solved += '\\begin{itemize}\n'
			# to randomize all vectors, we randomize indexing
			indexes = list(range(len(q['options'])))
			random.shuffle(indexes)
			for j in range(len(indexes)):
				opt = q['options'][indexes[j]]
				content += f'  \\item[$\\square$] {clean(opt)}\n'
				# TODO mark correct answers
				mark = '$\\square$'
				if q['correct'][indexes[j]] == 1:
					mark = '$\\checkmark$'
				solved += f'  \\item[{mark}] {clean(opt)}\n'
				j += 1

			content += '\\end{itemize}\n'
			solved += '\\end{itemize}\n'
		# fill type questions are different
		if q['type'] == 'fill':
			content += f'{clean(q["text"])}\\\\\n'
			solved += f'{clean(q["text"])}\\\\\n'
			tofill = clean(q['tofill'])
			for j in range(len(q['correct'])):
				# Attention: order of replacements is important
				sol_filled = tofill.replace(f'{{{{{j}}}}}', q['correct'][j])
				tofill = tofill.replace(f'{{{{{j}}}}}', fill_placehold)
				
			content += tofill
			solved += sol_filled
		i += 1

	# Text output
	out = open(template_file).read()
	out = out.replace('[[--CONTENT--]]', content)
	open(text_out_file, 'w').write(out)

	# Solution output
	out = open(template_file).read()
	out = out.replace('[[--CONTENT--]]', solved)
	open(solution_out_file, 'w').write(out)
	