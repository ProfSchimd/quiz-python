import json
import random
import argparse

def parse_arguments():
	parser = argparse.ArgumentParser(description='Generate random quiz from input JSON files.')
	parser.add_argument('--number', dest='n', type=int, default=-1, help='Number of questions, if -1 (default) use all')
	parser.add_argument('--input', dest='input', default='questions.json', help='Comma separated list of JSON file(s) with questions')
	parser.add_argument('--output', dest='output', default='text', help='Name of the output (text) file, without extension')
	parser.add_argument('--solution', dest='solution', default='solution', help='Name of the output (solution) file, without extension')
	parser.add_argument('--tracks', dest='tracks', type=int, default=1, help='Number of tracks (default 1)')
	return parser.parse_args()

template_file = 'template.tex'
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

'''
Loads questions from file, but doesn't randomize it. this function contains the
logic to open file(s), merge them (if multiple are indicated).
'''
def load_questions(args):
	question_files = args.input.split(',')
	questions = []
	for q in question_files:
		with open(q) as fp:
			questions += json.load(fp)
	return questions

def complement(x):
	return 1-x

def create_track(questions, max_number, out_file, sol_file):
	
	random.shuffle(questions)
	i = 1
	content = ''
	solved = ''
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
	open(out_file, 'w').write(out)

	# Solution output
	out = open(template_file).read()
	out = out.replace('%%--CONTENT--%%', solved)
	open(sol_file, 'w').write(out)
	

if __name__ == "__main__":
	args = parse_arguments()
	questions = load_questions(args)
	max_number = args.n
	if max_number < 0 or max_number > len(questions):
		max_number = len(questions)
	for track in range(args.tracks):
		out_file = args.output
		sol_file = args.solution
		if args.tracks > 1:
			out_file += f'_{track+1}'
			sol_file += f'_{track+1}'
		out_file += '.tex'
		sol_file += '.tex'
		create_track(questions, max_number, out_file, sol_file)
	