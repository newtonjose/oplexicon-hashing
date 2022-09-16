import requests

NUM_REQUESTS = 100
RESULTS = {
    "times": [],
    "collisions": [],
}

if __name__ == '__main__':
    for e in ['pjw', 'md4', 'md5', 'sha1', 'sha2']:
        # r = requests.get('http://localhost:8000/pjw?key=%23brandsclub')
        r = requests.get(f'http://localhost:8000/{e}')

        data = r.json()
        print(e, data['total_collisions'], data['performance_microseconds'])
