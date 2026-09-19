from __future__ import annotations
from fastapi.testclient import TestClient


def test_add_game(client: TestClient):
    payload = {
        "title": "Cyberpunk 2077",
        "genre": "RPG",
        "platform": "PC",
        "rating": 9.8,
        "released": 2020,
        "description": "Best game oat"
    }

    response = client.post("/games", json=payload)
    assert response.status_code == 200

    data = response.json()  
    assert data["title"] == "Cyberpunk 2077"
    assert data["genre"] == "RPG"
    assert data["platform"] == "PC"
    assert data["rating"] == 9.8
    assert data["released"] == 2020
    assert data["description"] == "Best game oat"


def test_get_games_when_empty(client: TestClient):
    response = client.get("/games")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_games_if_not_empty(client: TestClient):
    payload = {
            "title": "Cyberpunk 2077",
            "genre": "RPG",
            "platform": "PC",
            "rating": 9.8,
            "released": 2020,
            "description": "Best game oat"
        }

    client.post("/games", json=payload)
    response = client.get("/games")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_game_if_game_exists(client: TestClient):
    payload = {
        "title": "Cyberpunk 2077",
        "genre": "RPG",
        "platform": "PC",
        "rating": 9.8,
        "released": 2020,
        "description": "Best game oat"
    }
    
    create_res = client.post("/games", json=payload)
    game_id = create_res.json()["_id"]
    response = client.get(f"games/{game_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Cyberpunk 2077"
    assert data["_id"] == game_id


def test_get_game_if_not_found(client: TestClient):
    game_id = "111111111111111111111111"
    response = client.get(f"games/{game_id}")
    assert response.status_code == 404


def test_delete_game(client: TestClient):
    payload = {
        "title": "Cyberpunk 2077",
        "genre": "RPG",
        "platform": "PC",
        "rating": 9.8,
        "released": 2020,
        "description": "Best game oat"
    }
    
    create_res = client.post("/games", json=payload)
    game_id = create_res.json()["_id"]
    response = client.delete(f"/games/{game_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Game deleted"
    

def test_delete_game_if_not_found(client: TestClient):
    game_id = "111111111111111111111111"
    response = client.delete(f"games/{game_id}")
    assert response.status_code == 404


def test_update_game_if_found(client: TestClient):
    payload = {
        "title": "Cyberpunk 2077",
        "genre": "RPG",
        "platform": "PC",
        "rating": 9.8,
        "released": 2020,
        "description": "Best game oat"
    }
    
    create_res = client.post("/games", json=payload)
    game_id = create_res.json()["_id"]

    updated_payload = {
        "title": "Minecraft",
        "genre": "Open-world sandbox",
        "platform": "Cross-platform",
        "rating": 9.9,
        "released": 2009,
        "description": "Nostalgia"
    }

    response = client.put(f"/games/{game_id}", json=updated_payload)
    assert response.status_code == 200

    data = response.json()  
    assert data["message"] == "Game updated"


def test_update_game_if_not_found(client: TestClient):
    updated_payload = {
            "title": "Minecraft",
            "genre": "Open-world sandbox",
            "platform": "Cross-platform",
            "rating": 9.9,
            "released": 2009,
            "description": "Nostalgia"
        }
    
    game_id = "111111111111111111111111"
    response = client.put(f"games/{game_id}", json=updated_payload)
    assert response.status_code == 404