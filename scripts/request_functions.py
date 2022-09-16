import requests

NUM_REQUESTS = 100
RESULTS = {
    "times": [],
    "collisions": [],
    "hash keys": [],
}

if __name__ == '__main__':
    for e in ['pjw', 'md4', 'md5', 'sha1', 'sha2']:
        r = requests.get(f'http://localhost:8000/spread_collisions?algorith={e}')
        for w in ['zebrar', 'despersuadir']:
            ms_data = []
            for i in range(100):
                r = requests.get(f'http://localhost:8000/{e}?key={w}')

                data = r.json()
                ms_data.append(data['key_infos']['ms'])

            with open(f'./{e}_{w}_lexicon.csv', 'w') as f:
                for val in ms_data:
                    f.write("%s;%s\n" % (w, val))
