# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## **Module-2**
This enhancement connects the app with Trello to fetch and update to-do items. The application can -   
- Fetch all cards from one or more lists (To Do, Doing, Done, etc.). Default pull is from all lists, can be changed by passing list names to `fetch_all_items` method.
- Create a new card, by letting the user choose list name and title of the card.
- Update status of card to Done. The update method can be changed to move card to other list by changing second parm of method `change_card_status`   


The `.env` file has four new variables. Two of these are for Trello API key and token. 
The other two variables store User Name (to fetch boards for given user) and Board Name (to fetch cards from the given board). 


Visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.  


## Module 3

### Key Dependencies
The project uses pytest as testing framework. For end to end tests, Mozilla Firefox and Gecko Driver executable (which should be placed in the root of the project). 

### Running the tests
Unit and Integration tests are present in tests folder and can be executed through the following command 

```bash
$ poetry run pytest tests
```

The end to end tests are located in tests_e2e folder and can be executed using the following comand 

```bash
$ poetry run pytest tests_e2e

## Module 4 Running through VM
During VM provisioning, all the dependencies are installed. Provisioning steps are documented in vagrantfile.

Once VM is brought up (using the command $ vagrant up), visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## **Module-5**
For Part-1 of exercise, execute following commands to build docker image and create container:  
```
$ docker build --tag todo-app . 
$ docker run -p 5000:5000 --env-file .env todo-app gunicorn --bind 0.0.0.0:5000 todo_app.app:app
```

For Part-2 (multi-stage build file), following are the commands - 

Development Image:
    
```bash
$ docker build --target development --tag todo-app:dev .
$ docker run --env-file .env -p 5100:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
```

Production Image: (application is copied to image as well, hence no need to use bind mount)

```bash
$ docker build --target production --tag todo-app:prod .
$ docker run --env-file .env -p 5000:5000 todo-app:prod

```