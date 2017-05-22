"""
lookups from known projects
"""

from os.path import join as opj

class Project:

    def __init__(self, project_root, mapfile_depth=1):
        self.project_root = project_root
        self.mapfile_depth = mapfile_depth

    @property
    def project_data_root(self):
        return opj(self.project_root, "data")

    @property
    def project_mapfile_root(self):
        return opj(self.project_root, "metadata/mapfiles/by_name")

    def dataset_root(self, dataset_id):
        """
        Returns the top directory for a given dataset ID.
        """
        return opj(self.project_data_root, dataset_id.replace(".", "/"))

    def mapfile_path(self, dataset_id):
        """
        Returns the mapfile path for a given dataset ID.
        """
        facets = dataset_id.split(".")
        filename = "{0}.map".format(dataset_id)
        leading_dirs = opj(*facets[ : self.mapfile_depth])
        return opj(self.project_mapfile_root, leading_dirs, filename)

if __name__ == '__main__':
    project = Project("/group_workspaces/jasmin/esgf_fedcheck/archive/badc/cmip5", 5),
    dsid = "cmip5rt.output1.MPI-M.MPI-ESM-MR.rcp26.mon.ocean.Omon.r1i1p1.hfds.v20120625"
    
    print project.dataset_root(dsid)
    print project.mapfile_path(dsid)

