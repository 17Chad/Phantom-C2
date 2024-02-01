import readline
from collections import OrderedDict

# ANSI escape sequences for colors
GREEN = '\033[1;38;5;2m'
ORANGE = '\033[93m'
RESET = '\033[0m'

class AutoComplete:
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:  
            return None

class Menu:
    def __init__(self, name):
        self.name = name
        self.commands = OrderedDict()
        self.Commands = []

    def registerCommand(self, command, description, args):
        self.commands[command] = [description, args]

    def showHelp(self):
        print(f"\n{GREEN}Available commands:{RESET}\n")
        for command, details in self.commands.items():
            print(f"{command:<15} {details[0]:<25} {details[1]}")
        print()

    def clearScreen(self):
        print("\033[H\033[J", end="")

    def uCommands(self):
        self.Commands = list(self.commands.keys())

    def setPrompt(self, prompt):
        self.name = prompt

    def parse(self):
        readline.set_completer(AutoComplete(self.Commands).complete)
        readline.parse_and_bind('tab: complete')
        cmd = input(f"\n{GREEN}{self.name}{RESET}")
        cmd_parts = cmd.split()
        command = cmd_parts[0] if cmd_parts else ""
        args = cmd_parts[1:]
        return command, args
