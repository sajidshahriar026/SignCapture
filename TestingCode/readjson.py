import json


if __name__ == '__main__':
    location = 'F:/BDSL-50/BDSL-50.json'
    logs = []
    try:
        with open(location ,'r') as fileHandle:
            logs = json.load(fileHandle)
    except:
        pass
    else:
        print(logs)