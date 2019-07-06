import os
import ctypes
import cmd

class ZeroException(Exception):
    pass


def arg_parse(func):
    
    def wrapper(self, arg):
        args = []
        if arg != '':
            arg = ' '.join(arg.split())
            arg = eval(arg.replace(' ', ','))
            if not isinstance(arg, tuple):
                args.append(arg)
            else:
                args.extend(list(arg))
        try:
            result = func(self, *args)
            if result != None:
                print(result)
            else:
                print("Done")
        except Exception as e:
            print(e)
    return wrapper

class ZeroCmd(cmd.Cmd):
    intro = 'Welcome to Zero shell. Type help or ? to list the command'
    prompt = 'zero>>'

    def do_quit(self, arg):
        return True


