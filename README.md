# PVD Server 

REST Server of the PSGC lookup. 
>
- Version 2023_Q4


## Running the Server on Development Mode
0. (Do this only once) Create the Python virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

1. Make sure to set the appropriate version in your local `.env` file. An `.env.template` is available for your reference.

1. Run the uvicorn webserver:
    ```bash
    uvicorn app.main:app
    ```

## Running the Server in a Container


1. **Build the Docker image**:

   ```bash
   docker build -t myapp .
   ```

2. **Run the container**:

   ```bash
   docker run -d -p 8000:8000 --name myapp-container myapp
   ```

   If you want to override or add environment variables directly during the run, you can do so using the `-e` flag:

   ```bash
   docker run -d -p 8000:8000 --name myapp-container -e SOME_ENV_VARIABLE=value myapp
   ```



## Running the Server on Testing/Production Mode

For testing/production, the environment variables are configured via Kubernetes.

1. Provide the rest of the necessary environment variables in Kubernetes. See ```.env.template``` for an example. 

2. Run the uvicorn webserver:
    ```bash
    uvicorn app.main:app --reload --host <HOST IP ADDRESS> --port 8000
    ```