from flask import Flask, request, jsonify
from threading import Lock
import secrets
import datetime

from secrets import randbelow

posts = []
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

    # return list of matching posts
    return jsonify(results)

