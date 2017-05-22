"""
lookups from known projects
"""

import os

import config

class Project:

    def __init__(self, data_root, mapfile_root, mapfile_depth=1):
        self.data_root = data_root
        self.mapfile_root = mapfile_root
        self.mapfile_depth = mapfile_depth

    def dataset_root(self, dataset_id):
        """
        Returns the top directory for a given dataset ID.
        """
        return os.path.join(self.data_root, dataset_id.replace(".", "/"))

    def mapfile_path(self, dataset_id):
        """
        Returns the mapfile path for a given dataset ID.
        """
        facets = dataset_id.split(".")
        filename = "{0}.map".format(dataset_id)
        leading_dirs = os.path.join(*facets[ : self.mapfile_depth])
        return os.path.join(self.mapfile_root, leading_dirs, filename)

if __name__ == '__main__':
    project = Project("/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5/data",
                      "/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5/metadata/mapfiles/by_name/data",
                      5),
    dsid = "cmip5rt.output1.MPI-M.MPI-ESM-MR.rcp26.mon.ocean.Omon.r1i1p1.hfds.v20120625"
    
    print project.dataset_root(dsid)
    print project.mapfile_path(dsid)

