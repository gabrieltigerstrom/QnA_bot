Server
===

## Overview

Searcher supply 2 mode of searching:
* elasticsearch searching: by designing the queries manually, get the related
  queries in ES
* Infersent searching: 
  * Phase I: use elasticsearch simple query to filter possible candidates
  * Phase II: use Infersent to embed the queries into distributional vector space

## Experiment
Can we use general sentence embedding (trained offline) with simple query to achieve the same
performance with well-designed elasticsearch query (just my thought 😉)

## Reference

* [Infersent](https://github.com/facebookresearch/InferSent)
