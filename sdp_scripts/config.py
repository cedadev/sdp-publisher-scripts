import os
import grp

from projects import Project


# path to setup script which is required before esgpublish / esgunpublish can be run
# (if none needed, set to None)
setup_script = "/group_workspaces/jasmin/esgf_fedcheck/publisher/setup_env.sh"

# directory containing esg*.ini
ini_dir = "/group_workspaces/jasmin/esgf_fedcheck/publisher/ini"

# dictionary of objects for known projects, which can be used to look up mapfile paths etc,
# each instantiated using their data root, mapfile root, and mapfile subdirectory depth for 
# that project (to enable the leading part of the DRS to be used in the mapfile path)
projects = {
    "cmip5rt": Project("/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5rt/data",
                       "/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5rt/metadata/mapfiles/by_name",
                       1),

    "cmip5": Project("/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5/data", 
                     "/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5/metadata/mapfiles/by_name", 
                     5),
    }

# group ownership to set on mapfiles
gid = grp.getgrnam("gws_esgf_fedcheck").gr_gid

# file and directory ownerships to set
dir_mode = 0775
file_mode = dir_mode & 0666


# location of credentials file; 
# it should contain the following three items (one per line) relating to myproxy:
#    hostname (or hostname:port)
#    username
#    password
credentials_file = os.path.join(os.environ["HOME"], ".myproxy_creds")

# where to store the myproxy certificate
# probably should not change this
certificate_file = os.path.join(os.environ["HOME"], ".globus", "certificate-file")

# myproxy certificate lifetime (in hours) to request
certificate_lifetime = 72
