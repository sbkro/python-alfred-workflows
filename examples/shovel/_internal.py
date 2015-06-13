# -*- coding: utf-8 -*-
import os
import subprocess
from contextlib import contextmanager


def call(args):
    print('call -> {0}'.format(' '.join(args)))
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()

    if p.returncode == 0:
        print(stdout)
    else:
        raise Exception('error: stderr: {0}'.format(stderr))


@contextmanager
def pushd(path):
    print('cd -> {0}'.format(path))
    cwd = os.getcwd()
    os.chdir(path)

    yield

    os.chdir(cwd)
    print('cd -> {0}'.format(cwd))


def github_clone(username, reponame, branch=None, dir_name=None):
    if reponame.find('.git') == -1:
        reponame = reponame + '.git'

    args = ['git', 'clone',
            os.path.join('http://github.com', username, reponame)]

    if branch is not None:
        args.append('-b')
        args.append(branch)

    if dir_name is not None:
        args.append(dir_name)

    call(args)


def git_filter_branch(path):
    args = ['git', 'filter-branch',
            '-f', '--subdirectory-filter', path, 'HEAD']
    call(args)
