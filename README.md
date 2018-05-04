# Q&A Bot
From project description:

There are so many forums out there where people answer each other’s questions.
Do we really still need people to do that? Aren't most questions answered
already? For some topics it sure feels like all questions must have been
answered by now. By eliminating the need for human interaction, your answer
should be available way quicker! The idea behind this project is to create a
page where you state your question and get an automatic answer (within a
specific area) automatically, by indexing questions and answers already written
by others in a forum.

The assignment:
* Fetch questions and answers ( I have a large batch of familjeliv.se data
  collected that can be used).
* Use elasticsearch ( https://github.com/elastic/elasticsearch), or another
  search engine of your choice, to index the questions and answers.
* Build a query analyzer that can help you create a query to your search engine
  by, for example, selecting the most important words, or comparing the entir
  e question to questions in the index.
* Query your search engine and select the best answer available.
* Present answer in a web interface.

An interesting extension is to try to devise a scoring function that determines
how sure the system is of the answer.

## Project structure
[indexer/](indexer/) contains the part that reads raw data and puts it in
Elasticsearch.

[server/](server/) contains the actual searcher, it also contains
some form of http-server in order to be able to communicate with the client.

[client/](client/) contains the front-end that connects to the server and
displays the answer to a given question.

[report/](report/) contains the report (for now written in LaTeX)

## Docker
Docker should be able to help us run things without getting weird dependency
bugs. Setting up docker and running the hello world takes 30 minutes at most.
[This page](https://docs.docker.com/get-started/part2/) was very helpful in
explaining how to write Dockerfiles and how to run containers.

## Compile
To compile with docker-compose one can issue the command `docker-compose build <packagename>`.  In order to build everything just leave out the package name.

## Elasticsearch
To get Elasticsearch up and running install docker-compose and issue the command:
```
docker-compose start elasticsearch
```
in the root of the project (where the docker-compose.yml file is).

Note: The `start` command might not work first time running the docker-compose,
in that case try `docker-compose up -d elasticsearch`.

## Run indexer
To run indexer, make sure that Elasticsearch container is running.  This can be
done by issuing `docker ps`.

To index questions from the file `resources/Questions.csv` run `docker-compose run --rm indexer q`

To index answers from the file `resources/Answers.csv `run `docker-compose run --rm indexer a`

Note the `--rm` this flag is present so that docker does not create
one container per execution but removes it after indexer has shut down.
