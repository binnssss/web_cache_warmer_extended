# About

This is a simple tool to allow warming up of page caches.
An use case could be pre-warming the varnish cache straight after a full cache clear of a website.

# How to use

1. Add URL paths into CSV, delimited by commas.
2. Build the docker container - `docker build -t cache-warmer .`
3. To use the shell wrapper script run `./run_cache_warmer.sh https://your_site.com/ `

# Roadmap

1. Alter the script to allow either CSV based warming up of all pages or if a sitemap argument is passed into the script then it will attempt to parse the /sitemap.xml of a given site.
