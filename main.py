from pyfiglet import Figlet, figlet_format
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)
import os
import re
import click
import six

try:
    import colorama

    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


def print_banner():
    log("Healthy CLI", color="cyan", figlet=True)


def colorize():
    return style_from_dict({
        Token.QuestionMark: '#fac731 bold',
        Token.Answer: '#4688f1 bold',
        Token.Instruction: '',  # default
        Token.Separator: '#cc5454',
        Token.Selected: '#0abf5b',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Question: '',
    })


def log(string, color, font="banner3-D", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


def ask_questions(style):
    questions = [
        {
            'type': 'list',
            'name': 'starting_position',
            'message': 'Starting Position:',
            'choices': ['Kneeling', 'Sitting', 'Standing'],
            'filter': lambda val: val.lower()
        }
    ]
    answers = prompt(questions, style=style)
    return answers


@click.command()
def main():
    """
    Healthy CLI is a command line utility to help you get healthier while coding.
    Helping you take care of your body, so you can avoid chronic issues from coding.
    """
    style = colorize()
    print_banner()
    log("Welcome to Healthy CLI", "green")
    answers = ask_questions(style)
    log("Starting Position: " + answers.get('starting_position'), "cyan")


if __name__ == '__main__':
    main()

