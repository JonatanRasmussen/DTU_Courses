import os
import json

class Persistence:

    def save_json(dct, file_name):
        """Save dictionary as JSON file in location specified by file_name"""
        folder_name = 'my_folder'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_location = f'{folder_name}/{file_name}.json'
        with open(file_location, 'w') as fp:
            json.dump(dct, fp)

