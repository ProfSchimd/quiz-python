# Development

This document contains some information and ideas about the development of the
software. It should be considered an *internal* document, containing indications
for developer(s) only.

## Some changes to the code architecture

* Isolate the randomization algorithm, the idea is to randomize questions first
and then apply rendering on a "deterministic" list of questions. This should
ease the process of supporting more output formats.

## The `Question` class

It may be useful to create a class containing information about a question, if
needed the class could be extended and specialized into various type of questions.
The class could be useful as a way of isolating the concept of question from its
rendering. Once this isolation is achieved, adding new rendering methods (*i.e.*,
supporting more output formats) should be easier.

## Rendering improvements

* Using regular expression to perform the rendering may give a better way of
implementing rendering algorithms.

## Overall functioning
The software operates in three phases.

1. Input *parsing*: input `JSON`'s are read and, if needed, filtered, resulting in a
list of `RawQuestion` objects.
2. Assessment *building*: the list of `RawQuestion` sampled, if needed, the options
and variants of the questions are randomized, any constraint (*e.g.*, total score)
is also enforced in this phase. The result is a list of `DisplayQuestion`.
3. Assessment *rendering*: the list of `DisplayQuestion` is parsed and each question
is rendered into the output file(s) according to the given parameters.