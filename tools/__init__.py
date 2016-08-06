import os
import json
import re


class Inspector():
    def __init__(self, path='/home/pete/steam/assetto'):
        self.path = path

    # we need to walk the client's version of content/cars, picking-out car names and skin names
    def get_cars_and_skins(self, carsdir):
        cars = {}
        for root, dirs, files in os.walk(carsdir):
            if 'data.acd' in files:
                car = re.sub(carsdir + '/', '', root)
                cars[car] = []
                if 'skins' in dirs:
                    skins = os.listdir(os.path.join(root, 'skins'))
                    cars[car] = skins
        return cars

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
        cars_and_skins = self.get_cars_and_skins('/home/pete/Desktop/cars')
        tracks = self.get_track_listing()

        car_pk = 1
        car_skin_pk = 1
        for car in cars_and_skins.keys():
            results.append(
                {
                    'pk': car_pk,
                    'fields': {
                        'name': car,
                    },
                    'model': 'library.car',
                }
            )

            for car_skin in cars_and_skins[car]:
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

        track_pk = 0
        for track in tracks:
            results.append(
                {
                    'pk': track_pk,
                    'fields': {
                        'name': track['track'],
                        'subversion': track['subversion'],
                    },
                    'model': 'library.track',
                }
            )
            track_pk += 1

        return results


