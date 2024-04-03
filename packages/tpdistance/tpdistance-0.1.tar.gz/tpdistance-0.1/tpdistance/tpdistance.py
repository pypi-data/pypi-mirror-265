import igraph as ig
import numpy as np
from scipy import sparse
from tqdm.auto import tqdm
from collections import Counter

import cxrandomwalk as rw
import fastnode2vec

def shortestPathsTP(g, sources = None, targets=None, walk_length = 10, return_type = "matrix", progressBar = None):
    """
    Compute shortest paths TP in a graph.
    It is defined by the average lower bounds for the transition probability of the shortest paths from sources to targets.
    It is computed as the product of the inverse node degrees along the path.

    Parameters
    ----------
    g : igraph.Graph
        The graph.
    sources : list, optional
        The source vertices. If None, the shortest paths from all vertices are computed.
    targets : list, optional
        The target vertices. If None, the shortest paths to all vertices are computed.
    window_length : int, optional
        The window length.
    returnType : str, optional
        The type of the return. It can be "list", "matrix", "dict".
    progressBar : function, TQDM, bool, optional
        A progress bar. If None, no progress bar is shown.
        If function, it should receive three arguments: current, total, and label.
        If TQDM, it will use the provided TQDM progress bar.
        If bool, it will show a progress bar if True.
    Returns
    -------
    list, dict, matrix
        The shortest paths TP.

    """
    if(sources is None):
        sources = np.arange(0,g.vcount())
    if(targets is None):
        targets = np.arange(0,g.vcount())
    shortestPaths = g.get_shortest_paths(sources, to=targets, output="vpath")
    shortestTPProbabilities = np.zeros((len(sources),len(targets)))
    degrees = np.array(g.degree())
    for sourceNode in range(0,len(sources)):
        for targetNode in range(0,len(targets)):
            for path in shortestPaths[sourceNode][targetNode]:
                if(path):
                    shortestTPProbabilities[sourceNode][targetNode] += np.prod(1/degrees[path[:walk_length]])
    if(return_type == "list"):
        # return a list of [(source,target,shortestTPProbabilities),...]
        return [(sources[i],targets[j],shortestTPProbabilities[i][j]) for i in range(0,len(sources)) for j in range(0,len(targets))]
    if(return_type == "dict"):
        # return a dict of {(source,target):shortestTPProbabilities,...}
        return {(sources[i],targets[j]):shortestTPProbabilities[i][j] for i in range(0,len(sources)) for j in range(0,len(targets))}
    if(return_type == "matrix"):
        # return a matrix of shortestTPProbabilities
        return shortestTPProbabilities


def TP(g, sources = None, targets=None, window_length=10, returnType = "matrix", progressBar = None):
    """
    Compute exact TP (transition probabilities) in a graph.

    Parameters
    ----------
    g : igraph.Graph
        The graph.
    sources : list, optional
        The source vertices. If None, the shortest paths from all vertices are computed.
    targets : list, optional
        The target vertices. If None, the shortest paths to all vertices are computed.
    window_length : int, optional
        The window length.
    returnType : str, optional
        The type of the return. It can be "list", "matrix", "dict".
    progressBar : function, TQDM, bool, optional
        A progress bar. If None, no progress bar is shown.
        If function, it should receive three arguments: current, total, and label.
        If TQDM, it will use the provided TQDM progress bar.
        If bool, it will show a progress bar if True.

    Returns
    -------
    list, dict, matrix
        The shortest paths TP.

    """
    if(sources is None):
        sources = np.arange(0,g.vcount())
    if(targets is None):    
        targets = np.arange(0,g.vcount())

    A = np.array(g.get_adjacency().data)
    # by Sadamori
    deg = np.array(A.sum(axis = 1)).reshape(-1)
    P = sparse.diags(1/deg) @ A # transition matrix transposed?
    w = np.ones(window_length)
    w = w / np.sum(w)
    Pt = sparse.csr_matrix(sparse.diags(np.ones(P.shape[0]))) # diag 1
    Ps = sparse.csr_matrix(sparse.diags(np.zeros(P.shape[0]))) # empty
    for i in tqdm(range(window_length)):
        Pt = P @ Pt
        Ps = Ps + w[i] * Pt
        # print(i+1)
    degrees = np.array(g.degree())
    if(returnType == "list"):
        # return a list of [(source,target,shortestTPProbabilities),...]
        return [(sources[i],targets[j],Ps[i,j]/degrees[j]) for i in range(0,len(sources)) for j in range(0,len(targets))]
    if(returnType == "dict"):
        # return a dict of {(source,target):shortestTPProbabilities,...}
        return {(sources[i],targets[j]):Ps[i,j]/degrees[j] for i in range(0,len(sources)) for j in range(0,len(targets))}
    if(returnType == "matrix"):
        #reduce matrix to sources vs targets
        Ps = Ps[sources][:, targets]
        return Ps / degrees[targets]
    

def estimatedTP(g, sources = None, targets=None, window_length=20, walks_per_source=1_000_000,
                batch_size=10_000, returnType = "matrix", degreeNormalization=True, progressBar = None):
    """
    Compute estimated TP (transition probabilities) in a graph.
    
    Parameters
    ----------
    g : igraph.Graph
        The graph.
    sources : list, optional
        The source vertices. If None, the shortest paths from all vertices are computed.
    targets : list, optional
        The target vertices. If None, the shortest paths to all vertices are computed.
    """
    if(sources is None):
        sources = np.arange(0,g.vcount())
    if(targets is None):    
        targets = np.arange(0,g.vcount())
        targetsSet = set(targets)
    else:
        targetsSet = None
    

    vertexCount = g.vcount()
    edges = g.get_edgelist()

    agent = rw.Agent(vertexCount,edges,False)

    degrees = np.array(g.degree())

    hits = agent.walkHits(nodes=list(sources),
                      q=1.0,
                      p=1.0,
                      walksPerNode=walks_per_source,
                      batchSize=batch_size,
                      windowSize=window_length,
                      verbose=False,
                      updateInterval=1000,)
    
    totalHitsPerNode = window_length * walks_per_source

    probabilities = hits / totalHitsPerNode
    if(degreeNormalization):
        # divide by degree of each target
        probabilities = probabilities / degrees[targets]
    # np array of shape (sources, vertexCount)

    if(returnType == "list"):
        # return a list of [(source,target,shortestTPProbabilities),...]
        return [(source,target,probabilities[(source,target)]/degrees[target]) for source in sources for target in targets]
    if(returnType == "dict"):
        # return a dict of {(source,target):shortestTPProbabilities,...}
        return {(source,target):probabilities[(source,target)]/degrees[target] for source in sources for target in targets}
    if(returnType == "matrix"):
        # return a matrix of shortestTPProbabilities
        return np.array([[probabilities[(source,target)]/degrees[target] for target in targets] for source in sources])


# import pickle as pkl
# import igraph as ig
# with open("/Users/filsilva/Downloads/netwx__Astronomy & Astrophysics_1980.pickle", "rb") as f:
#     network = pkl.load(f)



# g = ig.Graph.from_networkx(network)

# nodeSampleIndices = np.random.choice(g.vcount(),500,replace=False)
# estimatedTP(g,sources=nodeSampleIndices,targets=nodeSampleIndices,walks_per_source=1_000_000,batch_size=10_000, window_length=15)

