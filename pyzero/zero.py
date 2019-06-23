import os
import ctypes
import cmd

class ZeroException(Exception):
    pass

class Zero(object):

    def __init__(self):
        pass

    @property
    def base_lib(self):
        lib_file = os.environ.get("PYZERO_LIB_PATH", "/usr/lib") + "/"
        lib_file += os.environ.get("PYZERO_LIB_NAME", "libzero.so")

        return ctypes.cdll.LoadLibrary(lib_file)

    @property
    def cpointer(self):
        return self._cpointer

    @cpointer.setter
    def cpointer(self, cptr):
        self._cpointer = cptr
        if cptr == 0:
            raise ZeroException("Invalid c pointer")


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


