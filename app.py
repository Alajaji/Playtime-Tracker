import os
import time
import datetime
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc, func, desc
import json
from flask_cors import CORS

from models import setup_db, Playtime, Genre, Player
from auth import AuthError, requires_auth



app = Flask(__name__)
setup_db(app)
CORS(app)


# convert string time hh:mm to seconds
def to_seconds(time_str):
    split = time_str.split(':')
    hour = int(split[0])
    min = int(split[1])
    total = hour * 3600 + min * 60
    return total

# convert int seconds to string time hh:mm


def from_second(time_str):
    return str(datetime.timedelta(seconds=time_str))


def get_player_id(name):
    player = Player.query.filter(
        Player.name.ilike(name)).all()
    if len(player) < 1:
        new_player = Player(name=name)
        new_player.insert()
        player_id = new_player.id
    else:
        player_id = player[0].id
    return player_id


"""
POST /playtime
    Creates new record in Playtime table.
    If player does not exist it will create player and add playtime
    takes JSON body:
        {
            "game": "Game name",
            "player": "Player name",
            "playtime": "hh:mm",
            "genre": "Action"  
        }
"""


@app.route("/playtime", methods=["POST"])
@requires_auth(permissions="post:playtime")
def create_playtime(payload):
    try:
        body = request.get_json()

        new_game = body.get("game", None)
        if new_game is None:
            return jsonify({"success": False, "error": 400, "message": "Game name was not provided."}), 400

        player_name = body.get("player", None)
        if player_name is None:
            return jsonify({"success": False, "error": 400, "message": "Player name was not provided."}), 400

        player_id = get_player_id(player_name)

        playtime = body.get("playtime", None)
        if playtime is None:
            return jsonify({"success": False, "error": 400, "message": "playtime time was not provided."}), 400
        playtime = to_seconds(playtime)

        new_genre = body.get("genre", None)
        playtime = Playtime(
            game=new_game, player_id=player_id, playtime=playtime, genre=new_genre)

        playtime.insert()

        return jsonify(
            {
                "success": True,
                "Game Added": playtime.format()
            }
        )
    except Exception as e:
        print(e)
        abort(400)


"""
GET /playtimes
    Gets all playtimes records.
"""


@app.route("/playtimes", methods=["GET"])
@requires_auth(permissions="get:playtimes")
def get_all_playtimes(payload):
    try:
        data = []
        all_play = {}
        playtimes = Playtime.query.all()
        if len(playtimes) < 1:
            return jsonify({"success": False, "error": 404, "message": "No playtimes found"}), 404
        for playtime in playtimes:
            all_play = playtime.format()
            data.append(all_play)
        return jsonify(
            {
                "success": True,
                "Playtimes": data
            }
        )
    except Exception as e:
        print(e)
        abort(422)


"""
GET /playtime/id
    Gets total playtime time for all games for id player.
"""


@app.route("/playtime/<int:player_id>", methods=["GET"])
@requires_auth(permissions="get:playtime/id")
def get_playtime(payload, player_id):
    try:
        total_time = 0
        playtime = Playtime.query.filter(
            Playtime.player_id == player_id).all()
        if len(playtime) < 1:
            return jsonify({"success": False, "error": 404, "message": "There is no Player with id  {}".format(player_id)}), 404
        for time in playtime:
            total_time = total_time + time.playtime
        return jsonify(
            {
                "success": True,
                "Your total gaming time is": from_second(total_time)
            }
        )
    except Exception as e:
        print(e)
        abort(422)


"""
GET /most-playtime
    Gets most played game for all players.
"""


@app.route("/most-playtime", methods=["GET"])
@requires_auth(permissions="get:most-playtime")
def get_most_played(payload):
    try:
        playtimes = Playtime.query.with_entities(Playtime.game, func.sum(
            Playtime.playtime).label("total_playtime")).group_by(Playtime.game).order_by(desc("total_playtime")).all()
        print(playtimes)
        if len(playtimes) < 1:
            return jsonify({"success": False, "error": 404, "message": "There is no play times added"}), 404

        return jsonify(
            {
                "success": True,
                "Most played game": playtimes[0][0],
                "Time played": from_second(playtimes[0][1])
            }
        )
    except Exception as e:
        print(e)
        abort(422)


"""
DELETE /playtime/<int:p_id>
    Deletes playtime record.
"""


@app.route("/playtime/<int:p_id>", methods=["DELETE"])
@requires_auth(permissions="delete:playtime")
def delete_playtime(payload, p_id):
    try:
        del_playtime = Playtime.query.filter(
            Playtime.id == p_id).one_or_none()
        if del_playtime is None:
            return jsonify({"success": False, "error": 404, "message": "Playtime id was not found."}), 404

        del_playtime.delete()

        return jsonify(
            {
                "success": True,
                "Playtime ID": del_playtime.id,
            }
        )
    except Exception as e:
        print(e)
        abort(422)


"""
PATCH /playtime/<int:p_id>
    Updates playtime record. 
    accepts json:
        {
            "game": "Phynix",
            "playtime": "10000:40",
            "genre": "Shooter"  
        }
"""


@app.route("/playtime/<int:p_id>", methods=["PATCH"])
@requires_auth(permissions="patch:playtime")
def update_playtime(payload, p_id):
    try:
        body = request.get_json()

        upt_playtime = Playtime.query.filter(Playtime.id == p_id).one_or_none()
        if upt_playtime is None:
            return jsonify({"success": False, "error": 404, "message": "Playtime id was not found."}), 404
        if body.get("game", None) != None:
            upt_playtime.game = body.get("game", None)
        if body.get("genre", None) != None:
            upt_playtime.genre = body.get("genre", None)
        if body.get("playtime", None) != None:
            upt_playtime.playtime = to_seconds(body.get("playtime", None))

        upt_playtime.update()

        return jsonify(
            {
                "success": True,
                "Playtime updated": upt_playtime.format(),
            }
        )
    except Exception as e:
        print(e)
        abort(422)


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404,
                 "message": "resource not found"}),
        404,
    )


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"success": False, "error": 401, "message": "Un authorized"}), 401


@app.errorhandler(AuthError)
def auth_error(auth):
    return (
        jsonify({"success": False, "error": auth.status_code,
                 "message": auth.error}),
        auth.status_code,
    )


if __name__ == '__main__':
    app.run()
