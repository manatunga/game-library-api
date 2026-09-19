from fastapi import APIRouter, HTTPException
from models import Game
from database import games_collection
from bson import ObjectId

router = APIRouter()

@router.get("/games")
def get_games():
    games = list(games_collection.find())
    for game in games:
        game["_id"] = str(game["_id"])
    return games

@router.get("/games/{id}")
def get_game(id: str):
    game = games_collection.find_one({"_id": ObjectId(id)})
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game["_id"] = str(game["_id"])
    return game

@router.post("/games")
def add_game(game: Game):
    new_game = dict(game)
    result = games_collection.insert_one(new_game)
    new_game["_id"] = str(result.inserted_id)
    return new_game

@router.delete("/games/{id}")
def delete_game(id: str):
    result = games_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message": "Game deleted"}

@router.put("/games/{id}")
def update_game(id: str, game: Game):
    result = games_collection.update_one(
        {"_id": ObjectId(id)}, 
        {"$set": dict(game)}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"message":"Game updated"}