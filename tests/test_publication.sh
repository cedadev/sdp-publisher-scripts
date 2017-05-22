#!/bin/sh

sdp_publish.py \
  --pipeline republication \
  --data_folder /group_workspaces/jasmin/esgf_fedcheck/synda/sdp/data \
  --project cmip5rt \
  --variable hfds \
  --model MPI-ESM-MR \
  --dataset_pattern cmip5rt/output1/MPI-M/MPI-ESM-MR/rcp26/mon/ocean/Omon/r1i1p1/hfds/v20120625 \
  --script-dir /group_workspaces/jasmin/esgf_fedcheck/synda/pp_scripts \
  --worker-log /tmp/worker.log
