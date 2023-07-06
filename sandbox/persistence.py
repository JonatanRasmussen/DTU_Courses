import os
import json


class Persistence:
    """ Save and retrieve data to and from storage """

    @staticmethod
    def save_json(dct, file_name):
        """Save dictionary as JSON file in location specified by file_name"""
        folder_name = 'data_folder'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_location = f'{folder_name}/{file_name}.json'
        with open(file_location, mode='w', encoding="utf-8") as fp:
            json.dump(dct, fp)
