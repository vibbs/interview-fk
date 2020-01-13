

from flask import Flask, jsonify, Request, request, Response



from models import User, Post, Reactions

CURRENT_USER = None

LATEST_USER_ID = 0

LATEST_POST_ID = 0

USER_LIST = []

POST_LIST = []

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/users/login/<id>")
def login(id):
    global CURRENT_USER
    global USER_LIST

    id = int(id)
    for user in USER_LIST:
        if id == user.id:
            CURRENT_USER = user
            return jsonify({'status' : 'ok'})

    return jsonify({'status' : 'failed'})

@app.route("/users", methods=['GET', 'POST'])
def user_controller():
    global LATEST_USER_ID
    global USER_LIST



    if request.method == 'POST':
        req_data = request.get_json()

        new_user_obj = User(id=LATEST_USER_ID, username=req_data['username'])

        USER_LIST.append(new_user_obj)

        LATEST_USER_ID += 1
        return jsonify({'status' : 'ok'})

    if request.method == 'GET':
        return jsonify([e.serialize() for e in USER_LIST])


@app.route("/users/follow/<ext_user_id>", methods=['GET'])
def user_follow(ext_user_id):
    global CURRENT_USER

    global USER_LIST

    ext_user_id = int(ext_user_id)

    for user in USER_LIST:
        if CURRENT_USER.id == user.id:
            user.follow_user(ext_user_id = ext_user_id)
            return jsonify({'status': 'ok'})

    return jsonify({'status': 'failed'})



@app.route("/posts", methods=['GET', 'POST'])
def post_controller():
    global LATEST_POST_ID
    global POST_LIST

    if request.method == 'POST':
        req_data = request.get_json()

        try :
            new_post_obj = Post(
                id =LATEST_POST_ID,
                content = req_data['content'],
                created_by= CURRENT_USER.id)


            POST_LIST.append(new_post_obj)

            LATEST_POST_ID += 1


            return jsonify({'status' : 'ok'})
        except AttributeError as ae:

            return jsonify({'status': 'failed', 'message':'No user logged in'})

    if request.method == 'GET':
        return jsonify([e.serialize() for e in POST_LIST])



@app.route("/posts/<id>/reaction/<reaction>", methods=['GET'])
def post_controller(id, reaction):
    global POST_LIST
    id = int(id)

    for post in POST_LIST:
        if id == post.id:
            post.add_reaction(reaction_type = reaction)


@app.route("/posts/<id>/comment/", methods=['POST'])
def post_controller(id):
    global POST_LIST
    global LATEST_POST_ID
    id = int(id)

    if request.method == 'POST':
        for post in POST_LIST:
            if id == post.id:

                req_data = request.get_json()
                try:
                    new_post_obj = Post(
                        id=LATEST_POST_ID,
                        content=req_data['content'],
                        created_by=CURRENT_USER.id)

                    POST_LIST.append(new_post_obj)

                    LATEST_POST_ID += 1

                    post.add_comment(new_post_obj)
                    return jsonify({'status': 'ok'})
                except AttributeError as ae:
                    return jsonify({'status': 'failed', 'message': 'No user logged in'})



if __name__ == "__main__":
    app.run()