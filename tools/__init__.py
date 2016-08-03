import os
import json
import re


class Inspector():
    def __init__(self, path='/home/pete/steam/assetto'):
        self.path = path

    def get_car_listing(self):
        return os.listdir(os.path.join(self.path, 'content', 'cars'))

    def get_track_listing(self):
        tracks_dir = os.path.join(self.path, 'content', 'tracks')
        results = []
        for root, dirs, files in os.walk(tracks_dir):
            if 'data' in dirs:
                try:
                    track, subversion = re.split('/', re.sub(tracks_dir + '/', '', root))
                except ValueError:
                    subversion = None
                    track = re.sub(tracks_dir + '/', '', root)

                results.append(
                    {
                        'track': track,
                        'subversion': subversion
                    }
                )

        return results


    def get_track_listing_old(self):
        return os.listdir(os.path.join(self.path, 'content', 'tracks'))

    def generate_fixture(self):
        results = []
        cars = self.get_car_listing()
        tracks = self.get_track_listing()

        c = 0
        for car in cars:
            results.append(
                {
                    'pk': c,
                    'fields': {
                        'name': car,
                    },
                    'model': 'acsession.car',
                }
            )
            c += 1

        c = 0
        for track in tracks:
            results.append(
                {
                    'pk': c,
                    'fields': {
                        'name': track['track'],
                        'subversion': track['subversion'],
                    },
                    'model': 'acsession.track',
                }
            )
            c += 1

        return results


