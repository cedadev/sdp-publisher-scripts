# synda postprocessing module plugins for the ESGF publisher

These will work in a setup where the publisher has been installed in a non-system directory, not necessarily on a data node. In particular:

* the `-i <dir>` argument is passed to the publisher to tell it where to find the ini files
* a setup script can be specified which needs to be sourced before the `esgpublish` and `esgunpublish` commands are available

Also it will work in a situation where the publisher can be run by multiple users belonging to a given Unix group. The group id and permissions are specified in the config file, and the scripts will apply these to any mapfiles (and any parent directories created).

For each project, the data root and mapfile root is set in `config.py`, and also a mapfile subdirectory depth.
* For example, if mapfile subdirectory depth = 3, then for dataset
   * `cmip5rt.output1.MPI-M.MPI-ESM-MR.rcp26.mon.ocean.Omon.r1i1p1.hfds.v20120625`
* the mapfile path would be
   * `<mapfile_root>/cmip5rt/output1/MPI-M/cmip5rt.output1.MPI-M.MPI-ESM-MR.rcp26.mon.ocean.Omon.r1i1p1.hfds.v20120625.map`

Data is published with `--set-replica` flag.

The publication script will automatically obtain a certificate via myproxy if needed. If a certificate already exists at the correct path and is not already expired or about to expire (in the next hour), then no myproxy request is made.

## Installation

Create and activate a virtual environment, edit `config.py` as required, and then `python setup.py install` into the venv.

The files `sdp_mapfile.py` and `sdp_publish.py` from the `bin` directory of the venv can then be symbolically linked (or copied) into the synda `pp_scripts` directory, and a sdp pipeline file with `tasks=['sdp_mapfile', 'sdp_publish']` can be created

## Per-user credentials setup
Store the file in `$HOME/.myproxy_creds`
It should have 3 lines, hostname, username, password, e.g.
```
slcs1.ceda.ac.uk
johndoe
sausages
```

optionally the myproxy port number can be included in the host name, e.g. `slcs1.ceda.ac.uk:7512` (not tested)

## Obtaining trust roots

Also you need to make sure you have a directory `$HOME/.globus/certificates` containing the correct trust roots needed to validate the host certificate. If not, by running `myproxy-login` once by hand with the `-b` (bootstrap) flag, for example:
```
myproxy-logon -s slcs1.ceda.ac.uk -l johndoe -b
```
because the script will _not_ use bootstrap option when doing a myproxy login. (This example command just uses the default location for the user certificate, as we are only interested in the trust roots at this point.)
