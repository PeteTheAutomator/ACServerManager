import zipfile
import os
from shutil import copyfile, copytree, rmtree
from background_task import background
from datetime import timedelta
from django.conf import settings
from .models import AssetCollection
from django.core.management import call_command


def unzip(source_filename, dest_dir):
    zip = zipfile.ZipFile(source_filename)
    zip.extractall(dest_dir)


def validate_assets():
    assets_tmp_dir = os.path.join(settings.ACSERVER_HOME, 'assets-tmp')
    if not os.path.isdir(assets_tmp_dir):
        raise Exception('Cannot find assets temp dir')

    if not os.path.isfile(os.path.join(assets_tmp_dir, 'fixtures.json')):
        raise Exception('Cannot find fixtures.json')

    if not os.path.isfile(os.path.join(assets_tmp_dir, 'acServer')):
        raise Exception('Cannot find acServer file')

    if not os.path.isdir(os.path.join(assets_tmp_dir, 'content')):
        raise Exception('Cannot find content dir')


@background(schedule=timedelta(seconds=0))
def process_assets(assetcollection_id):
    assetcollection = AssetCollection.objects.get(id=assetcollection_id)
    assets_tmp_dir = os.path.join(settings.ACSERVER_HOME, 'assets-tmp')
    unzip(assetcollection.collection, assets_tmp_dir)
    validate_assets()

    src_fixtures_file = os.path.join(assets_tmp_dir, 'fixtures.json')
    src_acserver_file = os.path.join(assets_tmp_dir, 'acServer')
    src_content_dir = os.path.join(assets_tmp_dir, 'content')
    dest_acserver_file = os.path.join(settings.ACSERVER_BIN_DIR, 'acServer')
    dest_content_dir = os.path.join(settings.ACSERVER_BIN_DIR, 'content')

    call_command('loaddata', src_fixtures_file)

    copyfile(src_acserver_file, dest_acserver_file)
    os.chmod(dest_acserver_file, 0755)

    # copy the content dir to the working location, after first renaming any existing content dir to .bak,
    # and any pre-existing content.bak directory gets erased.
    if os.path.isdir(dest_content_dir):
        if os.path.isdir(dest_content_dir + '.bak'):
            rmtree(dest_content_dir + '.bak')

        os.rename(dest_content_dir, dest_content_dir + '.bak')

    copytree(src_content_dir, dest_content_dir)
