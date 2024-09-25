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

## Running the Server on Testing/Production Mode

For testing/production, the environment variables are configured via Kubernetes.

1. Provide the rest of the necessary environment variables in Kubernetes. See ```.env.template``` for an example. 

2. Run the uvicorn webserver:
    ```bash
    uvicorn app.main:app --reload --host <HOST IP ADDRESS> --port 8000
    ```