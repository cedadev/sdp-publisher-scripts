import os
import grp
from projects import Project

projects = {
    "cmip5rt": Project("/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5rt", 1),
    "cmip5": Project("/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5", 5),
    }

group = "gws_esgf_fedcheck"
gid = grp.getgrnam(group).gr_gid

dir_mode = 0775
file_mode = dir_mode & 0666


# credentials file should have three lines relating to myproxy:
# - hostname (or hostname:port)
# - username
# - password
credentials_file = os.path.join(os.environ["HOME"], ".myproxy_creds")
certificate_file = os.path.join(os.environ["HOME"], ".globus", "certificate-file")
certificate_lifetime = 72
