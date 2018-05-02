# Indexer
In order to build the indexer via docker one must first create a docker image.
This is done with the command `docker build -t indexer .` where "indexer" is
just a easy-to-read name for the image.

To run the image, issue `docker run --rm --network qna_bot_esnet indexer` given that the name of the image
is indexer.

If we want to pipe someting into indexer we can issue the command ` docker run --rm -i --network qna_bot_esnet indexer < infile` where `infile` is the file you would like to pipe into the program.
