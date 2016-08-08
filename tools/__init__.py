import os
import json
import re


class Inspector:
    def __init__(self, path):
        self.path = path
        self.results = {
            'cars': [],
            'tracks': [],
            'weathers': [],
        }

    def get_cars(self):
        cars_root = os.path.join(self.path, 'cars')

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
                        if k not in ['name', 'brand', 'class']:
                            del car_detail[k]

                        car_detail['dirname'] = os.path.basename(root)

                        if 'skins' in dirs:
                            car_detail['skins'] = os.listdir(os.path.join(root, 'skins'))

                    self.results['cars'].append(car_detail)
                except:
                    raise Exception('failed to parse car_ui_json on ' + root)

    def get_tracks(self):
        tracks_root = os.path.join(self.path, 'tracks')

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
        for car in self.results['cars']:
            results.append(
                {
                    'pk': car_pk,
                    'fields': {
                        'name': car['name'],
                        'brand': car['brand'],
                        'clarse': car['class'],
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



