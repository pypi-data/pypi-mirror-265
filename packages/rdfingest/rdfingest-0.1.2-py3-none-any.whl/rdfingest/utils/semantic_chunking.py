"""Functionality for 'semantic chunking' of Graphs and Datasets."""

from collections.abc import Iterator

from rdflib import Dataset, Graph, URIRef
from more_itertools import ichunked


def semantic_chunk_graph(
        graph: Graph,
        triple_chunk_size: int = 1000,
        skolem_basepath: str | URIRef | None = None
) -> Iterator[Graph]:
    """Perform 'semantic chunking' on a graph.

    The input graph gets chunked into n graphs of (at most) triple_chunk_size triples each.

    Warning: The operation performs skolemization, so blank nodes are resolved with URIs.
    This is necessary to not lose connections between chunked graphs.
    The namespace for auto-generated URIs can be configured by setting skolem_basepath.
    """
    _graph_id = graph.identifier
    skolemized_graph = graph.skolemize(basepath=skolem_basepath)
    triple_chunks = ichunked(
        skolemized_graph.triples((None, None, None)),
        triple_chunk_size
    )

    for chunk in triple_chunks:
        g = Graph(identifier=_graph_id)
        for triple in chunk:
            g.add(triple)
        yield g


def semantic_chunk_dataset(
        dataset: Dataset,
        triple_chunk_size: int = 1000,
        skolem_basepath: str | URIRef | None = None
) -> Iterator[Dataset]:
    """Perform 'semantic chunking' on a dataset.

    The input dataset of n contexts gets chunked into n datasets of 1 context each
    holding (at most) triple_chunk_size triples each.

    E.g. a dataset with 2 namedgraphs of 10 triples each gets chunked into
    4 datasets with 1 namedgraph each holding 5 triples if triple_chunk_size is set to 5.

    Note that the operation performs skolemization, i.e. blank nodes are resolved with URIs.
    See the 'semantic_chunk_graph' function.
    """
    for graph in dataset.contexts():
        chunk_graphs = semantic_chunk_graph(
            graph=graph,
            triple_chunk_size=triple_chunk_size,
            skolem_basepath=skolem_basepath
        )

        for chunk_graph in chunk_graphs:
            d = Dataset()
            d.graph(chunk_graph)
            yield d
