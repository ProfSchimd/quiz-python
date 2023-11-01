"""Main module."""
import json
import random
import argparse
import os.path

import Question as qst
from rendering.latex_rendering import latex_render
from rendering.text_rendering import text_render
from rendering.html_rendering import html_render
from rendering.json_rendering import json_render
from util import get_similarity_matrix


def parse_arguments() -> argparse.Namespace:
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
    parser.add_argument('--template', dest='template', 
                        help="Indicates the template file")
    parser.add_argument('--test', dest='test', type=int,
                        default=0, help='Used for developing purpose')
    parser.add_argument('-v', '--verbosity', dest='verbosity', type=int,
                        default=0, help='Indicate the verbosity level (0, 1, 2) of output (default is 0)')
    return parser.parse_args()


def load_questions(input: str) -> list:
    """Loads questions from file, but doesn't randomize it. 
    
    This function contains the logic to open file(s), merge them
    (if multiple are indicated)."""
    question_files = input.split(',')
    questions = []
    for q in question_files:
        with open(os.path.expanduser(q)) as fp:
            questions += json.load(fp)
    return questions


def parse_question_json(json_questions: list) -> list:
    return [qst.RawQuestion.from_dict(q) for q in json_questions]
    

def create_quiz(questions: list, count: int, shuffle: bool=True) -> list:
    quiz = [q.to_display_question() for q in questions]
    if shuffle:
        random.shuffle(quiz)
    return quiz[:count]


def render_quiz(quiz: list, template:str, text: str, solution: str, track_n: int, render: str, destination: str):
    extensions = {
        'latex': 'tex',
        'text': 'txt',
        'html': 'html'
    }
    ext = extensions.get(render, '')
    text_path: str = os.path.join(destination, f'{text}.{ext}')
    solution_path: str = os.path.join(destination, f'{solution}.{ext}')
    template: str = template if template is not None else f'template.{ext}'
    
    if render.lower() == 'latex':
        latex_render(quiz, template, text_path, solution_path, track_n)
    elif render.lower() == 'text':
        text_render(quiz, template, text_path, solution_path, track_n)
    elif render.lower() == 'html':
        html_render(quiz, template, text_path, solution_path, track_n)
    elif render.lower() == 'json':
        json_render(quiz, template, text_path, solution_path, track_n)
        
def print_output(info: dict, verbosity: int):
    if verbosity == 0:
        return
    print(f'Input:  {len(info["files"])} file(s) {len(info["questions"])} question(s)')
    print(f'Seed:   {info["seed"]}')
    print(f'Tracks: {info["tracks"]}')
    print(f'Number: {info["number"]}')
    table = {
        "header": [],
        "weights": [],
        "questions": []
    }
    for i, quiz in enumerate(info["tests"]):
        table["header"].append(f"T{i}")
        table["weights"].append(f"W={sum([q._weight for q in quiz])}")
        table["questions"].append([f"{q.id} ({q._type[0].upper()}:{q._weight})" for q in quiz])
    print("".join([f"{t:^12}" for t in table["header"]]))
    print("".join([f"{t:^12}" for t in table["weights"]]))
    if verbosity > 1:
        # Print summary of questions with IDs
        for r in zip(*table["questions"]):
            print("".join([f"{t:^12}" for t in r]))
        # Print a similarity matrix
        matrix = get_similarity_matrix(info["tests"])
        n = len(info["tests"])
        print()
        print("    ", "".join([f" T{i:<4} " for i in range(n)]))
        for i in range(n):
            row = f"T{i:<3}"
            for j in range(n):
                row += f" {matrix[i][j]:^5.2} "
                
            print(row)
    
        
def main():
    args = parse_arguments()
    # This contains output information 
    info = {}

    # Load JSON file and convert to raw questions
    json_questions = load_questions(args.input)
    questions = parse_question_json(json_questions)
    # Adjust the number of question in the quiz
    max_number = args.n
    if max_number < 0 or max_number > len(questions):
        max_number = len(questions)

    # We always use a seed to allow reproducibility
    if args.seed is None:
        # Convert int to string to be consistent with the seed parameter
        args.seed = str(random.randint(0,2**30))
    random.seed(args.seed)
    info["files"] = args.input.split(",")
    info["questions"] = questions
    info["seed"] = args.seed
    info["tracks"] = args.tracks
    info["number"] = max_number
    info["tests"] = []
    
    for track in range(args.tracks):
        # Create quiz
        quiz = create_quiz(questions, max_number)
        info["tests"].append(quiz)
        # File naming and rendering
        out_file = args.output
        sol_file = args.solution
        if args.tracks > 1:
            out_file += f'_{track}'
            sol_file += f'_{track}'
        render_quiz(quiz, args.template, out_file,
            sol_file, track, args.render,
            os.path.expanduser(args.destination)
        )
        
    print_output(info, args.verbosity)


if __name__ == "__main__":
    main()        
