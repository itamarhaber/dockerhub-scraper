import json
import requests
from datetime import datetime
from pathlib import Path

def get_stats(user, name):
    uri = f'https://hub.docker.com/v2/repositories/{user}/{name}/'
    print(f'Getting stats for {user}/{name}')
    req = requests.get(uri)
    return req.json()

def init_db(user, name):
    path = f'data/{user}/'
    fullpath = f'{path}{name}.json'
    Path(path).mkdir(parents=True, exist_ok=True)
    if not Path(fullpath).exists():
        with open(fullpath, 'w') as f:
            json.dump([], f)
    return fullpath

def append_stats(dt, user, name, pull_count, star_count):
    path = init_db(user, name)
    # !!! TODO: make the append w/o parsing the JSON
    with open(path, 'r') as f:
        j = json.load(f)
    j.append({
        'date': dt,
        'pull_count': pull_count,
        'star_count': star_count,
    })
    with open(path, 'w') as f:
        json.dump(j, f)

if __name__ == '__main__':
    sample = {
        'timestamp': datetime.now().timestamp()
    }
    print(f'{sample["timestamp"]} Starting run...')
    with open('./config/sources.json', 'r') as f:
        sources = json.load(f)

    for source in sources:
        user = source['user']
        name = source['name']
        fullname = f'{user}/{name}'
        j = get_stats(user, name)
        sample[fullname] = j['pull_count']

    # Init DB
    datapath = './data/'
    dbpath = f'{datapath}db.json'
    Path(datapath).mkdir(parents=True, exist_ok=True)
    if not Path(dbpath).exists():
        with open(dbpath, 'w') as f:
            json.dump([], f)
    # !!! TODO: make the append w/o parsing the JSON
    with open(dbpath, 'r') as f:
        j = json.load(f)
    j.append(sample)
    with open(dbpath, 'w') as f:
        json.dump(j, f)

    print('done.')