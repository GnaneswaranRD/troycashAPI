# Install docker before run the project

# build docker images
docker compose build

# create .env file
copy and paste env variables from env.sample file

# Start project
docker compose up -d

# Hit this url URL = http://localhost:9001/

# Stop project
docker compose down
