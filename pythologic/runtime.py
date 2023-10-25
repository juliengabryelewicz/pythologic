class Runtime:
    def __init__(self, rules):
        self.rules = rules

    def execute(self, goal):
        for rule in self.rules:
            match = rule.head.match(goal)
            if match is not None:
                head = rule.head.substitute(match)
                tail = rule.tail.substitute(match)
                for item in tail.query(self):
                    yield head.substitute(tail.match(item))