# PokeAPI

This is a demo for a Pokémon statistics API.

The app is live! You can see it working [here](https://api--backend--szddylxwrcg5.code.run/). 
![App screenshot](https://i.imgur.com/09go2xB.png)

# How to run locally

## Requirements
- Python 3.12
- Docker Compose or everything in `requirements.txt` (and `requirements-dev.txt` if testing/developing).

## Set up
1. Clone repo:
    ```shell
    git clone https://github.com/mggp/poke_api.git
    ```
2. Move to new directory:
    ```shell
    cd poke_api
    ```
3. Set environment variables to configure project. See [the configuration section](https://github.com/mggp/poke_api/edit/main/README.md#configurations) for a complete break down.  
Sample configurations are declared in `.env.example`. These work out of the box, the fastest way to set up is to just copy them into an `.env` file for later tweaking:
    ```shell
    cp .env.example .env
    ``` 

## Using Docker Compose
To start the project for development using Docker Compose:

```shell
docker-compose up dev
```

This will start the app in development mode, automatically reloading whenever changes are made to the `/app` directory. Visit `http://localhost:8000/` to see the docs and interact with the API. 

To enable Redis caching with the provided Redis service, start both services together:
```shell
docker-compose up redis dev
```
## Using a local python installation
1. Ensure you have Python 3.12 installed.
2. Install dependencies:
    ```shell
    pip install -r requirements.txt
    ```
   For development and testing, also install:
    ```shell
    pip install -r requirements-dev.txt
    ```
3. Set up your `.env` file as described above.
4. Start the app:
    ```shell
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
5. (Optional) If you want to use Redis caching, make sure you have a Redis server running and configure the connection in your `.env` file.
6. Visit `http://localhost:8000/` to see the docs and interact with the API. 
## Running tests

### Using Docker Compose

To run the test suite with Docker Compose, use the `test` service:

```shell
docker-compose up test
```

This will build the test environment, mount the `app` and `tests` directories, and execute all tests using `pytest`. You can view the test results in your terminal. 

### Using a local python installation

1. Ensure you have installed all dependencies, including those in `requirements-dev.txt`:

    ```shell
    pip install -r requirements.txt -r requirements-dev.txt
    ```

2. Run the tests with:

    ```shell
    pytest tests
    ```

This will execute all tests in the `tests` directory.

# Environment configurations
#### POKE_API_PATH
- Use: The base URL for the PokeAPI service your app will connect to.
- Possible values: Any valid URL (e.g., https://pokeapi.co/api).

#### FLOAT_DECIMAL_PLACES
- Use: Sets how many decimal places to display for floating-point numbers. This helps keep the API readable.
- Possible values: Any integer (e.g.: 2 for two decimal places).
- If you want to disable rounding, please set it to `0`.

#### LOGGER_LEVEL
- Use: Controls the verbosity of logging output.
- Possible values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

#### REDIS_ENABLED
- Use: Enables or disables Redis caching.
- Type: `bool`

#### REDIS_DB
- Use: Specifies which Redis database index to use. Default is 0.
- Type: `int`

#### REDIS_HOST
- Use: The hostname or IP address of the Redis server.
- Possible values: Any valid hostname or IP.

#### REDIS_PORT
- Use: The port number Redis is listening on.
- Possible values: Any valid port number (default is `6379`).

#### REDIS_PASSWORD
- Use: Password for authenticating with the Redis server.
- Possible values: Any string.

#### REDIS_DEFAULT_EXPIRATION
- Use: Default time-to-live (TTL) for cached items, in seconds.
- Possible values: Any integer (e.g.: 3600 for one hour).

#### REDIS_USE_SSL 
- Use: Determines if SSL/TLS should be used for Redis connections.
- Type: `bool`
