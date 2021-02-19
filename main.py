from pyfiglet import Figlet, figlet_format
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)
import os
import re
import random
import click
import six
import time
from progress.bar import Bar
from playsound import playsound
# fails with runtime error
# from pywinauto.application import Application

# no window controls
#import pyautogui


SOUNDS = [
    'EarlyRiser.mp3',
    'SlowMorning.mp3',
    'Freshstart.mp3',
    'Auratone.mp3',
    'Softchime.mp3'
]

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
            'type': 'confirm',
            'name': 'testing',
            'message': 'Are you testing healthy cli (I\'ll treat minutes as seconds)?'
        },
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
            'choices': ['05 minutes', '25 minutes', '20 minutes'],
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
        },
        {
            'type': 'list',
            'name': 'new_position',
            'message': 'Which position are you changing to?',
            'choices': ['Sitting', 'Standing', 'Kneeling'],
            'filter': lambda val: val.lower(),
            'when': lambda ans: ans.get('repeat') == 'yes',
            'default': 'Standing'
        }
    ]
    answers = prompt(questions, style=style)
    return answers


def show_interval_progress(starting_position, interval_minutes, test_mode):
    seconds_to_wait = 60
    if test_mode:
        seconds_to_wait = 1
    bar = Bar(starting_position, max=interval_minutes)
    for i in range(interval_minutes):
        time.sleep(seconds_to_wait)
        bar.next()
    bar.finish()
    playsound('sounds/' + SOUNDS[random.randint(0, 4)])


def wait_and_ask(style, position, interval_minutes, include_movement_break=True, test_mode=False):
    show_interval_progress(f'{position} minutes', interval_minutes, test_mode)
    if include_movement_break:
        show_interval_progress('5 minutes movement break', 5, test_mode)
        # TODO: suggestion a new kind of movement each loop
    loop_answers = ask_loop_questions(style)
    return loop_answers.get('repeat'), loop_answers.get('new_position')


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
    test_mode = answers.get('testing')
    starting_position = answers.get('starting_position')
    interval_minutes = int(answers.get('interval')[0:2])
    log(f"Starting Position: {starting_position}, switching every {interval_minutes} minutes", "cyan")
    new_position = starting_position
    include_movement_break = True

    while True:
        repeat, new_position = wait_and_ask(style, new_position, interval_minutes, include_movement_break, test_mode)
        if repeat == 'call it a wrap':
            log("Goodbye", "green")
            exit(0)
        elif repeat == 'Show me stats':
            log("stats coming soon", "yellow")
        elif repeat == 'lunch break':
            interval_minutes = 60
            new_position = 'lunch time'


if __name__ == '__main__':
    main()

