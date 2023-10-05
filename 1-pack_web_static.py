#!/usr/bin/python3
""" Script Fabric that creates a .tgz """
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Script that generates a .tgz archive """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(date)
    tgz_archive = local("tar -cvzf {} web_static".format(archive_path))

    if tgz_archive.succeeded:
        return archive_path
    else:
        return None
