## On Startup
Set the path variable to the root directory of the repo
```
export PYTHONPATH=$(pwd)
```

## Start FastAPI server locally
```
fastapi dev app.py
```

## To test Frontend Changes
1. Create an account with a personal email, and verify it. 
2. Fill in this bash script with the correct details: ```
    #!/bin/bash

    # Define the endpoint, username, and password
    URL="https://backend-dot-cardmath-llc.uc.r.appspot.com/token"
    USERNAME="your@email.com"
    PASSWORD="password"

    # Perform the POST request to login and extract the access_token
    ACCESS_TOKEN=$(curl -s -X POST "$URL" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=$USERNAME" \
    -d "password=$PASSWORD" | jq -r '.access_token')

    # Check if the token was extracted successfully
    if [[ "$ACCESS_TOKEN" != "null" && -n "$ACCESS_TOKEN" ]]; then
    echo "localStorage.setItem('cardmath_access_token', '$ACCESS_TOKEN');"
    else
    echo "Failed to retrieve access token. Please check your credentials or server status."
    fi
    ```

3. Execute the script and copy the output with ctrl+shift+c
4. Start the frontend with: 
```HTTPS=true npm start ```
5. Open the browser console and paste the command ex:
``localStorage.setItem('cardmath_access_token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqYWwyMzQwQGNvbHVtYmlhLmVkdSIsImV4cCI6MTczMjY0ODIwNX0.g2aXv02CHs0fpsQQbBNoPtP40_QITgeH4QS830B7F9A');```
6. Finished! Make changes to your local frontend and see them in action with real data
