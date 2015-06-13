# -*- coding: utf-8 -*-
import os
import shutil
import zipfile
from shovel import task


app_name = 'date'

top_dir = os.path.dirname(os.path.abspath(__name__))
build_dir = os.path.join(top_dir, '_build')
target_dir = os.path.join(top_dir, app_name)
config_dir = os.path.join(top_dir, 'config')


@task
def workflows():
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)

    shutil.copytree(target_dir, os.path.join(build_dir, app_name))
    shutil.copy(os.path.join(config_dir, 'info.plist'), build_dir)
    shutil.copy(os.path.join(config_dir, 'icon.png'), build_dir)

    app_file = zipfile.ZipFile(
        os.path.join(top_dir, '{0}.{1}'.format(app_name, 'alfredworkflow')),
        'w', zipfile.ZIP_DEFLATED
    )

    for root, dirs, files in os.walk(build_dir):
        for f in files:
            src = os.path.join(root, f)
            dst = src.split(build_dir)[1]
            app_file.write(src, dst)

    app_file.close()

    shutil.rmtree(build_dir)
