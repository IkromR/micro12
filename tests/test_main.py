import requests
api_url = 'http://localhost:8000'


def test_healthcheck():
    responce = requests.get(f'{api_url}/__health')
    assert responce.status_code == 200


class TestProduct:
    def test_get_empty_product(self):
        responce = requests.get(f'{api_url}/v1/product')
        assert responce.status_code == 200
        assert len(responce.json()) == 0

    def test_create_product(self):
        body = { "model": "modelTest", "name": "nameTest", "info": "infoTest" }
        responce = requests.post(f'{api_url}/v1/product', json=body)
        assert responce.status_code == 200
        assert responce.json().get("model") == "modelTest"
        assert responce.json().get("name") == "nameTest"
        assert responce.json().get("info") == "infoTestdsds"
        assert responce.json().get("id") == 0

    def test_get_product_by_id(self):
        responce = requests.get(f'{api_url}/v1/product/0')
        assert responce.status_code == 200
        assert responce.json().get("model") == "modelTest"
        assert responce.json().get("name") == "nameTest"
        assert responce.json().get("info") == "infoTest"
        assert responce.json().get("id") == 0

    def test_get_not_empty_product(self):
        responce = requests.get(f'{api_url}/v1/product')
        assert responce.status_code == 200
        assert len(responce.json()) == 1
