#!/usr/bin/python3
"""Script to deploy web static"""

from fabric.api import put, run, task, env
from os.path import exists, splitext

# Define target hosts
env.hosts = ['100.25.142.90', '54.145.241.45']


@task
def do_deploy(archive_path):
    """Deploys an archive to web servers."""

    # Check if the archive exists
    if not exists(archive_path):
        return False

    # Extract archive name and file name from path
    archive_name = archive_path.split('/')[-1]
    file_name_without_extension = splitext(archive_name)[0]

    # Define remote paths
    temp_remote_path = "/tmp/{}".format(archive_name)
    release_remote_path = (
            "/data/web_static/releases/{}"
            .format(file_name_without_extension)
            )

    # Upload the archive to the remote server's temp directory
    put(archive_path, '/tmp/')

    # Deploy the archive
    run('mkdir -p {}'.format(release_remote_path))
    run('tar -xzf {} -C {}'.format(temp_remote_path, release_remote_path))
    run('rm {}'.format(temp_remote_path))
    run('mv {0}/web_static/* {0}/'.format(release_remote_path))
    run('rm -rf {}/web_static'.format(release_remote_path))

    # Update the symbolic link
    run('rm -rf /data/web_static/current')
    run('ln -s {} /data/web_static/current'.format(release_remote_path))

    print("New version deployed!")
    return True
