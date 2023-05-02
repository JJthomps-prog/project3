import json
from flask import Flask, request, jsonify
from threading import Lock
import secrets
import datetime
import re


posts = []
users = []
posts2 = []
lock = Lock()
app = Flask(__name__)


@app.route('/post', methods=['POST'])
def create_post():
    # check if request body is JSON
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # get message from request body
    msg = request.json.get('msg')

    # check if message field is present and is a string
    if not msg or not isinstance(msg, str):
        return jsonify({"error": "Request body must contain a string-valued 'msg' field"}), 400

    # generate random key and id
    key = secrets.token_hex(16)
    id = len(posts) + 1

    # get current timestamp in ISO 8601 format
    timestamp = datetime.datetime.utcnow().isoformat()

    # create new post and add it to the list
    post = {"id": id, "key": key, "timestamp": timestamp, "msg": msg}
    posts.append(post)

    # return response with new post details
    return jsonify(post), 200


@app.route('/post/<int:id>', methods=['GET'])
def read_post(id):
    with lock:
        # find post with given id
        post = next((p for p in posts if p["id"] == id), None)

        # return error if post is not found
        if post is None:
            return jsonify({"error": "Post not found"}), 404

        # create response JSON object
        response = {"id": post["id"], "timestamp": post["timestamp"], "msg": post["msg"]}

        # return response
        return jsonify(response)


@app.route('/post/<int:id>/delete/<string:key>', methods=['DELETE'])
def delete_post(id, key):
    with lock:
        # find post with given id
        post = next((p for p in posts if p["id"] == id), None)

        # return error if post is not found
        if post is None:
            return jsonify({"error": "Post not found"}), 404

        # return error if key is incorrect
        if post["key"] != key:
            return jsonify({"error": "Incorrect key"}), 403

        # remove post from list
        posts.remove(post)

        # create response JSON object
        response = {"id": post["id"], "key": post["key"], "timestamp": post["timestamp"]}

        # return response
        return jsonify(response)


@app.route('/post/search', methods=['POST'])
def search_posts():
    # get start and end timestamps from query parameters
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    print(end_time)

    # check if timestamps are present and in the correct format
    if not end_time:
        return jsonify({"error": "At least one end_time must be provided"}), 400
    try:
        if start_time:
            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        if end_time:
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        if start_time and end_time < start_time:
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid timestamp format"}), 400

    # search for posts within the given time range
    results = []
    with lock:
        for post in posts:
            post_time = datetime.datetime.fromisoformat(post["timestamp"])
            if (not start_time or post_time >= start_time) and (post_time <= end_time):
                results.append(post)
        for post in posts2:
            post_time = datetime.datetime.fromisoformat(post["timestamp"])
            if (not start_time or post_time >= start_time) and (post_time <= end_time):
                results.append(post)

    # return list of matching posts
    return jsonify(results)


@app.route('/user', methods=['POST'])
def create_user():
    # check if request body is JSON
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # get username and realname from request body
    username = request.json.get('username')
    realname = request.json.get('realname')

    if not username or not isinstance(username, str):
        return jsonify({"error": "Must have a string-valued username"}), 400

    for user_info in users:
        if username in user_info.values():
            return jsonify({"error": "Username must be unique"}), 400

    # generate random key and id
    key = secrets.token_hex(16)
    id = len(users) + 1

    # create new user and add it to the list
    user = {"id": id, "key": key, "username": username, "realname": realname}
    users.append(user)

    # return response with new user details
    return jsonify(user), 200


@app.route('/userinfo/<int:id>', methods=['GET'])
def get_user_by_id(id):
    with lock:
        # find user with given id
        user = next((u for u in users if u["id"] == id), None)

        # return error if user is not found
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # create response JSON object
        response = {"id": user["id"], "username": user["username"], "realname": user["realname"]}

        # return response
        return jsonify(response)


@app.route('/userinfo/<string:name>', methods=['GET'])
def get_user_by_name(name):
    with lock:
        # find user with given username
        user = next((u for u in users if u["username"] == name), None)

        # return error if user is not found
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # create response JSON object
        response = {"id": user["id"], "username": user["username"], "realname": user["realname"]}

        # return response
        return jsonify(response)


@app.route('/user_edit/<string:key>', methods=['POST'])
def edit_user(key):
    with lock:
        new_username = request.json.get('new_username')
        new_realname = request.json.get('new_realname')

        if not new_username or not isinstance(new_username, str):
            return jsonify({"error": "Must have a string-valued username"}), 400

        for user_info in users:
            if new_username in user_info.values():
                return jsonify({"error": "Username must be unique"}), 400

        for aim_user in users:
            if aim_user['key'] == key:
                aim_user['username'] = new_username
                aim_user['realname'] = new_realname
                break

        user = next((u for u in users if u["key"] == key), None)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        response = {"id": user["id"], "username": user["username"], "realname": user["realname"]}

        # return response
        return jsonify(response)


@app.route('/<string:key>/post_with_author', methods=['POST'])
def create_post_with_author(key):
    # check if request body is JSON
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # get message from request body
    msg = request.json.get('msg')

    # check if message field is present and is a string
    if not msg or not isinstance(msg, str):
        return jsonify({"error": "Request body must contain a string-valued 'msg' field"}), 400

    # get user info from users list
    user_info = next((u for u in users if u["key"] == key), None)
    author = user_info['username']

    # generate random key and id
    post_key = secrets.token_hex(16)
    id = len(posts2) + 1

    # get current timestamp in ISO 8601 format
    timestamp = datetime.datetime.utcnow().isoformat()

    # create new post and add it to the list
    post = {"id": id, "post_key": post_key, "author": author, "author_key": key, "timestamp": timestamp, "msg": msg}
    posts2.append(post)

    # return response with new post details
    return jsonify(post), 200


@app.route('/search_post/<string:name>', methods=['GET'])
def get_posts_by_author(name):
    with lock:
        # find user with given name
        user = next((u for u in users if u["username"] == name), None)

        # return error if user is not found
        if user is None:
            return jsonify({"error": "User not found"}), 404

        response = [{"author": name}]

        for post in posts2:
            if post['author'] == name:
                response.append({"id": post["id"], "msg": post["msg"], "timestamp": post["timestamp"]})

        # return response
        return jsonify(response)


@app.route('/search_text/<string:text>', methods=['GET'])
def search_text(text):
    with lock:
        response = []

        for post in posts2:
            if re.search(text, post['msg']):
                response.append({"id": post["id"], "author": post["author"], "msg": post["msg"], "timestamp": post["timestamp"]})

        return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')
