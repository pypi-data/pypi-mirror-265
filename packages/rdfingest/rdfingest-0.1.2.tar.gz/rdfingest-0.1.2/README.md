![<img source="goku_rdf_slurp.png" width=10% height=10%>](https://raw.githubusercontent.com/lu-pl/rdfingest/main/goku_rdf_slurp.png)

# RDFIngest
![tests](https://github.com/lu-pl/rdfingest/actions/workflows/tests.yaml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/lu-pl/rdfingest/badge.svg?branch=main)](https://coveralls.io/github/lu-pl/rdfingest?branch=main)
[![PyPI version](https://badge.fury.io/py/rdfingest.svg)](https://badge.fury.io/py/rdfingest)
[![license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


RDFIngest - A simple tool for ingesting local and remote RDF data sources into a triplestore.

> WARNING: This project is in an early stage of development and should be used with caution.

## Requirements

* Python >= 3.11

## Installation
RDFIngest is availabe on PyPI:
```shell
pip install rdfingest
```

Also the RDFIngest CLI can be installed with [pipx](https://pypa.github.io/pipx/):
```shell
pipx install rdfingest
```

For installation from source either use [poetry](https://python-poetry.org/) or run `pip install .` from the package folder.

## Usage

RDFIngest reads two YAML files: 
- a config file for obtaining triplestore credentials and 
- a registry which defines the RDF sources to be ingested.

#### Example config:
```yaml
service:
  endpoint: "https://sometriplestore.endpoint"
  user: "admin"
  password: "supersecretpassword123"
```

#### Example registry:
```yaml
graphs:
  - source: https://someremote.ttl
    graph_id: https://somenamedgraph.id

  - source: [
    somelocal.ttl,
    https://someotherremote.ttl
    ]
    graph_id: https://someothernamedgraph.id
    
  - source: https://someremote.trig
  
  - source: [
    https://someotherremote.trig,
    someotherlocal.ttl,
    yetanotherremote.ttl	
    ]
    graph_id: https://yetanothernamedgraph.id
```

RDFIngest parses all registered RDF sources and ingests the data as named graphs into the specified triplestore by executing POST requests for every source.  

By default also a SPARQL DROP operation is run for every Graph ID before POSTing.  

For contextless RDF sources a `graph_id` is required, [RDF Datasets](https://www.w3.org/TR/rdf11-concepts/#section-dataset)/Quad formats obviously do not require a `graph_id` field.  

For Datasets, the default graph (at least for now) is ignored. Running automated DROP and/or POST operations on a remote default graph is considered somewhat dangerous. 
> Namespaces are one honking great idea -- let's do more of those!

The tool accepts both local and remote RDF data sources.  


#### Entry example

Consider the following entry:

```yaml
graphs:
 - source: [
    https://someremote.trig,
    somelocal.ttl,
    anotherremote.ttl	
    ]
    graph_id: https://somenamedgraph.id/
```

In this case every named graph in the Dataset `https://someremote.trig` is ingested using their respective named graph identifiers,
`somelocal.ttl` and `anotherremote.ttl` are ingested into a named graph `https://somenamedgraph.id/`.


### CLI
Run the `rdfingest` command.

```shell
rdfingest --config ./config.yaml --registry ./registry.yaml
```

Default values for config and registry are `./config.yaml` and `./registry.yaml`.

Also see `rdfingest --help`.

### RDFIngest class

Point an `RDFIngest` instance to a config file and a registry and invoke `run_ingest`.

```python
rdfingest = RDFIngest(
	config="./config.yaml"
	registry="./registry.yaml", 
	drop=True,
	debug=False
)

rdfingest.run_ingest()
```
