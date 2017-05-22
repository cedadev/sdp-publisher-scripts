"""
When imported, make sure we are running the script in the expected virtual
environment.  To put in main program before other imports.
"""

import os
import sys

python_exe = "/group_workspaces/jasmin/esgf_fedcheck/publisher/venv/bin/python"

if sys.executable != python_exe:
    os.execv(python_exe, [python_exe] + sys.argv)
    print "failed exec of {0} - continuing with {1}".format(python_exe,
                                                            sys.executable)
