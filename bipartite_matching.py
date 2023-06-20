# ref: https://www.kaggle.com/code/azxc9595/visual-graphs-of-philosophy
List2=[]
All=pd.DataFrame()
for c in DF["author"].unique():
    We_Edges=[]
    for a in DF[DF["author"]==c]["citation"]:
        if a!=[] and a!=['']:#Eliminating rubbish elements
            for b in a:
                We_Edges.append([b,1])#Adding all referred philosophers to second set
    Connections=pd.DataFrame([a[1] for  a in We_Edges],index=[a[0] for  a in We_Edges]).groupby(level=0).sum()#Adding the number of times that have been referred and the referred philosopher
    All=pd.concat((All,pd.DataFrame([c,Connections]).T))#Iteratively concatenating data frames 
    import networkx as nx
    G=nx.Graph()
    if c in Connections.index: 
        X=[]
        C=Connections.index.to_list() 
        for a in C:
            if a!=c:#We eliminate the occasion of referring to his oneself
                X.append(a)#We gather all the citations into 1 list 
        G.add_nodes_from([c],bipartite=0)#For each philosopher from DF we add them into the first set for their own graph
        G.add_nodes_from([a for a in X],bipartite=1)#And the citations to the second set
        for index,value in zip(X,Connections.values):
            G.add_edge(c,str(index),weight=int(value))
        List2.append(G)#Gathering all graphs in a list
         
    else: 
        G=nx.Graph()
        G.add_nodes_from([c],bipartite=0)
        G.add_nodes_from([a for a in Connections.index],bipartite=1)
        for index,value in zip(Connections.index,Connections.values):
            G.add_edge(c,str(index),weight=int(value))
        List2.append(G)
        
All=All.rename(columns={0:"Name",1:"Citations"})
