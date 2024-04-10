# Documentation

1. Add URL paths into CSV, delimited by commas.
2. Build the docker container - `docker build -t cache-warmer .`
3. Run the container and pass the BASE_URL `docker run -e BASE_URL=https://your_site.com  -v $(pwd)/csv/urls.csv:/app/urls.csv cache-warmer`