import os
import platform
import json
import sys
from shutil import copyfile
import hashlib
import zipfile
import requests


def md5(fname):
    """
    Calculates the md5 hash of a file
    :param fname: path to the file
    :return: string (md5 hash)
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def make_archive(file_list, archive, root):
    """
    Makes a zip archive
    :param file_list: a list of files to be included in the archive
    :param archive: filename of the resulting archive
    :param root: a path to become the root directory of the archive
    """
    a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)
    for f in file_list:
        print "archiving file %s" % f
        a.write(f, os.path.relpath(f, root))
    a.close()


class AssetGatherer:
    """
    Given a Steam installation directory, this class will build zip archive of the required files and a database fixture
    to be loaded into the Assetto Corsa Server Manager
    """
    def __init__(self, steam_path, outfile='assetto-assets.zip', tempdir='tmp'):
        self.steam_path = steam_path
        self.outfile = outfile
        self.tempdir = tempdir
        self.ac_dir = os.path.join(self.steam_path, 'steamapps', 'common', 'assettocorsa')
        self.acserver_dir = os.path.join(self.steam_path, 'steamapps', 'common', 'Assetto Corsa Dedicated Server')
        self.tracks_dir = os.path.join(self.ac_dir, 'content', 'tracks')
        self.cars_dir = os.path.join(self.ac_dir, 'content', 'cars')
        self.weather_dir = os.path.join(self.ac_dir, 'content', 'weather')
        if not os.path.isdir(tempdir):
            os.makedirs(tempdir)

    def validate_installation(self):
        expected_dirs = [
            self.ac_dir,
            self.tracks_dir,
            self.cars_dir,
            self.weather_dir,
        ]

        missing_folders_list = []
        for folder in expected_dirs:
            if not os.path.isdir(folder):
                missing_folders_list.append(folder)

        if len(missing_folders_list) > 0:
            print 'Could not find the following folder(s): '
            for folder in missing_folders_list:
                print folder
            sys.exit(1)

        acserver_binary = os.path.join(self.acserver_dir, 'acServer')
        if not os.path.isfile(acserver_binary):
            print 'Could not find the Assetto Corsa Dedicated Server binary: '
            print '   ' + acserver_binary
            print 'Please install this using Steam.'
            sys.exit(1)

    def validate_acserver_binary(self, acserver_builds):
        actual_acserver_md5 = md5(os.path.join(self.acserver_dir, 'acServer'))
        if actual_acserver_md5 not in acserver_builds:
            return False
        else:
            return True

    def gather_fixtures(self):
        i = Inspector(self.ac_dir)
        fixtures = i.generate_fixtures()
        fh = open(os.path.join(self.tempdir, 'fixtures.json'), 'w')
        fh.write(json.dumps(fixtures, indent=4))
        fh.close()

    def gather_track_files(self):
        file_list = [
            'drs_zones.ini',
            'surfaces.ini',
        ]

        for root, dirs, files in os.walk(self.tracks_dir):
            for f in files:
                if f in file_list:
                    source = os.path.join(root, f)
                    common_prefix = os.path.commonprefix([self.ac_dir, source])
                    target = os.path.join(self.tempdir, os.path.relpath(source, common_prefix))
                    if not os.path.exists(os.path.dirname(target)):
                        os.makedirs(os.path.dirname(target))
                    copyfile(source, target)

    def gather_car_files(self):
        for root, dirs, files in os.walk(self.cars_dir):
            for f in files:
                if f == 'data.acd':
                    source = os.path.join(root, f)
                    common_prefix = os.path.commonprefix([self.ac_dir, source])
                    target = os.path.join(self.tempdir, os.path.relpath(source, common_prefix))
                    if not os.path.exists(os.path.dirname(target)):
                        os.makedirs(os.path.dirname(target))
                    copyfile(source, target)

    def gather_acserver_binary(self):
        copyfile(os.path.join(self.acserver_dir, 'acServer'), os.path.join(self.tempdir, 'acServer'))

    def build_payload(self):
        file_list = []
        for root, dirs, files in os.walk(self.tempdir):
            for f in files:
                file_list.append(os.path.join(root, f))
        make_archive(file_list, self.outfile, self.tempdir)

    def create(self):
        self.gather_fixtures()
        self.gather_acserver_binary()
        self.gather_track_files()
        self.gather_car_files()
        self.build_payload()


class Inspector:
    """
    Examines the Assetto Corsa content directory and builds a JSON database fixture of tracks, cars and skins
    """
    def __init__(self, path):
        self.path = path
        self.results = {
            'cars': [],
            'tracks': [],
            'weathers': [],
        }

    def get_cars(self):
        cars_root = os.path.join(self.path, 'content', 'cars')

        if not os.path.isdir(cars_root):
            raise Exception('Cannot find cars root directory')

        for root, dirs, files in os.walk(cars_root):
            car_ui_json = os.path.join(root, 'ui', 'ui_car.json')
            if os.path.isfile(car_ui_json):
                fh = open(car_ui_json)
                car_ui_json_raw = fh.read()
                fh.close()
                try:
                    if platform.system() == 'Windows':
                        car_detail = json.loads(car_ui_json_raw.replace('\n', '').replace('\t', ''))
                    else:
                        car_detail = json.loads(car_ui_json_raw.replace('\r\n', '').replace('\t', ''))

                    car_detail['skins'] = None
                    for k in car_detail.keys():
                        if k not in ['name', 'brand', 'class', 'tags']:
                            del car_detail[k]

                        car_detail['dirname'] = os.path.basename(root)

                        if 'skins' in dirs:
                            car_detail['skins'] = os.listdir(os.path.join(root, 'skins'))

                    self.results['cars'].append(car_detail)
                except:
                    raise Exception('failed to parse car_ui_json on ' + root)

    def get_tracks(self):
        tracks_root = os.path.join(self.path, 'content', 'tracks')

        if not os.path.isdir(tracks_root):
            raise Exception('Cannot find tracks root directory')

        for root, dirs, files in os.walk(tracks_root):
            if 'ui_track.json' in files:
                fh = open(os.path.join(root, 'ui_track.json'))
                track_ui_json_raw = fh.read()
                fh.close()
                try:
                    track_ui_json_unicodefix = unicode(track_ui_json_raw, errors='replace')
                    if platform.system() == 'Windows':
                        track_detail = json.loads(track_ui_json_unicodefix.replace('\n', '').replace('\t', ''))
                    else:
                        track_detail = json.loads(track_ui_json_unicodefix.replace('\r\n', '').replace('\t', ''))

                    for k in track_detail.keys():
                        if k not in ['name', 'description', 'country', 'pitboxes', 'run']:
                            del track_detail[k]
                            track_detail['subversion'] = None
                            workdir = os.path.relpath(root, tracks_root)
                            workdirs_split = workdir.split(os.sep)
                            track_detail['dirname'] = workdirs_split[0]
                            if len(workdirs_split) > 2:
                                track_detail['subversion'] = workdirs_split[-1]
                    self.results['tracks'].append(track_detail)
                except:
                    raise Exception('failed to parse track_ui_json: ' + os.path.join(root, 'ui_track.json'))

    def generate_fixtures(self):
        self.get_tracks()
        self.get_cars()
        results = []
        track_pk = 0
        for track in self.results['tracks']:
            results.append(
                {
                    'pk': track_pk,
                    'fields': {
                        'name': track['name'],
                        'dirname': track['dirname'],
                        'subversion': track['subversion'],
                        'run': track['run'],
                        'country': track['country'],
                        'pitboxes': track['pitboxes'],
                        'description': track['description'],

                    },
                    'model': 'library.track',
                }
            )
            track_pk += 1

        car_pk = 1
        car_skin_pk = 1
        car_tag_pk = 1
        car_tag_dict = {}
        for car in self.results['cars']:
            car_tag_pk_list = []

            for car_tag in car['tags']:
                if car_tag not in car_tag_dict:
                    car_tag_dict[car_tag] = car_tag_pk
                    results.append(
                        {
                            'pk': car_tag_pk,
                            'fields': {
                                'name': car_tag,
                            },
                            'model': 'library.cartag',
                        }
                    )
                    car_tag_pk += 1

                car_tag_pk_list.append(car_tag_dict[car_tag])

            results.append(
                {
                    'pk': car_pk,
                    'fields': {
                        'name': car['name'],
                        'brand': car['brand'],
                        'clarse': car['class'],
                        'tags': car_tag_pk_list,
                        'dirname': car['dirname'],
                    },
                    'model': 'library.car',
                }
            )

            for car_skin in car['skins']:
                results.append(
                    {
                        'pk': car_skin_pk,
                        'fields': {
                            'name': car_skin,
                            'car': car_pk,
                        },
                        'model': 'library.carskin',
                    }
                )
                car_skin_pk += 1
            car_pk += 1

        return results


class ACManagerAPI:
    def __init__(self, baseurl='http://localhost:8000'):
        self.baseurl = baseurl
        self.api_auth = self.baseurl + '/api-auth/login/'
        self.api = self.baseurl + '/api'

    def test_conn(self):
        r = requests.head(self.api_auth)
        if r.status_code != 200:
            raise Exception('Got unexpected http status code {0} from {1}'.format(r.status_code, self.api_authl))

    def get_tracks(self):
        results = []
        next_url = self.api + '/cars/'
        while next_url:
            r = requests.get(next_url)
            if r.status_code != 200:
                raise Exception('Got unexpected http status code {0} from {1}'.format(r.status_code, next_url))
            results += (r.json().get('results'))
            next_url = r.json().get('next')
        return results

