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
* a `correct` array which contains `0` for options not to be chcked and `1` for the
options to be checked (in `invertible` type questions this relation is reversed for the "inverted" questions)
* a `weight` number representing the weight of the answer in the final score computation (used only for automatic evaluation).

