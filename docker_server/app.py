from flask import Flask, jsonify, request, session
import docker_runner

app = Flask(__name__)
app.secret_key = b'AT3stStr1ng'

@app.route("/")
def hello():
    return jsonify(msg="Hello World!")

@app.route("/wargame/<int:wargame_id>", methods=['GET'])
def request_info(wargame_id):
    """
    워게임 정보를 받는다.
    :wargame_id: int
    :return: {title:string, context:string}
    """
    if wargame_id == 1:
        return jsonify(
            title="Web Shell 탐지"
            ,context="주어진 웹 쉘이 있는지 탐지하자.")
    if wargame_id == 2:
        return jsonify(
            title="Remote Buffer Overflow"
            ,context="원격 버퍼 오버플로우 공격을 방어하자.")

@app.route("/wargame/start", methods=['POST'])
def request_start():
    """
    워게임 시작을 요청한다.
    :wargame_id: int
    :return: {msg:string}
    """
    wargame_id = int(request.json['wargame_id'])
    return jsonify(msg="Requested to start : {}".format(wargame_id))

@app.route("/score", methods=['GET'])
def get_score():
    """
    현재 자신의 점수를 받는다.
    """
    pass

@app.route("/is_running", methods=['GET'])
def is_running():
    """
    현재 워게임을 진행 중인지 확인한다.
    """
    pass