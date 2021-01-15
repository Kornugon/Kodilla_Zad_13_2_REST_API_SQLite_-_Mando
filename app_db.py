"""
Zadanie 13.2
Bazujac na zad 9.4 dodano obsuge bazy danych SQLite

restore_all_from_JSON()  to dane z JSONa
nie ma opcji zapisu do JSONa z poziomu tej appki.
"""

import os
from flask import Flask, jsonify, abort, make_response, request

from modelsSQLite import episodes



app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'developmentOnlySecretKey')



@app.errorhandler(400)
def validate_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.errorhandler(404)
def find_episode(error):
    return make_response(jsonify({'error': 'Episode or task not found', 'status_code': 404}), 404)




@app.route("/api/mando/epi/", methods=["GET"])
def get_episodes_list():
    episodes.create_connection()
    return jsonify(episodes.select_all("episodes"))


@app.route("/api/mando/task/", methods=["GET"])
def get_tasks_list():
    episodes.create_connection()
    return jsonify(episodes.select_all("tasks"))


@app.route("/api/mando/epi/<int:episode_id>", methods=["GET"])
def get_single_episode(episode_id):
    episodes.create_connection()
    episode = episodes.select_where("episodes", id=episode_id)
    if not episode:
        abort(404)
    return jsonify({"episode": episode})


@app.route("/api/mando/task/<int:id>", methods=["GET"])
def get_single_task(id):
    episodes.create_connection()
    task = episodes.select_where("tasks", id=id)
    if not task:
        abort(404)
    return jsonify({"task": task})


@app.route("/api/mando/task/<status>", methods=["GET"])
def get_task_by_status(status):
    episodes.create_connection()
    episodes.select_task_by_status(status)

    task = episodes.select_where("tasks", status=status)
    if not task:
        abort(404)
    return jsonify({"task": task})


@app.route("/api/mando/epi/<int:episode_id>", methods=["PUT"])
def update_episode(episode_id):
    episodes.create_connection()
    episode = episodes.select_where("episodes", id=episode_id)
    episode = episode[0]
    if not episode:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'id' in data and not isinstance(data.get('id'), int),
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
    ]):
        abort(400)

    title = data.get('title', episode[1])
    description = data.get('description', episode[2])
    
    episodes.update("episodes", id=episode_id, title=title, description=description)
    return jsonify({'episode': episode})


@app.route("/api/mando/task/<int:id>", methods=["PUT"])
def update_task(id):
    episodes.create_connection()
    tasks = episodes.select_where("tasks", id=id)
    tasks = tasks[0]
    if not tasks:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'id' in data and not isinstance(data.get('id'), int),
        'episode_id' in data and not isinstance(data.get('episode_id'), int),
        'task' in data and not isinstance(data.get('task'), str),
        'task_description' in data and not isinstance(data.get('task_description'), str),
        'status' in data and not isinstance(data.get('status'), str),
        'start_date' in data and not isinstance(data.get('start_date'), str),
        'end_date' in data and not isinstance(data.get('end_date'), str)
        ]):
        abort(400)

    episode_id = data.get('episode_id', tasks[1])
    task = data.get('task', tasks[2])
    task_description = data.get('task_description',tasks[3])
    status = data.get('status', tasks[4])
    start_date = data.get('start_date', tasks[5])
    end_date = data.get('end_date', tasks[6])
    
    episodes.update("tasks", id=id, episode_id=episode_id, task=task, task_description=task_description, status=status, start_date=start_date, end_date=end_date)
    return jsonify({'task': tasks})


@app.route("/api/mando/epi/<int:episode_id>", methods=['DELETE'])
def delete_episode(episode_id):
    episodes.create_connection()
    episodes.delete_where("tasks", episode_id=episode_id)
    result = episodes.delete_where("episodes", id=episode_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/mando/task/<int:id>", methods=['DELETE'])
def delete_task(id):
    episodes.create_connection()
    result = episodes.delete_where("tasks", id=id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/mando/delete/", methods=['DELETE'])
def delete_all():
    episodes.create_connection()
    episodes.delete_all("tasks")
    result = episodes.delete_all("episodes")
    if not result:
        abort(404)
    return jsonify({'result': "Tables episodes and tasks cleared"})


@app.route("/api/mando/restore/", methods=["GET"])
def restore_all_from_JSON():
    episodes.create_connection()
    result = episodes.load_episodes_JSON_backup()
    return jsonify({'result': result})






if __name__ == "__main__":

    create_episodes_sql = """
    -- episodes table
    CREATE TABLE IF NOT EXISTS episodes (
      id integer PRIMARY KEY,
      title text NOT NULL,
      description text NOT NULL
        );
    """

    create_tasks_sql = """
    -- tasks table
    CREATE TABLE IF NOT EXISTS tasks (
        id integer PRIMARY KEY,
        episode_id integer NOT NULL,
        task VARCHAR(250) NOT NULL,
        task_description TEXT,
        status VARCHAR(15) NOT NULL,
        start_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (episode_id) REFERENCES episodes (id)
    );
    """

    conn = episodes.create_connection()
    episodes.execute_sql(create_episodes_sql)
    episodes.execute_sql(create_tasks_sql)
    conn.close()

    app.run(debug=True)