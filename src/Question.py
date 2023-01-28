import random

"""Module containing all Question classes."""
class Question:
    """Contains basic feature of a Question."""

    def __init__(self, id, text, weight):
        """Initialize Question."""
        self.id = id
        self._text = text
        self._weight = weight
        self._tags = []
        self._type = 'undefined'


    def __str__(self):
        return f'ID: {self.id} (W: {self._weight})'
 

class DisplayQuestion(Question):
    """DisplayQuestion are those rendered."""


class CheckboxQuestion(DisplayQuestion):
    def __init__(self, id, text, weight, options = [], correct = [], type = None):
        super().__init__(id, text, weight)
        self._options = options
        self._correct = correct
        if type is not None:
            self._type = type

class FillQuestion(DisplayQuestion):
    def __init__(self, id, text, to_fill, weight, correct = [], type = None):
        super().__init__(id, text, weight)
        self._correct = correct
        self._to_fill = to_fill
        if type is not None:
            self._type = type

class OpenQuestion(DisplayQuestion):
    def __init__(self, id, text, weight, variants):
        super().__init__(id, text, weight)
        self._variants = variants

class RawQuestion(Question):
    """Represents (meta) questions before instantiation randomization and substitution."""

    def __init__(self, id, text, weight):
        """Initialize RawQuestion."""
        super().__init__(id, text, weight)

    def to_display_question(self, seed=None):
        return DisplayQuestion(self.id, self._text, self._weight)

    def __str__(self):
        return f'[{self.id}] ({self._type} {self.__class__.__name__})'

    @classmethod
    def from_dict(cls, d):
        if d['type'] in ['single', 'multiple', 'invertible', 'multi-variate']:
            return RawChoiceQuestion.from_dict(d)
        elif d['type'] == 'fill':
            return RawFillQuestion.from_dict(d)
        return cls(d['id'], d['text'], d['weight'])
        

class RawChoiceQuestion(RawQuestion):
    def __init__(self, id, text, weight, options, correct, type='single'):
        super().__init__(id, text, weight)
        self._options = options
        self._correct = correct
        self._type = type

    def to_display_question(self, seed=None):
        if seed is None:
            random.seed(seed)
        text = None
        # Choose between versions (single -> 1, multiple -> 1, invertible -> 2, ...)
        variant = random.randint(0,len(self._text)-1)
        text = self._text[variant]
        n = len(self._options)
        # randomize options and correct
        indexes = list(range(n))
        random.shuffle(indexes)
        options = [self._options[i] for i in indexes]
        correct = [self._correct[variant][i] for i in indexes]
        return CheckboxQuestion(self.id, text, self._weight, options, correct, self._type)

    @classmethod
    def from_dict(cls, d):
        """Construct RaChoiceQuestion from a dictionary.
        
        The dictionary should have the exact same structure as the JSON file."""
        text = None
        correct = None
        if d['type'] == 'single' or d['type'] == 'multiple':
            text = [d['text']]
            correct = [d['correct']]
        elif d['type'] == 'invertible':
            text = d['text']
            correct =  [
                d['correct'], 
                [1-x for x in d['correct']]
            ]
        elif d['type'] == 'multi-variate':
            text = d['text']
            correct = d['correct']
        return cls(d['id'], text, d['weight'], d['options'], correct, d['type'])
        

class RawFillQuestion(RawQuestion):
    def __init__(self, id, text, weight, to_fill, correct, type):
        super().__init__(id, text, weight)
        self._to_fill = to_fill
        self._correct = correct
        self._type = type

    def to_display_question(self, seed=None):
        return FillQuestion(self.id, self._text, self._to_fill, self._weight, self._correct, self._type)

    @classmethod
    def from_dict(cls, d):
        return cls(d['id'], d['text'], d['weight'], d['tofill'], d['correct'], d['type'])

class RawOpenQuestion(RawQuestion):
    pass

class RawCompositeQuestion(RawQuestion):
    pass