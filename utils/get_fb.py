from requests import get

req = get('https://gpsvista-55ca2-default-rtdb.firebaseio.com/.json')

key = req.json()['key'].strip()