import requests

base_url = 'http://localhost:8001'
random_joke_url = f'{base_url}/random_joke'
jokes_by_category_url = f'{base_url}/jokes_by_category'


def test_get_random_joke():
    response = requests.get(random_joke_url)
    assert response.status_code == 200
    assert 'joke' in response.json() or 'setup' in response.json()


def test_get_jokes_by_category():
    category = "Programming"
    response = requests.get(f"{jokes_by_category_url}/{category}")
    assert response.status_code == 200
    assert len(response.json()) > 0
