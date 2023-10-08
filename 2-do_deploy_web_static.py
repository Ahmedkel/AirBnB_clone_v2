#!/usr/bin/python3
"""Script to deploy web static"""

from fabric.api import put, run, local, task
from os.path import exists, splitext
import socket

env.hosts = ['xx-web-01', 'xx-web-02']


@task
def do_deploy(archive_path):
    """Deploys an archive locally or to web servers based on the hostname."""

    # Check if the archive exists
    if not exists(archive_path):
        return False

    archive_name = archive_path.split('/')[-1]
    file_name_without_extension = splitext(archive_name)[0]

    temp_path = "/tmp/{}".format(archive_name)
    release_path = (
            "/data/web_static/releases/{}"
            .format(file_name_without_extension)
            )

    # Check if the script is running on one of the servers
    hostname = socket.gethostname()

    if hostname in env.hosts:
        # Remote deployment commands
        put(archive_path, '/tmp/')
        cmd = run
    else:
        # Local deployment commands
        local('cp {} {}'.format(archive_path, temp_path))
        cmd = local

    # Common deployment commands
    cmd('mkdir -p {}'.format(release_path))
    cmd('tar -xzf {} -C {}'.format(temp_path, release_path))
    cmd('rm {}'.format(temp_path))
    cmd('mv {0}/web_static/* {0}/'.format(release_path))
    cmd('rm -rf {}/web_static'.format(release_path))
    cmd('rm -rf /data/web_static/current')
    cmd('ln -s {} /data/web_static/current'.format(release_path))

    print("New version deployed!")
    return True
