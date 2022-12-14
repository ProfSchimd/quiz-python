# Quiz Python

A Python program to generate randomized tests from input `json` questions.
Current output format is LaTeX, which can be compiled into pdf. The program
outputs both text and solution files.

## Json format

The Json file for questions is an array of objects, each object should
contain:
* an `id` to identify the question (preferably a string);
* a string `type` which must be one of `single`, `multiple`, `invertible`, `fill`;
* a `text` string containing the text of the question, for `invertible` questions
this is an array with two strings the for normal and inverted version
* an `options` which is an array containing the options to be displayed (ignored in `fill` questions);
* a `correct` array which contains `0` for options not to be checked and `1` for the
options to be checked (in `invertible` type questions this relation is reversed for the "inverted" questions)
* a `weight` number representing the weight of the answer in the final score computation (used only for automatic evaluation).

## Next features
* Create several version with `--versions` options (default being 1)
* ~~Add options `--output` for output names~~
* Add more type of questions
    * Ordered options: asks student to assign an order from `1` to `n` to the `n` options
    * Multi-Multiple: like `multiple`, but has several versions (similar to `invertible` but allowing even more than two versions)
* Allow tha definition of the number of quiz for any type and/or define the number of quiz for each weight
* Optional seeding for replication of tests
* Integrate external service like [YToTech](https://latex.ytotech.com/), see documentation
[here](https://github.com/YtoTech/latex-on-http)

## Prerequisites

Currently, the code uses only features from standard Python packages: `random`, `json`, `argparse`.

