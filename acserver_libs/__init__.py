import os
import json
import re
import sys
from shutil import copyfile
import hashlib
import zipfile


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for f in files:
            ziph.write(os.path.join(root, f))


class AssetGatherer:
    def __init__(self, steam_path, outfile='assetto-assets.zip', tempdir='/var/tmp/assetto-assets'):
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
            for file in files:
                if file in file_list:
                    source = os.path.join(root, file)
                    target = re.sub(self.ac_dir, '', os.path.join(root, file)).strip('/')
                    destination = os.path.join(self.tempdir, target)
                    if not os.path.exists(os.path.dirname(destination)):
                        os.makedirs(os.path.dirname(destination))
                    copyfile(source, os.path.join(self.tempdir, destination))

    def gather_car_files(self):
        for root, dirs, files in os.walk(self.cars_dir):
            for file in files:
                if file == 'data.acd':
                    source = os.path.join(root, file)
                    target = re.sub(self.ac_dir, '', os.path.join(root, file)).strip('/')
                    destination = os.path.join(self.tempdir, target)
                    if not os.path.exists(os.path.dirname(destination)):
                        os.makedirs(os.path.dirname(destination))
                    copyfile(source, os.path.join(self.tempdir, destination))

    def gather_acserver_binary(self):
        copyfile(os.path.join(self.acserver_dir, 'acServer'), os.path.join(self.tempdir, 'acServer'))

    def create_archive(self):
        zipf = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        zipdir(self.tempdir, zipf)
        zipf.close()

    def create(self):
        self.gather_fixtures()
        self.gather_acserver_binary()
        self.gather_track_files()
        self.gather_car_files()
        self.create_archive()


class Inspector:
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

        for root, dirs, files in os.walk(self.path, 'cars'):
            car_ui_json = os.path.join(root, 'ui', 'ui_car.json')
            if os.path.isfile(car_ui_json):
                fh = open(car_ui_json)
                car_ui_json_raw = fh.read()
                fh.close()
                try:
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

        for root, dirs, files in os.walk(self.path, 'tracks'):
            if 'ui_track.json' in files:
                fh = open(os.path.join(root, 'ui_track.json'))
                track_ui_json_raw = fh.read()
                fh.close()
                try:
                    track_ui_json_unicodefix = unicode(track_ui_json_raw, errors='replace')
                    track_detail = json.loads(track_ui_json_unicodefix.replace('\r\n', '').replace('\t', ''))
                    for k in track_detail.keys():
                        if k not in ['name', 'description', 'country', 'pitboxes', 'run']:
                            del track_detail[k]
                            track_detail['subversion'] = None
                            workdir = re.sub(tracks_root + '/', '', root)
                            workdirs_split = re.split('/', workdir)
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



