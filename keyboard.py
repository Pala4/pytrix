# -*- coding: utf-8 -*import

import sys

try:
    import msvcrt

    KEY_LEFT = 'K'
    KEY_UP = 'H'
    KEY_RIGHT = 'M'
    KEY_DOWN = 'P'


    def flush():
        while msvcrt.kbhit():
            msvcrt.getch()


    def scan_key():
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == b'\xe0':
                return msvcrt.getch().decode()
            return ch.decode()
        return ''

except ImportError:
    import termios
    import fcntl
    import os

    KEY_LEFT = 'K'
    KEY_UP = 'H'
    KEY_RIGHT = 'M'
    KEY_DOWN = 'P'


    def scan_key():
        fd = sys.stdin.fileno()
        old_term = termios.tcgetattr(fd)
        new_attr = termios.tcgetattr(fd)
        new_attr[3] = new_attr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, new_attr)
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)
        try:
            while True:
                try:
                    return sys.stdin.read(1)
                except IOError:
                    return ''
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
            return ''
