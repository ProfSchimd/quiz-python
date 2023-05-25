# Quiz Python

A Python program to generate randomized tests from input `json` questions.
Current output format is LaTeX, which can be compiled into pdf. The program
outputs both the text and the solution files.

- [Quiz Python](#quiz-python)
  - [Json format](#json-format)
  - [Planned features](#planned-features)
    - [Completed features](#completed-features)
  - [Prerequisites](#prerequisites)
  - [Synopsis](#synopsis)
  - [Examples](#examples)

## Json format

The Json file for questions is an array of objects, each object should
contain:
* an `id` to identify the question (preferably a string);
* a string `type` which must be one of `single`, `multiple`, `invertible`, `fill`;
* a `text` string containing the text of the question, for `invertible` questions
this is an array with two strings the for normal and inverted version
* an `options` which is an array containing the options to be displayed (ignored in `fill` questions);
* a `tofill` which contains the text with placeholders `{{#}}` for gaps to be filled (ignored in non-`fill` questions);
* a `correct` array which contains `0` for options not to be checked and `1` for the
options to be checked (in `invertible` type questions this relation is reversed for the "inverted" questions)
* a `weight` number representing the weight of the answer in the final score computation (used only for automatic evaluation).

## Planned features
* Add a `--no-random` option that disable randomization
* Add a `--save file.json` option to save in `JSON` format the questions used (multiple file if
`--tracks` is greater than one)
* Add more type of questions
    * Ordered options: asks student to assign an order from `1` to `n` to the `n` options
    * Multi-Multiple: like `multiple`, but has several versions (similar to `invertible` but allowing even more than two versions)
* Allow the definition of the number of quiz for any type/file and/or define the number of quiz for each weight
* Integrate external service like [YToTech](https://latex.ytotech.com/), see documentation
[here](https://github.com/YtoTech/latex-on-http)
* Support different backends: TeX, pdf, txt, docx, ...

### Completed features
* ~~Optional seeding for replication of tests~~
* * ~~Refactoring with Question class (see `dev.md`)~~
* ~~Add an option `--template` for custom templates~~
* ~~Create several version with `--tracks` options (default being 1)~~
* ~~All English help text~~
* ~~Add options `--output` for output names~~
* ~~Support multiple input files `--input a.json,b.json,c.json`~~

## Prerequisites

Currently, the code uses only features from standard Python packages: `random`, `json`, `argparse`.

The backend uses [FastAPI](https://fastapi.tiangolo.com/), it is best run in development environment with [uvicorn](https://www.uvicorn.org/), see also [requirements.txt](./requirements.txt).

## Synopsis

```
usage: py-quiz.py [-h] [--number N] [--input INPUT] [--output OUTPUT]
                  [--solution SOLUTION] [--destination DESTINATION]
                  [--tracks TRACKS] [--seed SEED] [--render RENDER]
                  [--template TEMPLATE] [--test TEST] [-v VERBOSITY]

Generate random quiz from input JSON files.

options:
  -h, --help            show this help message and exit
  --number N            Number of questions, if -1 (default) use all
  --input INPUT         Comma separated list of JSON file(s) with questions
  --output OUTPUT       Name of the output (text) file, without extension
  --solution SOLUTION   Name of the output (solution) file, without extension
  --destination DESTINATION
                        Directory where the output files will be put
  --tracks TRACKS       Number of tracks (default 1)
  --seed SEED           Integer value for seeding randomization (default is no
                        seeding)
  --render RENDER       Defines the rendering type: latex, text (default is
                        latex)
  --template TEMPLATE   Indicates the template file
  --test TEST           Used for developing purpose
  -v VERBOSITY, --verbosity VERBOSITY
                        Indicate the verbosity level (0, 1, 2) of output
                        (default is 0)
```

## Examples

Create a single test (`text.tex`) with solution (`solution.tex`) using questions from the file `questions.json`
using all questions present on the file.

```
$ python py-quiz.py
```
---

Specifies input file `in.json`
```
$ python py-quiz --input in.json
```
---

Specifies multiple input files `in1.json`, `in2.json`, `in3.json` (pay attention
to the format, **do not** put whitespaces in the list and separete with commas)
```
$ python py-quiz --input in1.json,in2.json,in3.json
```
---

Specifies input (`in.json`), text (`out.tex`), and solution (`sol.tex`) output files
```
$ python py-quiz --input in.json --output out.tex --solution sol.tex
```
---

Specifies the maximum number (`10`) of questions taken from `questions.json` in the output `out.tex`
```
python py-quiz.py --number 10

## Backend (experimental)
The *backend* will be the preferred way to access `quiz-python` APIs, currently it is under development and can only be tested with sample API. 

To run the backend app on the port 8888 (leaving out `--port` uses default port which is 8000)

```console
uvicorn runserver:app --reload --port 8888
```

**It is important to move to the `src/` directory before running the command.**

