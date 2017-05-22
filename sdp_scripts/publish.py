#!/usr/bin/env python

"""
plugin for sdp to publish to ESGF
"""

import os
import config

from sdp_args import parse_args
from certs import ensure_certificate
from cmd_runner import run_command
from utils import Log


def main():

    ns = parse_args()
    log = Log(ns.worker_log)

    project_id = ns.project
    project = config.projects[project_id]
    dataset_id = ns.dataset_id

    mapfile_path = project.mapfile_path(dataset_id)

    log("requested to publish {0} using mapfile {1}".format(dataset_id,
                                                            mapfile_path))

    # check certificate now, as about to need it
    log("checking myproxy certificate")
    ensure_certificate(config.certificate_file,
                       config.credentials_file,
                       lifetime=config.certificate_lifetime,
                       log=log)


    unpub_args = ["--project", project_id,
                  "--delete",
                  "--database-delete",
                  "--no-republish",
                  "--no-thredds-reinit",  # see comment below
                  "--map", mapfile_path]

    cmd = "esgpublish"

    common_args = ["--project", project_id,        
                   "--map", mapfile_path,
                   "--set-replica"]

    db_args = []

    tds_args = ["--noscan",
                "--thredds",
                "--service", "fileservice",
                "--no-thredds-reinit"]

    tds_reinit_args = ["--project", project_id,
                       "--thredds", 
                       "--use-list", "/dev/null"]

    solr_args = ["--noscan", "--publish"]


    # For speed, do not do THREDDS reinit during unpublishing because
    # it is not necessary and can wait until after publication to
    # THREDDS (see unpub_args above).  However, ensure that if the
    # publication to db or creation of the THREDDS XML file fail, the
    # THREDDS reinit still gets done.

    log("unpublishing (if it exists)")
    run_command("esgunpublish", unpub_args, log)

    try:
        log("publishing to database")
        run_command(cmd, common_args + db_args, log)

        log("publishing to THREDDS (without reinit)")
        run_command(cmd, common_args + tds_args, log)

    finally:
        log("THREDDS reinit")
        run_command(cmd, tds_reinit_args, log)


    # probably overkill, but recheck that certificate is still valid
    # in case publication to db/THREDDS was really slow
    log("checking myproxy certificate")
    ensure_certificate(config.certificate_file,
                       config.credentials_file,
                       lifetime=config.certificate_lifetime,
                       log=log)

    log("publising to Solr")
    run_command(cmd, common_args + solr_args, log)


if __name__ == '__main__':
    main()
