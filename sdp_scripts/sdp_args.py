"""
arg parsing for sdp scripts
"""

import argparse


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline', type=str)
    parser.add_argument('--data_folder', type=str)
    parser.add_argument('--project', type=str)
    parser.add_argument('--variable', type=str)
    parser.add_argument('--model', type=str)
    parser.add_argument('--dataset_pattern', type=str)
    parser.add_argument('--script-dir', type=str)
    parser.add_argument('--worker-log', type=str)

    ns = parser.parse_args()

    if ns.dataset_pattern:
        ns.dataset_id = ns.dataset_pattern.replace("/", ".")

    return ns


if __name__ == '__main__':
    ns = parse_args()
    print ns.project
    print ns.dataset_id

# to test, run with some args, e.g.

# python sdp_args.py --pipeline republication --data_folder /group_workspaces/jasmin/esgf_fedcheck/synda/sdp/data --project cmip5rt --variable hfds --model MPI-ESM-MR --dataset_pattern cmip5rt/output1/MPI-M/MPI-ESM-MR/rcp26/mon/ocean/Omon/r1i1p1/hfds/v20120625 --script-dir /group_workspaces/jasmin/esgf_fedcheck/synda/pp_scripts --worker-log /tmp/worker.log
