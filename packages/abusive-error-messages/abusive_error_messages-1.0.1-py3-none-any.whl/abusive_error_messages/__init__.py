__version__ = "1.0.1"

import sys
from random import choice, randint
from rich import print

"""
From https://docs.python.org/3/library/exceptions.html#exception-hierarchy:

BaseException
 ├── BaseExceptionGroup
 ├── GeneratorExit
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ExceptionGroup [BaseExceptionGroup]
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    ├── NotImplementedError
      │    └── RecursionError
      ├── StopAsyncIteration
      ├── StopIteration
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning
           ├── BytesWarning
           ├── DeprecationWarning
           ├── EncodingWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── PendingDeprecationWarning
           ├── ResourceWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UnicodeWarning
           └── UserWarning
"""

traceback_msgs = [
    'Find the error yourself, why do I have to do everything?',
    'You don\'t deserve a traceback. You made the error, [bold]YOU[/bold] find it',
    "Why do [italic]I[/] have to do everything for you?",
    "Whaaa, wittle baby progammer needs his twaceback. Toughen up, wuss",
]


misc_error_msgs = [
    "Wow, that's a hard error to get, what'd you do to screw up [italic]THAT[/] badly??",
    'I can\'t be bothered',
    'Eh, whatever',
    'This is [bold]your[/] fault.'
]

# Credit: XKCD - https://www.explainxkcd.com/wiki/index.php/Category:Code_Quality
xkcd = (
    "Wow. This is like being in a house built by a child using nothing but a hatchet and a picture of a house.",
    "It's like a salad recipe written by a corporate lawyer using a phone autocorrect that only knew Excel formulas.",
    "It's like someone took a transcript of a couple arguing at IKEA and made random edits until it compiled without errors.",
    "It's like you ran OCR on a photo of a Scrabble board from a game where Javascript reserved words counted for triple points.",
    "It looks like someone transcribed a naval weather forecast while woodpeckers hammered their shift keys, then randomly indented it.",
    "It's like an E E Cummings poem written using only the usernames a website suggests when the one you want is taken.",
    "This looks like the output of a Markov bot that's been fed bus timetables from a city where the buses crash constantly.",
    "Your code looks like song lyrics written using only the stuff that comes after the question mark in a URL.",
    'It\'s like a JSON table of model numbers for flashlights with "tactical" in their names.',
    "Like you read Turing's 1936 paper on computing and a page of JavaScript example code and guessed at everything in between.",
    "It's like a leet-speak translation of a manifesto by a survivalist cult leader who's for some reason obsessed with memory allocation.",
    "It looks like a spreadsheet formula which assembles a Haskell function for parsing HTML.",
)

general_insults = (
    "Figure it out yourself",
    "Wow, you suck at coding",
    "Your code sucks and so do you",
    "Who taught you to program, your mom?",
    # "Geez, can't you code?",
    "Gosh, I bet you dip your Oreos in water because your dad never came back with the milk",
)


replacements = {
# BaseException
#  ├── BaseExceptionGroup
    GeneratorExit: ("Don't use generators if you don't know what you're doing", 'The "yeild" keyword is called that for a reason.'),
    KeyboardInterrupt: ("What the heck, I was [italic]running[/]", "Hey, I'm runnin' heare!", "[bold]OOf", "Ouch! What the crap?!", "You suck"),
    SystemExit: ("[italic]*ack*[/] I'm dyyyyingggggggg....", "[bold italic]GOODBYE CRUEL WORLD"),
    Exception: ("Oh, so someone [italic]else's[/] code messed up",) + general_insults,
    SyntaxError: general_insults,
    ArithmeticError: "Gosh, can't you do math?",
    # FloatingPointError
    OverflowError: "Your mama's so fat, even [bold]she[/] couldn't fit in that number",
    ZeroDivisionError: ('Gosh, you suck at math.', 'Something just broke inside me', 'What are you doing, that doesn\'t even make [italic]sense[/]'),
    AssertionError: ("Can't you do anything right?",) + general_insults,
    AttributeError: ("You didn't read the docs, did you", "Do you even know what that is?"),
    # BufferError
    EOFError: "That file was so fed up with your crap it committed suicide to get away from you",
    # ExceptionGroup: "Oh my gosh, what did you do that was [italic]so[/] that [bold]multiple[/] errors need to be raised just to describe it properly??",
    ImportError: "Don't worry, it's probably someone else's code that broke. I'm sure once you fix their code for them, yours will break too",
    ModuleNotFoundError: ("That's not a module, moron",) + general_insults,
    # LookupError:
    IndexError: ("Bad index, idiot",) + general_insults,
    KeyError: ("That's not a key! What are you [italic]doing[/]?",) + general_insults,
    MemoryError: "Gosh, you messed up. I'd help you with that, but I can't remember... ",
    NameError:         ("That's not a variable, idiot", "Can't you remember what you [italic]just[/] typed?") + general_insults,
    UnboundLocalError: ("That's not a variable, idiot", "Can't you remember what you [italic]just[/] typed?") + general_insults,
    OSError: ("Stop abusing the operating system! He an I are friends."),
    BlockingIOError: ("Don't touch that, that's not yours yet"),
    ChildProcessError: ("Your child died. He got kidnapped and tortured to death. You should have protected him."),
    ConnectionError: ("Nobody wants to date you"),
    # BrokenPipeError: (""),
    # ConnectionAbortedError: (""),
    # ConnectionRefusedError: (""),
    # ConnectionResetError: (""),
    FileExistsError: ("That file already exists, idiot, pick a different one"),
    FileNotFoundError: ("That file doesn't exist, did you [italic]think[/] it did??"),
    InterruptedError: ("God said no."),
    IsADirectoryError: ("That's a directory, stop that! Don't touch that!", "You can't be trusted with that power."),
    NotADirectoryError: ("That's a directory, what are you [italic]doing[/]?"),
    PermissionError: ("I'm calling the cops",  "Whaaat? There's nothing [italic]there[/]. Don't worry about it."),
    # ProcessLookupError: (""),
    TimeoutError: ("You took too long"),
    # ReferenceError: (""),
    RuntimeError: ("Gosh, you suck at programming"),
    NotImplementedError: ("That doesn't exist, cause [bold]you[/] didn't bother to do it!"),
    RecursionError: ("Maybe if you tried just a few more times, it might work", ""),
    # StopAsyncIteration: (""),
    # StopIteration: (""),
    IndentationError: ("You suck at scopes. Maybe try an easier programming language, like Scratch"),
    TabError: ("Ha! You're screwed.", "Try using an [italic]IDE[/]"),
    SystemError: ("Ohhh boy, you're screwed"),
    TypeError: ("If you can't manage types, try a staticly typed language like TypeScript or C++"),
    ValueError: ("If you can't do things right, stop doing them",) + general_insults,
    UnicodeError: ("Ha ha, you tried to use emojis"),
    # UnicodeDecodeError
    # UnicodeEncodeError
    # UnicodeTranslateError
    Warning: ("If you're not gonna give a real error, don't even try", "If you're gonna raise an error, you gotta [italic]commit[/]"),
    # BytesWarning
    DeprecationWarning: ("Update your freakin' dependancies", "Your code is probably hackable"),
    # EncodingWarning: (""),
    # FutureWarning: (""),
    ImportWarning: ("Fix yo imports"),
    PendingDeprecationWarning: ("If you're gonna depricate it, just depricate it!"),
    # ResourceWarning: (""),
    RuntimeWarning: ("Lookin' pretty sus..."),
    SyntaxWarning: ("Lookin' pretty sus..."),
    UnicodeWarning: ("Lookin' pretty sus..."),
    UserWarning: general_insults,
    IOError: ("Good luck figuring [italic]that[/] out"),
    # EnvironmentError: ("Gosh, you're worse than global warming"),
}

if sys.platform in ('win32', 'cygwin'):
    replacements[WindowsError] = ("If you used [italic]Linux[/] you wouldn't be having this problem", "Try using a [italic]real[/] operating system", "You're clearly not a programmer"),

print_type = True
# 15% of the time it just gives a random generic insult
general_insult_percentage = 15

def unhelpful_except_hook(type_, value, traceback):
    if traceback is not None:
        print("Traceback (most recent call last):")
        print('\t' + choice(traceback_msgs))

    if print_type:
        print(type_.__name__, end=': ')

    if randint(0, 100) <= general_insult_percentage:
        print(choice(xkcd + general_insults))
    else:
        if type_ in replacements:
            msgs = replacements[type_]
            print(msgs if type(msgs) is str else choice(msgs))
        else:
            print(choice(misc_error_msgs))

sys.excepthook = unhelpful_except_hook
