import numpy as np
import cxrandomwalk as rw
from tqdm.auto import tqdm 



def getRandomWalks():
  vertexCount = 10000
  edges = np.random.randint(0,vertexCount-1,(vertexCount*2, 2))
  weights = np.random.random(size=vertexCount*2)

  agent = rw.Agent(vertexCount,edges,False,weights)

  return agent.generateWalks(q=1.0,p=1.0,verbose=False,updateInterval=1000)


vertexCount = 10000
edges = np.random.randint(0,vertexCount-1,(vertexCount*2, 2))
weights = np.random.random(size=vertexCount*2)

agent = rw.Agent(vertexCount,edges,False,weights)

def make_pbar():
  pbar = None
  def inner(current,total):
    nonlocal pbar
    if(pbar is None):
      pbar= tqdm(total=total)
    pbar.update(current - pbar.n)
  return inner

print(len(agent.generateWalks(q=1.0,p=1.0,verbose=False,updateInterval=1000,callback=make_pbar())))
