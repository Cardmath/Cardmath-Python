# Cardmath Monorepo
All code pertaining to https://cardmath.ai is tracked in this repository.

## Techstack Rundown
- FastAPI Python backend server
- PostgreSQL database
- ReactJS Single-Page-Application Frontend /w Create React App, Primereact Components, Primeflex CSS Utility Classes 

Both are deployed separately on Google App Engine. 

## Essential Reading
Read this before looking at the code.
- [FastAPI First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
    - Understand how API routes are defined / requests validated 
- [FastAPI Security Guide](https://fastapi.tiangolo.com/tutorial/security/)
    - Understand the basic idea of JWT / OAuth2, and how FastAPI can implement these protocols 
- [SQLAlchemy 1.4 Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/index.html)
    - Understand how to simplify database interactions and use more object oriented syntax
    - This one is a bit long, so you can skim some parts
    - Very rich in information, great general learning resource


## Local Development Prereqs
- Unix (Mac or Linux) System
- Google Cloud Command Line SDK / Tool
- [ngrok](https://dashboard.ngrok.com/get-started/setup/macos) for request tunneling
- Google Cloud SQL Auth Proxy Executable [Find OS Specific Install Here](https://cloud.google.com/sql/docs/postgres/connect-auth-proxy)
- Python 3.12.3
- NodeJS Version Manager v0.39.1 (nvm)
- NodeJS v18.20.5 (install this with nvm)
- Node Package Manager (npm) v10.8.2 

## Start FastAPI server locally
0.  
    Create a new python venv (virtual environment) with the requirements.txt file
1. 
    Set the path environment variable to the root directory of the repo
    ```
    export PYTHONPATH=$(pwd)
    ```
2. 
    Authenticate with your cardmath-llc Google account (either johannes@cardmath.ai or nickeliacin@gmail.com). Before running the below command you should set up the Google Cloud Command Line Tool and sign into the cardmath-llc project.
    ```
    gcloud auth application-default login
    ```
3. Before we start the server, we need to ensure that Google Cloud recognizes our machine. Execute this script to initiate Google Cloud SQL Auth Proxy. You will *definitely* have to adjust the path of where you installed the cloud-sql-proxy executable. Everything else should work just fine. 
    ```
    #!/bin/bash

    # Variables
    INSTANCE_NAME="cardmath-llc:northamerica-northeast2:cardmathdb"
    AUTH_PROXY_KEY="auth-proxy-key.json"
    PROXY_EXECUTABLE="../cloud-sql-proxy"
    SOCKET_DIR="/cloudsql"

    # Check if the Cloud SQL Auth Proxy executable is installed
    if ! command -v $PROXY_EXECUTABLE &> /dev/null; then
        echo "Cloud SQL Auth Proxy not found. Please install it first."
        exit 1
    fi

    # Ensure the socket directory exists
    if [ ! -d "$SOCKET_DIR" ]; then
        echo "Creating socket directory: $SOCKET_DIR"
        mkdir -p $SOCKET_DIR
    fi

    # Start the Cloud SQL Auth Proxy with Unix socket
    echo "Starting Cloud SQL Auth Proxy for instance: $INSTANCE_NAME with Unix socket"
    $PROXY_EXECUTABLE \
        --credentials-file=$AUTH_PROXY_KEY \
        --unix-socket=$SOCKET_DIR \
        $INSTANCE_NAME & 
    # Capture the process ID of the proxy
    PROXY_PID=$!

    # Provide feedback to the user
    echo "Cloud SQL Auth Proxy started. PID: $PROXY_PID"
    echo "Unix socket created at: $SOCKET_DIR/$INSTANCE_NAME"

    # Wait for user input to stop the proxy
    read -p "Press ENTER to stop the Cloud SQL Auth Proxy..."

    # Stop the proxy
    echo "Stopping Cloud SQL Auth Proxy..."
    kill $PROXY_PID
    echo "Cloud SQL Auth Proxy stopped."
    ```
    *P.S. If you get a port blocked error later on, you might have to run the following command to delete the UNIX socket. Don't worry - it is created automatically again if you run the above script.*
    ```
    rm /cloudsql/cardmath-llc:northamerica-northeast2:cardmathdb/.s.PGSQL.5432
    ```
3. 
    Start the server with two workers. One worker handles long running processes like calculating the heavy hitters, and the other worker can ingest lighter requests such as setting the user's primary email. Timeout is set to 120s because the heavy hitters computation takes quite long.
    ```
    gunicorn -w 2 -k uvicorn.workers.UvicornWorker --timeout 120 app:app
    ```
