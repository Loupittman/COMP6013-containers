import requests
import pytest

APPLICATION_JSON = 'application/json'

CONTAINERS_CERT_PEM = 'C:\\Users\\ljp\\PycharmProjects\\COMP6013-containers\\containers\\cert.pem'

BASE = "https://localhost:5000/container/"


def test_containers():
    response = requests.get(BASE + "3081811", verify=CONTAINERS_CERT_PEM)
    assert response.ok
    assert APPLICATION_JSON in response.headers['Content-Type']
    assert response.json()['container_id'] == "3081811"

    response = requests.get(BASE + "12345hi", verify=CONTAINERS_CERT_PEM)
    assert not response.ok
    assert APPLICATION_JSON in response.headers['Content-Type']
