"""Main module."""
import json
import random
import argparse
import os.path

from rendering.latex_render import latex_render
from rendering.text_rendering import text_render
from rendering.html_rendering import html_render
import Question as qst


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate random quiz from input JSON files.')
    parser.add_argument('--number', dest='n', type=int, default=-1,
                        help='Number of questions, if -1 (default) use all')
    parser.add_argument('--input', dest='input', default='questions.json',
                        help='Comma separated list of JSON file(s) with questions')
    parser.add_argument('--output', dest='output', default='text',
                        help='Name of the output (text) file, without extension')
    parser.add_argument('--solution', dest='solution', default='solution',
                        help='Name of the output (solution) file, without extension')
    parser.add_argument('--destination', dest='destination', default='.',
                        help='Directory where the output files will be put')
    parser.add_argument('--tracks', dest='tracks', type=int,
                        default=1, help='Number of tracks (default 1)')
    parser.add_argument('--seed', dest='seed', default=None,
                        help='Integer value for seeding randomization (default is no seeding)')
    parser.add_argument('--render', dest='render', default='latex', 
                        help='Defines the rendering type: latex, text (default is latex)')
    parser.add_argument('--test', dest='test', type=int,
                        default=0, help='Used for developing purpose')
    return parser.parse_args()


template_file = 'template.tex'

def load_questions(args):
    """Loads questions from file, but doesn't randomize it. 
    
    This function contains the logic to open file(s), merge them
    (if multiple are indicated)."""
    question_files = args.input.split(',')
    questions = []
    for q in question_files:
        with open(os.path.expanduser(q)) as fp:
            questions += json.load(fp)
    return questions

def parse_question_json(json_questions):
    return [qst.RawQuestion.from_dict(q) for q in json_questions]
    
def create_quiz(questions, count, shuffle=True):
    # TODO: for efficiency it will be better to only parse
    # 'count' number of RawQuestion into DisplayQuestion
    quiz = [q.to_display_question() for q in questions]
    if shuffle:
        random.shuffle(quiz)
    return quiz[:count]

def render_quiz(quiz, template, text, solution, track_n, render, destination):
    extensions = {
        'latex': 'tex',
        'text': 'txt',
        'html': 'html'
    }
    ext = extensions.get(render, '')
    text_path = os.path.join(destination, f'{text}.{ext}')
    solution_path = os.path.join(destination, f'{solution}.{ext}')
    
    if render == 'latex':
        latex_render(quiz, template, text_path, solution_path, track_n)
    elif render == 'text':
        text_render(quiz, template, text_path, solution_path, track_n)
    elif render == 'html':
        html_render(quiz, 'template.html', text_path, solution_path, track_n)

if __name__ == "__main__":
    args = parse_arguments()

    # Load JSON file and convert to raw questions
    json_questions = load_questions(args)
    questions = parse_question_json(json_questions)
    # Adjust the number of question in the quiz
    max_number = args.n
    if max_number < 0 or max_number > len(questions):
        max_number = len(questions)

    random.seed(args.seed)
    
    for track in range(args.tracks):
        # Create quiz
        quiz = create_quiz(questions, max_number)
        # File naming and rendering
        out_file = args.output
        sol_file = args.solution
        if args.tracks > 1:
            out_file += f'_{track+1}'
            sol_file += f'_{track+1}'
        render_quiz(quiz, template_file, out_file,
            sol_file, track, args.render,
            os.path.expanduser(args.destination)
        )
        
