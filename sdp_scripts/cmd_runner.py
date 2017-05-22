"""
wrapper for running esgprep or esgpublish
"""

import string
import subprocess
import os
import sys
import config

def run_command(cmd, args, log=None, add_ini_arg=True, abort_on_fail=True, verbose=False):
    """
    Wrapper for running shell command, which loads in the setup_env.sh
    and adds the -i argument to point to the ini directory.  Also runs with the 
    correct gid and umask.

    input:
      cmd (string) command to run, including any args that should appear before any 
                    "-i ..." arg that gets added   (e.g. "esgprep mapfile")
      args (list of strings) remaining args, (e.g. ["--project", "cmip5rt", .....])
      add_ini_arg (bool) whether to add implicit "-i /path/to/ini/dir"
      abort_on_fail (bool) whether to raise exception on non-zero return value

    returns: status
    """
    if log == None:
        log = sys.stdout.write    

    if add_ini_arg:
        args = ["-i", config.ini_dir] + args

    cmd_line = string.join([cmd] + args, " ")

    if config.setup_script:
        cmd_line = ". {0}; {1}".format(config.setup_script, cmd_line)

    p = subprocess.Popen(cmd_line,
                         preexec_fn=_sp_preexec,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    log("running command: {0}".format(cmd_line))
    output = p.communicate()[0]
    status = p.returncode
    log("command status: {0}".format(status))
    log("command output:\n{0}".format(output))
    if status != 0 and abort_on_fail:
        raise Exception("command {0} failed, see log".format(cmd_line))

    return status


def _sp_preexec():
    """
    set umask and egid
    """
    os.umask(0777 - config.dir_mode)
    


if __name__ == '__main__':
    status = run_command("esginitialize", ["-c"])
    print status

    status = run_command("esginitialize", ["-i", "/asdfasdfasdf"], add_ini_arg=False)
    print status  # not reached
