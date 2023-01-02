# Quiz Python

A Python program to generate randomized tests from input `json` questions.
Current output format is LaTeX, which can be compiled into pdf. The program
outputs both the text and the solution files.

* [Json format](#json-format)
* [Planned features](#planned-features)
* [Prerequisites](#prerequisites)
* [Examples](#examples)

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
* Optional seeding for replication of tests
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
* Refactoring with Question class (see `dev.md`)
* Add an option `--template` for custom templates

### Completed features
* ~~Create several version with `--tracks` options (default being 1)~~
* ~~All English help text~~
* ~~Add options `--output` for output names~~
* ~~Support multiple input files `--input a.json,b.json,c.json`~~

## Prerequisites

Currently, the code uses only features from standard Python packages: `random`, `json`, `argparse`.

## Synopsis

```
usage: py-quiz.py [-h] [--number N] [--input INPUT] [--output OUTPUT] [--solution SOLUTION] [--tracks TRACKS]

Generate random quiz from input JSON files.

options:
  -h, --help           show this help message and exit
  --number N           Number of questions, if -1 (default) use all
  --input INPUT        Comma separated list of JSON file(s) with questions
  --output OUTPUT      Name of the output (text) file, without extension
  --solution SOLUTION  Name of the output (solution) file, without extension
  --tracks TRACKS      Number of tracks (default 1)
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

Specifies input (`in.json`) and text (`out.tex`) and solution (`sol.tex`) output files
```
$ python py-quiz --input in.json --output out.tex --solution sol.tex
```
---

Specifies the maximum number (`10`) of questions taken from `questions.json` in the output `out.tex`
```
python py-quiz.py --number 10

