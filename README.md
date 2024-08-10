
#### Overview
PyFast is a server-side application built with FastAPI, featuring a set of endpoints for user management. It also includes tests to verify the functionality of the API and its schemas.

#### Project Structure
The project is organized as follows:

- `test_pyfast.py` – Tests for verifying API functionality.
- `main.py` – File for starting the server.

#### Installation

1. Clone the repository:
    ```
    git clone <repository_url>
    cd <repository_folder>
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

#### Running the Server
To start the server, use one of the following commands:

```
uvicorn main:app --reload
```


#### API

##### Endpoints

- **GET /api/users/{user_id}**: Return a fake user.
- **POST /api/users**: Creates a new fake user. 
- **PUT /api/users/{user_id}**: Update fake user

You can see more info in Swagger Documentation http://127.0.0.1:8000/dosc

##### Example Requests

- **Get Users**:
    ```curl -X 'GET' \
  'http://127.0.0.1:8000/api/users/1723240738' \
  -H 'accept: application/json'
    ```

- **Create User (JSON)**:
    ```
    curl -X 'POST' \
  'http://127.0.0.1:8000/api/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "avatar": "string"}'
    ```
- **Update User (JSON)**:
    ```
    curl -X 'PUT' \
  'http://127.0.0.1:8000/api/users/1723240738' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "avatar": "string"}'
    ```

#### Testing
To run the tests, execute the following command:

```
pytest -sv test_pyfast.py
```

**Note:**
- Ensure that the server is running before executing the tests.
- The `test_pyfast.py` file includes both schema validation tests and API logic tests.
