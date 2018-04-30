# Indexer
In order to build the indexer via docker one must first create a docker image.
This is done with the command `docker build -t indexer .` where "indexer" is
just a easy-to-read name for the image.

To run the image, issue `docker run --network qna_bot_esnet indexer` given that the name of the image
is indexer.
