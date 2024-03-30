# `CarlAdam`: Petri net tools and interactive simulator for Python

## What is a Petri net?

Petri nets are a mathematical modeling scheme for the description of distributed systems.

Petri nets were invented in 1962 by Carl Adam Petri.
They have been used to model various kinds of systems,
including computer networks, manufacturing systems, and biological systems.

## What is `CarlAdam`?

`CarlAdam` is a Python library for working with Petri nets, named after their inventor.
It provides a simple, Python-oriented API for defining and executing Petri nets.

It is also a simulator for Petri nets, so you can run your Petri net models and see how they behave.

## Getting started

Check out the examples using the simulator:

```shell
poetry install --with=simulator
make simulator
```

Or use Docker:

```shell
docker compose up
```

Then browse to http://localhost:8000 to see the simulator in action.

## Sponsors

Initial work on the CarlAdam package was sponsored by [Routable](https://routable.com/).
