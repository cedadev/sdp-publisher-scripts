#!/usr/bin/env python

"""
plugin for sdp to create mapfiles
"""

import os

import config
from sdp_args import parse_args
from cmd_runner import run_command
from utils import ensure_parent_dirs, set_perms, Log


def main():

    ns = parse_args()
    log = Log(ns.worker_log)


    project_id = ns.project
    project = config.projects[project_id]
    dataset_id = ns.dataset_id

    dataset_dir = project.dataset_root(dataset_id)
    mapfile_path = project.mapfile_path(dataset_id)

    ensure_parent_dirs(mapfile_path, mode=config.dir_mode, gid=config.gid)

    cmd = "esgprep mapfile"

    args = ["--project", project_id,
            "--max-threads", "4",
            "--mapfile", mapfile_path,
            dataset_dir]

    log("Making mapfile {0}".format(mapfile_path))

    try:
        run_command(cmd, args, log)
    finally:
        # if anything is created, even if unsuccessful, set permissions
        if os.path.exists(mapfile_path):
            set_perms(mapfile_path, config.file_mode, config.gid)


if __name__ == '__main__':
    main()
