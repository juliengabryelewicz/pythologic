import argparse
import os
import sys
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pathlib import Path
from parser import Parser
from lexer import lexer
from runtime import Runtime

def main():
    ap = argparse.ArgumentParser(
        prog='pythologic',
        usage='%(prog)s [options]',
        description='Pythologic'
    )
    ap.add_argument(
        '-f', 
        '--file',
        type=str,
        help='Path to Prolog file'
    )

    args = ap.parse_args()
    input_file = args.file
    rules_text = ''
    runtime = Runtime([])
    if input_file is not None:
        try:
            with open(input_file) as reader:
                line = reader.readline()
                while line != '':
                    rules_text += line
                    line = reader.readline()
            rules = Parser(lexer(rules_text)).parse_rules()
            runtime = Runtime(rules)
        except Exception as e:
            print(f'Error while loading rules: {str(e)}')
            sys.exit()

    print('\nPythologic')
    print('quit : Ctrl+c')
    try:
        while True:
            query = prompt(
                '>>> ',
                history=FileHistory(os.path.join(str(Path.home()), '.pythologic_history')),
                auto_suggest=AutoSuggestFromHistory()
            )
            try:
                goal = Parser(lexer(query)).parse_terms()
                for index, item in enumerate(runtime.execute(goal)):
                    print(item)
            except Exception as e:
                print('Error: {str(e)}')
    except KeyboardInterrupt:
        print('\nExiting...')

if __name__ == '__main__':
    main()