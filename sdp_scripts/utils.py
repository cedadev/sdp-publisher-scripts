import os
import sys
import time


def ensure_parent_dirs(path, **perms_args):
    """
    create parent directories as necessary, also setting their mode and gid
    """
    parent = os.path.dirname(path)

    if not os.path.exists(parent):

        ensure_parent_dirs(parent, **perms_args)
        os.mkdir(parent)
        set_perms(parent, **perms_args)


def set_perms(path, mode=None, gid=None):

    if mode != None:
        os.chmod(path, mode)

    if gid != None:
        os.chown(path, os.getuid(), gid)


class Log:

    """
    Simple logger. Instantiate with filename, then call with message to append.
    """

    def __init__(self, path=None):
        self.path = path
        if path:
            self.fh = open(path, "a")
        else:
            self.fh = sys.stdout
        self._pidstr = "[pid={0}] ".format(os.getpid())
    
    def __call__(self, msg):
        if self.path:
            self.fh.seek(0, 2)
        prefix = time.strftime("[%Y-%m-%d %H:%M:%S] ") + self._pidstr
        for line in msg.split("\n"):
            self.fh.write(prefix + line + "\n")
        self.fh.flush()

    def close(self):
        if self.path:
            self.fh.close()

    def __del__(self):
        self.close()
