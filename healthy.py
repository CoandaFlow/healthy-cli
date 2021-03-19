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
#from playsound import playsound
import pygame
import threading


# TODO: give shotout to pygame in credits if this is useful
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()
pygame.mixer.init()



# no window controls
import pyautogui

# is able to list window titles, and sometimes bring window to front, but also fails with 'Unknown error'
#import win32gui

# def windowEnumerationHandler(hwnd, top_windows):
#     top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
#
# def show_window():
#     top_windows = []
#     win32gui.EnumWindows(windowEnumerationHandler, top_windows)
#     for i in top_windows:
#         # print("window title:", i[1])
#         if "powershell" in i[1].lower():
#             print(i)
#             win32gui.ShowWindow(i[0], 5)
#             win32gui.SetForegroundWindow(i[0])
#             break

# fails with runtime error
# TypeError: item 2 in _argtypes_ passes a union by value, which is unsupported.
# from pywinauto.application import Application
# def show_window():
#     app = Application(backend="uia").start("notepad.exe")
#     app.UntitledNotepad.menu_select("Help->About Notepad")
#     app.AboutNotepad.OK.click()
#     app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces=True)

# fails with runtime error at startup
# KeyError: (<class 'ctypes.HRESULT'>, (<class 'comtypes.automation.tagVARIANT'>, <class 'comtypes.LP_POINTER(IDispatch)'>), 0)
# from pywinauto.findwindows    import find_window
# from pywinauto.win32functions import SetFocus

# fails with no module named pywin32, even though with venv active and pip install pywin32 indicates 'requirement already satisfied'
# need to track down these imports, think there was a module name change
# from pywin32 import win32gui
# from pywin32 import win32process
# from pywin32 import win32api
from win10toast import ToastNotifier
def show_window(message):

    toaster = ToastNotifier()
    toaster.show_toast("Healthy-CLI", message)
    # window = find_window(title='powershell.exe')
    # SetFocus(window)
    # fgwin = win32gui.GetForegroundWindow()
    # fg = win32process.GetWindowThreadProcessId(fgwin)[0]
    # current = win32api.GetCurrentThreadId()
    # if current != fg:
    #     win32process.AttachThreadInput(fg, current, True)
    #     win32gui.SetForegroundWindow(self.hwnd)
    #     win32process.AttachThreadInput(fg, win32api.GetCurrentThreadId(), False)


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
    os.system('cls' if os.name == 'nt' else 'clear')
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
            'message': 'Are you testing healthy cli (I\'ll treat minutes as quarter seconds)?'
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


def playsound(thepath, test_mode=False, wait_for_sound=False):
    sound = pygame.mixer.Sound(thepath)
    sound.set_volume(0.7)   # Now plays at 90% of full volume.
    seconds_to_wait = 1
    if test_mode:
        seconds_to_wait = .25
    clip_length = int(seconds_to_wait * 8)
    clip_fade_out = clip_length - (1.5 * seconds_to_wait)
    clip_length_ms = clip_length * 1000
    clip_fade_out_ms = clip_fade_out * 1000
    sound.play(0, clip_length_ms, 1500)

    timer = threading.Timer(clip_fade_out, fade_out_sound, [sound])
    timer.start()
    if wait_for_sound:
        time.sleep(clip_length)


def fade_out_sound(sound):
    sound.fadeout(1500)


def show_interval_progress(starting_position, interval_minutes, test_mode):
    seconds_to_wait = 60
    if test_mode:
        seconds_to_wait = .25
    bar = Bar(starting_position, max=interval_minutes)
    for i in range(interval_minutes):
        time.sleep(seconds_to_wait)
        bar.next()
    bar.finish()
    # TODO: These seem like they are a little loud, compared to my zoom call volumes,
    #  normalize audio levels or see if the API supports playing at a lower volume
    playsound('sounds/' + SOUNDS[random.randint(0, 4)], test_mode)


def wait_and_ask(style, position, interval_minutes, include_movement_break=True, test_mode=False):
    show_interval_progress(f'{position} minutes', interval_minutes, test_mode)
    show_window('time to move')
    if include_movement_break:
        show_interval_progress('5 minute movement break', 5, test_mode)
        show_window('nice movement, you\'ve reached 5 minutes')
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
    playsound('sounds/' + SOUNDS[0], False, False)
    log("Welcome to Healthy CLI", "green")
    answers = ask_questions(style)
    test_mode = answers.get('testing')
    starting_position = answers.get('starting_position')
    starting_interval = answers.get('interval')
    if starting_interval is None:
        exit(1)
    else:
        starting_interval_minutes = int(answers.get('interval')[0:2])
    log(f"Starting Position: {starting_position}, switching every {starting_interval_minutes} minutes", "cyan")
    new_position = starting_position
    include_movement_break = True
    interval_minutes = starting_interval_minutes

    while True:
        repeat, new_position = wait_and_ask(style, new_position, interval_minutes, include_movement_break, test_mode)
        if repeat == 'call it a wrap':
            log("Goodbye", "green")
            exit(0)
        elif repeat == 'Show me stats':
            log("stats coming soon", "yellow")
            interval_minutes = starting_interval_minutes
        elif repeat == 'lunch break':
            interval_minutes = 60
            new_position = 'lunch time'
        elif repeat == 'yes':
            interval_minutes = starting_interval_minutes
        else:
            exit(1)


if __name__ == '__main__':
    main()

