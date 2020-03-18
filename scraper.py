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

def append_stats(user, name, pull_count, last_updated):
    path = init_db(user, name)
    with open(path, 'r') as f:
        j = json.load(f)
    j.append({
        'pull_count': pull_count,
        'last_updated': last_updated,
    })
    with open(path, 'w') as f:
        json.dump(j, f)

if __name__ == '__main__':
    print(f'Starting run...')
    with open('./config/sources.json', 'r') as f:
        sources = json.load(f)

    for source in sources:
        user = source['user']
        name = source['name']
        j = get_stats(user, name)
        pull_count = j['pull_count']
        last_updated = j['last_updated']
        append_stats(user, name, pull_count, last_updated)

    print('done.')