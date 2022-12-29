# Development

This document contains some information and ideas about the development of the
software. It should be considered an *internal* documents containing indications
for the developer(s).

## Some changes to the code architecture

* Isolate the randomization algorithm, the idea is to randomize questions first
and then apply rendering on a "deterministic" list of questions.

## The `Question` class

It may be useful to create a class containing information about a question, if
needed the class could be extended to specialize for various type of questions.
The class could be useful as a way of isolating the concept of question from its
rendering. Once this isolation is achieved, adding new rendering methods (*i.e.*,
new output formats) should be easier.

## Rendering improvements

* Using regular expression to perform the rendering may give a better way of
implementing rendering algorithms.