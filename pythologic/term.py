from functools import reduce

class Term:
    def __init__(self, predicate, *args):
        self.predicate = predicate
        self.args = list(args)

    def match(self, other):
        if isinstance(other, Term):
            if self.predicate != other.predicate or \
               len(self.args) != len(other.args):
                return None
            l = list(
                    map(
                        (lambda arg1, arg2: arg1.match(arg2)),
                        self.args,
                        other.args
                    )
            )
            return reduce(self.merge_bindings, [{}] + l)
        return other.match(self)

    def substitute(self, bindings):
        return Term(self.predicate, *map(
            (lambda arg: arg.substitute(bindings)),
            self.args
        ))

    def query(self, runtime):
        yield from runtime.execute(self)

    def __str__(self):
        if len(self.args) == 0:
            return f'{self.predicate}'
        args = ', '.join(map(str, self.args))
        return f'{self.predicate}({args})'

    def merge_bindings(self, b1, b2):
        if b1 is None or b2 is None:
            return None
        bindings = {**b1}
        for variable, value in b2.items():
            if variable in bindings:
                other = bindings[variable]
                sub = other.match(value)
                if sub is not None:
                    for var, val in sub.items():
                        bindings[var] = val
                else:
                    return None
            else:
                bindings[variable] = value
        return bindings

class TermTrue(Term):
    def __init__(self):
        super().__init__(TermTrue)

    def substitute(self, bindings):
        return self

    def query(self, runtime):
        yield self

class Conjunction(Term):
    def __init__(self, args):
        super().__init__(None, *args)

    def query(self, runtime):
        def solutions(index, bindings):
            if index >= len(self.args):
                yield self.substitute(bindings)
            else:
                arg = self.args[index]
                for item in runtime.execute(arg.substitute(bindings)):
                    unified = self.merge_bindings(
                        arg.match(item),
                        bindings
                    )
                    if unified is not None:
                        yield from solutions(index + 1, unified)
        yield from solutions(0, {})

    def substitute(self, bindings):
        return Conjunction(
            map(
                (lambda arg: arg.substitute(bindings)),
                self.args
            )
        )