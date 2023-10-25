import re
from term import Conjunction, Term, TermTrue
from rule import Rule
from variable import Variable

class Parser:
    def __init__(self, tokens):
        self._current = ''
        self._scope = {}
        self._tokens = tokens
        self._done = False
        self._next()

    def _next(self):
        try:
            next_token = next(self._tokens)
            self._current = next_token
        except StopIteration:
            self._done = True

    def parse_rules(self):
        rules = []
        while not self._done:
            self._scope = {}
            rules.append(self._parse_rule())
        return rules

    def parse_terms(self):
        self._scope = {}
        return self._parse_term()


    def _parse_atom(self):
        name = self._current
        if re.match(r"^[A-Za-z0-9_]+$", name) is None:
            raise Exception(f'Wrong atom name: {name}')
        self._next()
        return name

    def _parse_term(self):
        if self._current == '(':
            self._next()
            args = []
            while self._current != ')':
                args.append(self._parse_term())
                if self._current != ',' and self._current != ')':
                    raise Exception(
                        f'Expecter , or ) in term, got {self._current} instead')
                if self._current == ',':
                    self._next()
            self._next()
            return Conjunction(args)
        predicate = self._parse_atom()
        if re.match(r"^[A-Z_][A-Za-z0-9_]*$", predicate) is not None:
            if predicate == '_':
                return Variable('_')
            variable = self._scope.get(predicate, None)
            if variable is None:
                variable = Variable(predicate)
                self._scope[predicate] = variable
            return variable
        if self._current != '(':
            return Term(predicate)
        self._next()
        args = []
        while self._current != ')':
            args.append(self._parse_term())
            if self._current != ',' and self._current != ')':
                raise Exception(
                    f'Expected , or ) in term, got {self._current} instead')
            if self._current == ',':
                self._next()
        self._next()
        return Term(predicate, *args)

    def _parse_rule(self):
        head = self._parse_term()
        if self._current == '.':
            self._next()
            return Rule(head, TermTrue())
        if self._current != ':-':
            raise Exception(f'Expected :- in rule, got {self._current} instead')
        self._next()
        args = []
        while self._current != '.':
            args.append(self._parse_term())
            if self._current != ',' and self._current != '.':
                raise Exception(
                    f'Expected , or ) in term, got {self._current} instead')
            if self._current == ',':
                self._next()
        self._next()
        tail = None
        if len(args) == 1:
            tail = args[0]
        else:
            tail = Conjunction(args)
        return Rule(head, tail)
