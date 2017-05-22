#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='sdp_scripts',
      version='0.1',
      description='Synda post-processing module plugins for ESGF publisher',
      author='Alan Iwi',
      author_email='alan.iwi@stfc.ac.uk',
      packages=find_packages(),

      # including ".py" in the names, because sdp looks for files called 
      # *.sh or *.py
      entry_points={
        "console_scripts": [
            "sdp_mapfile.py=sdp_scripts.mapfile:main",
            "sdp_publish.py=sdp_scripts.publish:main"
            ]
        },
      scripts=["tests/test_mapfile.sh", "tests/test_publication.sh"]
      )
