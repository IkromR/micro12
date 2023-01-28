import requests


api_url = 'http://localhost:8000'


def test_healthcheck():
    responce = requests.get(f'{api_url}/__health')
    assert responce.status_code == 200
