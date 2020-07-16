# Worklogs Service
**Worklog Service** is a Restful API web service 
built on top of [ASAB Micro Framework](https://github.com/TeskaLabs/asab). 
It logs our daily working activities. 
Please refer to this [dashboard](https://github.com/ardihikaru/worklogs-dashboard)
to deploy the GUI.

### Requirements 
1. Python 3.6++
2. RedisDB 
3. [ASAB Framework](https://github.com/TeskaLabs/asab)
4. MongoDB

### How to use 
1. Install required stacks 
2. Create virtual environment: `$ python3 -m venv venv`
3. Install python libraries: `$ pip install -r requirements.txt`
4. Run RedisDB (Please add password: `bismillah`); 
    [Suggested to use this dockerized version](https://github.com/ardihikaru/flask-api/tree/master/others/redis)
5. Run MongoDB
6. Run main file with the config file (`app.conf`): `$ python app.py -c app.conf`

### Accessible APIs 
* Auth
    - `POST /auth/login`: Login and receive `access_token`
    - `GET /auth/logout`: Logout and delete (revoked/blacklisted) active `access_token`
* Users
    - `POST /users`: Register a new user 
    - `GET /users`: Get all users
    - `GET /users`: Update a specific user (with `JSON Body`); Filter by ID
    - `DELETE /users`: Delete a specific user; Filter by ID (String) or IDs (List)
* WorkLogs
    -  // TBD
    
### Contributors 
1. Muhammad Febrian Ardiansyah 
([github](https://github.com/ardihikaru), 
[gitlab](https://gitlab.com/ardihikaru), 
[bitbucket](https://bitbucket.org/ardihikaru3/))

### Important resources 
1. GIT Branching Model: https://nvie.com/posts/a-successful-git-branching-model/
2. ASAB Micro Framework: https://github.com/TeskaLabs/asab
3. AIOHTTP Mircro Framework: https://docs.aiohttp.org/en/stable/
4. AIOHTTP JWT library: https://pypi.org/project/aiohttp-jwt/
5. Route Decorator: https://pypi.org/project/aiohttp_route_decorator/0.0.1/

### License 
[MIT](https://choosealicense.com/licenses/mit/)