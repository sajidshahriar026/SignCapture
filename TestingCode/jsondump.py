import os
import json

if __name__ == '__main__':

    dataset_location_logs = []
    fileName = 'jsondump.json'
    entry = {1:{'name': 'ami', 'location': 'videos'}}

    if not os.path.exists(fileName):
        with open(fileName, 'w') as file:
            dataset_location_logs.append(entry)
            json.dump(dataset_location_logs, file, indent=4)
    else:
        try:
            with open(fileName, 'r') as file:
                dataset_location_logs = json.load(file)
        except:
            pass
        finally:
            dataset_location_logs.append(entry)
            with open(fileName, 'w') as file:
                json.dump(dataset_location_logs, file)