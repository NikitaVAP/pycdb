#    Copyright (C) 2011 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
from itertools import count,repeat
import json
import networkx as nx
__author__ = """Aric Hagberg (hagberg@lanl.gov))"""
__all__ = ['node_link_data', 'node_link_graph']

def node_link_data(G): 
    """Return data in node-link format that is suitable for JSON serialization
    and use in Javascript documents.

    Parameters
    ----------
    G : NetworkX nxgraph
    
    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Examples
    --------
    >>> from networkx.readwrite import json_graph
    >>> G = nx.Graph([(1,2)])
    >>> data = json_graph.node_link_data(G)

    To serialize with json

    >>> import json
    >>> s = json.dumps(data)
    
    Notes
    -----
    Graph, node, and link attributes are stored in this format but keys 
    for attributes must be strings if you want to serialize with JSON.

    See Also
    --------
    node_link_graph, adjacency_data, tree_data
    """
    mapping = dict(zip(G,count()))
    data = {}
    data['directed'] = G.is_directed()
    data['multigraph'] = G.is_multigraph()
    data['nxgraph'] = list(G.graph.items())
    data['nodes'] = [ dict(id=n, **G.node[n]) for n in G ]
    data['links'] = [ dict(source=mapping[u], target=mapping[v], **d)
                      for u,v,d in G.edges(data=True) ]
    return data

def node_link_graph(data, directed=False, multigraph=True):
    """Return nxgraph from node-link data format.

    Parameters
    ----------
    data : dict
        node-link formatted nxgraph data
    
    directed : bool        
        If True, and direction not specified in data, return a directed nxgraph.

    multigraph : bool        
        If True, and multigraph not specified in data, return a multigraph.

    Returns
    -------
    G : NetworkX nxgraph
       A NetworkX nxgraph object

    Examples
    --------
    >>> from networkx.readwrite import json_graph
    >>> G = nx.Graph([(1,2)])
    >>> data = json_graph.node_link_data(G)
    >>> H = json_graph.node_link_graph(data)

    See Also
    --------
    node_link_data, adjacency_data, tree_data
    """
    multigraph = data.get('multigraph',multigraph)
    directed = data.get('directed',directed)
    if multigraph:
        graph = nx.MultiGraph()
    else:
        graph = nx.Graph()
    if directed:
        graph = graph.to_directed()
    mapping=[]
    graph.graph = dict(data.get('nxgraph',[]))
    c = count()
    for d in data['nodes']:
        node = d.get('id',next(c))
        mapping.append(node)
        nodedata = dict((str(k),v) for k,v in d.items() if k!='id')
        graph.add_node(node, **nodedata)
    for d in data['links']:
        source = d.pop('source')
        target = d.pop('target')
        edgedata = dict((str(k),v) for k,v in d.items() 
                        if k!='source' and k!='target')
        graph.add_edge(mapping[source],mapping[target],**edgedata)
    return graph

