import json
import requests

f = open('Library_Load_Testing_Data.json')

data = json.load(f)

for row in data:
    if row['type'] == 'reservation':
        url = 'http://127.0.0.1:8000/book/reservation/'
    else:
        url = 'http://127.0.0.1:8000/book/checkout/'
    data = {
        "book_id": row['book_id'],
        "member_id": row['member_id']
    }
    res = requests.post(url, data)
    res = res.json()
    print(res)


