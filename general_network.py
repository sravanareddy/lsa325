from __future__ import division

"""Run some exploratory analysis on Twitter replies network.
Some of the code is adapted from the snap.py tutorial."""

import snap
from twython import Twython
import sys

if __name__=='__main__':
    CONSUMER_KEY, CONSUMER_SECRET = open('twitapikeys.txt').read().split()[:2]
    twitterapi = Twython(CONSUMER_KEY, CONSUMER_SECRET)
    
    filename = sys.argv[1]
    repliesgraph = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1)
    snap.PrintInfo(repliesgraph, "Twitter replies network")
    print
    
    #reciprocity
    num_dir_edges = snap.CntUniqDirEdges(repliesgraph)
    print "{0:.2f}% of directed edges are reciprocal".format(snap.CntUniqBiDirEdges(repliesgraph)*2*100/num_dir_edges)
    
    #clustering coefficient
    print "The clustering coefficient is {0:.2f}%".format(snap.GetClustCf(repliesgraph)*100)
        
    #strongly and weakly connected components
    CntV = snap.TIntPrV()
    snap.GetSccSzCnt(repliesgraph, CntV)
    num_cc = 0
    for p in CntV:
        print "{0} strongly connected component(s) of size {1}".format(p.GetVal2(), p.GetVal1())
        num_cc += p.GetVal2()
    print num_cc, "total strongly connected components"
    print
    
    snap.GetWccSzCnt(repliesgraph, CntV)
    num_cc = 0
    for p in CntV:
        print "{0} weakly connected component(s) of size {1}".format(p.GetVal2(), p.GetVal1())
        num_cc += p.GetVal2()
    print num_cc, "total weakly connected components"
    print
    
    #properties of largest strongly connected component
    big_scc = snap.GetMxScc(repliesgraph)
    snap.PrintInfo(big_scc, "Largest strongly connected component")

    num_dir_edges = snap.CntUniqDirEdges(big_scc)
    print "{0:.2f}% of directed edges are reciprocal".format(snap.CntUniqBiDirEdges(big_scc)*2*100/num_dir_edges)
    
    print "The clustering coefficient is {0:.2f}%".format(snap.GetClustCf(big_scc)*100)
    
    print "The diameter is approximately {0}".format(snap.GetBfsFullDiam(big_scc, 1000))

    #store CC for graphviz
    snap.SaveGViz(big_scc, filename+".dot", "Largest Connected Component")
    print "Saved GraphViz"
    
    #page rank over entire graph to detect "celebrities"
    PRankH = snap.TIntFltH()
    snap.GetPageRank(repliesgraph, PRankH)
    page_rank = {}
    for userid in PRankH:
        if PRankH[userid]>0:
            page_rank[userid] = PRankH[userid]
    page_rank = sorted(page_rank.items(), key=lambda x:x[1], reverse=True)
    print "Nodes with the highest page rank:"
    celebs = map(lambda x:str(x[0]), page_rank[:100])
    infos = twitterapi.lookup_user(user_id=','.join(celebs))
    for info in infos:
        print info['name'], info['verified']
    print 

    
    
