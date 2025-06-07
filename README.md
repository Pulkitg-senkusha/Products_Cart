# Products_Cart

Docker for local:
docker build -t intern/python-demo3 --build-arg APP_NAME="Hello_Senkusha" .


docker run -p 8000:8000 --env-file .env intern/python-demo3


docker run -p 8000:8000 --env-file .env 8e0da40c99d3

For docker hub:

docker build -t pulkitgsenkusha/test1:v1.0.0 --build-arg APP_NAME="HelloInterns_Senkusha" .
docker images
docker push pulkitgsenkusha/test1:v1.0.0

docker pull pulkitgsenkusha/product:v1.0.0
docker run -p 8000:8000 pulkitgsenkusha/product:v1.0.0


https://hub.docker.com/repository/docker/pulkitgsenkusha/product/tags/v1.0.0/sha256-f20cf6163bf82f6b50e5d5e165a458328a562aafebaff8ae12c9788d745a78ee
