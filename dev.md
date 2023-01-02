# Development

This document contains some information and ideas about the development of the
software. It should be considered an *internal* document, containing indications
for developer(s) only.

## Some changes to the code architecture

* Isolate the randomization algorithm, the idea is to randomize questions first
and then apply rendering on a "deterministic" list of questions. This should
ease the process of supporting more output formats.

## The `Question` class

It may be useful to create a class containing informations about a question, if
needed the class could be extended and specialized into various type of questions.
The class could be useful as a way of isolating the concept of question from its
rendering. Once this isolation is achieved, adding new rendering methods (*i.e.*,
supportin more output formats) should be easier.

## Rendering improvements

* Using regular expression to perform the rendering may give a better way of
implementing rendering algorithms.