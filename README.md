# Build image and start cotainer

* Modify .env file
* Run command: ```docker compose --env-file .env up --detach```

# Stop container

* Run command: ```docker compose --env-file .env stop && docker compose --env-file .env rm -f```

# Remove container

* Run command: ```docker compose --env-file .env rm -f```
