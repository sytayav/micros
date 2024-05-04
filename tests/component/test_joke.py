import requests

base_url = 'http://localhost:8000'
add_joke_url = f'{base_url}/add_joke'
get_jokes_url = f'{base_url}/jokes'
get_joke_by_id_url = f'{base_url}/get_joke_by_id'
delete_joke_url = f'{base_url}/delete_joke'
search_jokes_url = f'{base_url}/search_jokes'


new_joke = {
    "id": 99,
    "content": "Why don't programmers like nature? It has too many bugs.",
    "category": "Programming"
}


def test_1_add_joke():
    response = requests.post(add_joke_url, json=new_joke)
    assert response.status_code == 200
    assert response.json()['content'] == new_joke['content']


def test_2_get_jokes():
    response = requests.get(get_jokes_url)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_3_get_joke_by_id():
    response = requests.get(f"{get_joke_by_id_url}/99")
    assert response.status_code == 200
    assert response.json()['id'] == 99


def test_4_search_jokes():
    search_query = "programmers"
    response = requests.get(f"{search_jokes_url}?query={search_query}")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_5_delete_joke():
    delete_response = requests.delete(f"{delete_joke_url}/99")
    assert delete_response.status_code == 200
    response = requests.get(f"{get_joke_by_id_url}/99")
    assert response.status_code == 404
