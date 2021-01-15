# Readme for Kodilla task 9.4 - REST API
This API has list of episodes of "The Mandalorian" series as JSON.

Required liblaries are mentioned in requirements.txt
To install basick requrements use "pip install -r requirements.txt" command.
Just in case I added requirements_all.txt for full view.

To run the application based on JSON use app.py file.
To run the application based on SQLite use app_db.py file.

Main page (really just JSON overview) might be on below address.
> <http://127.0.0.1:5000/api/v2/mando/>

An episode page (view/delete/update) might be on below address. Where at the end number represents an id (episode number).
> <http://127.0.0.1:5000/api/v2/episode/1>

An episode of the series has data as below, stored as JSON:
- "id"
- "title"
- "description"
- "viewed"

Main page might be on below address. Main page will load all data from "episodes" table.
> <http://127.0.0.1:5000/api/mando/epi/>

An episode page (view/delete/update) might be on below address. Where at the end number represents an id (episode number).
> <http://127.0.0.1:5000/api/mando/epi/1>


Tasks overview page might be on below address. Page will load all data from "tasks" table.
> <http://127.0.0.1:5000/api/mando/task/>

A task page (view/delete/update) might be on below address. Where at the end number represents an id (task id number).
> <http://127.0.0.1:5000/api/mando/task/1>


Tasks might be vievewd by status (open/done) on below address. Where at the end type status eg. "open".
> <http://127.0.0.1:5000/api/mando/task/done>


Delete all data (from "tasks" & "episodes" tables at once) might be on below address. methods=['DELETE']
> <http://127.0.0.1:5000/api/mando/delete/>


It is possible to restore JSON data in to SQLite by using below address.
It is not posiible to store data from SQLite into JSON from app_db.py.
> <http://127.0.0.1:5000/api/mando/restore/>


:)
