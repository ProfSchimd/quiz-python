import sys
import json
import random
import argparse

def parse_arguments():
	parser = argparse.ArgumentParser(description='Crea quiz randomizzati.')
	parser.add_argument('--numero', dest='n', type=int, default=-1, help='Numero di domande se -1 (default) usa tutte')
	parser.add_argument('--input', dest='input', default='questions.json', help='File JSON contenente le domande')
	return parser.parse_args()

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

def complement(x):
	return 1-x

if __name__ == "__main__":
	args = parse_arguments()
	print(args)
	question_file = args.input
	fp = open(question_file)
	questions = json.load(fp)
	random.shuffle(questions)
	max_number = args.n
	if max_number < 0 or max_number > len(questions):
		max_number = len(questions)
	i = 1
	content = ''
	solved = ''
	if max_number > len(questions):
		max_number = len(questions)
	for q in questions[:max_number]:
		content += question_header(i)
		solved += question_header(i)
		text = q['text']
		correct = q['correct']
		type = q['type']

		if type != 'fill':
			options = q['options']
			if type == 'invertible':
				alternate = random.randint(0,1)
				text = q['text'][alternate]
				correct = list(map(complement, correct))

			content += f'{clean(text)}\n'
			solved += f'{clean(text)}\n'
			content += '\\begin{itemize}\n'
			solved += '\\begin{itemize}\n'
			# to randomize all vectors, we randomize indexing
			indexes = list(range(len(options)))
			random.shuffle(indexes)
			for j in range(len(indexes)):
				opt = options[indexes[j]]
				content += f'  \\item[$\\square$] {clean(opt)}\n'
				mark = '$\\square$'
				if correct[indexes[j]] == 1:
					mark = '$\\checkmark$'
				solved += f'  \\item[{mark}] {clean(opt)}\n'
				j += 1

			content += '\\end{itemize}\n'
			solved += '\\end{itemize}\n'
		# fill type questions are different
		if type == 'fill':
			content += f'{clean(text)}\\\\\n'
			solved += f'{clean(text)}\\\\\n'
			tofill = clean(q['tofill'])
			for j in range(len(correct)):
				# Attention: order of replacements is important
				sol_filled = tofill.replace(f'{{{{{j}}}}}',correct[j])
				tofill = tofill.replace(f'{{{{{j}}}}}', fill_placehold)
				
			content += tofill
			solved += sol_filled
		i += 1

	# Text output
	out = open(template_file).read()
	out = out.replace('%%--CONTENT--%%', content)
	open(text_out_file, 'w').write(out)

	# Solution output
	out = open(template_file).read()
	out = out.replace('%%--CONTENT--%%', solved)
	open(solution_out_file, 'w').write(out)
	