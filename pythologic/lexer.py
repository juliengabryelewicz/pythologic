import re

def lexer(text):
    matches = re.findall(r"[A-Za-z0-9_]+|:\-|[()\.,]", text)

    for token in matches:
        yield token