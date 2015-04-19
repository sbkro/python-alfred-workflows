# -*- coding: utf-8 -*-
from shovel import task
from _internal import pushd, git_filter_branch, github_clone


@task
def develop():
    print('setup develop start')

    with pushd('./date'):
        github_clone(
            'sbkro', 'python-alfred-workflows',
            branch='develop', dir_name='workflows'
        )

    with pushd('./date/workflows'):
        git_filter_branch('workflows')

    print('setup develop finished')
