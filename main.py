from pyfiglet import Figlet, figlet_format
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)
import os
import re
import click
import six
import time
from progress.bar import Bar

TEST_MODE = True

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
            'message': 'Which position are you starting in?',
            'choices': ['Sitting', 'Standing', 'Kneeling'],
            'filter': lambda val: val.lower(),
            'default': 'Sitting'
        },
        {
            'type': 'list',
            'name': 'interval',
            'message': 'How often do you want to switch positions?',
            'choices': ['25 minutes', '20 minutes'],
            'filter': lambda val: val.lower(),
            'default': '25 minutes'
        }
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_loop_questions(style):
    questions = [
        {
            'type': 'list',
            'name': 'repeat',
            'message': 'Would you like to go again?',
            'choices': ['Yes', 'Lunch break', 'Show me stats', 'Call it a wrap'],
            'filter': lambda val: val.lower(),
            'default': 'Yes'
        }
    ]
    answers = prompt(questions, style=style)
    # TODO: See how to cascade ask which position if Yes to repeat question
    return answers


def show_interval_progress(starting_position, interval_minutes):
    seconds_to_wait = 60
    if TEST_MODE:
        seconds_to_wait = 1
    bar = Bar(starting_position, max=interval_minutes)
    for i in range(interval_minutes):
        time.sleep(seconds_to_wait)
        bar.next()
    bar.finish()


def wait_and_ask(style, position, interval_minutes):
    show_interval_progress(position, interval_minutes)
    show_interval_progress('5 minutes movement break', 5)  # TODO: suggestion a new kind of movement each loop
    loop_answers = ask_loop_questions(style)
    return loop_answers


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
    starting_position = answers.get('starting_position')
    interval_minutes = int(answers.get('interval')[0:2])
    log(f"Starting Position: {starting_position}, switching every {interval_minutes} minutes", "cyan")
    initial_loop_answers = wait_and_ask(style, starting_position, interval_minutes)
    repeat = initial_loop_answers.get('repeat')
    while repeat == 'yes':
        loop_answers = wait_and_ask(style, starting_position, interval_minutes)
        repeat = loop_answers.get('repeat')


if __name__ == '__main__':
    main()

