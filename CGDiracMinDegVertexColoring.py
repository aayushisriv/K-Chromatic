"""
@author-Aayushi Srivastava
This code uses Dirac's Method to generate chordal graphs with few edges. Uses mutually independent vertices
and MDV to make the graph chordal. Then uses Welsch Powell Algorithm for on the chordal graph for minimum
vertex coloring.
"""


import sys
import random

import itertools
import copy

import networkx as nx
import matplotlib.pyplot as plt

class DirMd:
	def __init__(self, noNodes, noEdges, m_vert=0):
		"""function to initialize the variables in the instance of a ChordalGraph"""
		self.noNodes = noNodes
		self.noEdges = noEdges
		self.vertexList = []
		self.GEdgeList = []
		self.HEdgeList = [] #HEdgeList
		self.G = {}
		self.H = {}
		self.neb = [] 
		self.m_vert = m_vert
		self.minv = {}
		self.neb = []
		self.mivlist = []
		self.mneb = []
		self.NEdgeList = []
		self.diffvert = []
		self.MIEdgeList = []


	def ArbitraryGraph(self):
		"""function to create arbitrary graph"""
		self.G = nx.dense_gnm_random_graph(self.noNodes, self.noEdges)
		
		if type(self.G) is not dict:
			self.G = nx.to_dict_of_lists(self.G)
				
		for i in range(0, self.noNodes):
			self.vertexList.append(i)
		for key, value in self.G.iteritems():
			for v in value:
				if key<v:
					e = []
					e.append(key)
					e.append(v)
					self.GEdgeList.append(e)
		
		self.G = nx.Graph(self.G)
		connComp = sorted(nx.connected_components(self.G))
		self.G = nx.to_dict_of_lists(self.G)
		
		connComp = list(connComp)
		noOFConnComp = len(connComp)
		if noOFConnComp > 1:
			print "Here we are"
			print connComp
			self.G = nx.Graph(self.G)
			self.G = nx.to_dict_of_lists(self.G)
			self.plotArbitraryGraph(self.G)
			j = 0
			while j < noOFConnComp - 1:
				u = random.choice(list(connComp[j%noOFConnComp]))
				v = random.choice(list(connComp[(j+1)%noOFConnComp]))
				self.addAnEdge(self.G, self.GEdgeList, u, v)
				j = j + 1
		print str(self.G)
		self.G = nx.Graph(self.G)
		self.G = nx.to_dict_of_lists(self.G)
		self.plotArbitraryGraph(self.G)
#		self.G = nx.to_dict_of_lists(self.G)

		 
	def addAnEdge(self, graphToAdd, edgeListToAdd, v1, v2):
		"""function to add an edge in the graph"""
		graphToAdd = nx.to_dict_of_lists(graphToAdd)
		graphToAdd[v1].append(v2)
		graphToAdd[v2].append(v1)
		e = []
		e.append(v1)
		e.append(v2)
		edgeListToAdd.append(e)
		

	def plotArbitraryGraph(self, graphToDraw):
		#self.G = nx.Graph(self.G)
		#graphToDraw = nx.Graph(graphToDraw)
		edges = 0
		for node, degree in graphToDraw.iteritems():
			edges += len(degree) 
		
		GD = nx.Graph(graphToDraw)
		pos = nx.spring_layout(GD)
		print "\nArbitrary Graph: "+str(self.G)
		print "\nNo. of edges in the Arbitrary Graph: "+ str(edges/2)
		#plt.title("Arbitrary Graph")
		#nx.draw(GD, pos, width=8.0,alpha=0.5,with_labels = True)
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_nodes(GD, pos, node_color='red', node_size=300, alpha=0.8)
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		#plt.show(block=False)
		plt.show()
		self.mutualInd(self.G)

	def mutualInd(self,randomGraph):
		"""Making mutually independent vertices chordal"""
		#randomGraph = nx.to_dict_of_lists(randomGraph)
		miVertices = nx.maximal_independent_set(nx.Graph(randomGraph))
		print "Mutually Independent Vertices are", miVertices
		randomGraph = nx.Graph(randomGraph)
		for m in miVertices:
			self.mneb = list(randomGraph.neighbors(m))
			print "Neighbors of the vertex", m,"are:",self.mneb
			mncom = list(itertools.combinations(self.mneb,2))
			for p in mncom:
				v1 =  p[0]
				v2 = p[1]
				if randomGraph.has_edge(*p) :
					print "Already edge is there",p
					continue
				else:
					randomGraph.add_edge(*p)
				#self.NEdgeList.append(p)
					print "Edge added between",p
					self.MIEdgeList.append(p)
					continue
		#randomGraph.remove_nodes_from(list(list(set(self.vertexList) - set(list(miVertices)))))
		randomGraph.remove_nodes_from(list(set(list(miVertices))))
		self.diffvert = list(set(self.vertexList).difference(set(miVertices)))

		print "Checkers", self.MIEdgeList
		print "BlacknWhite", self.diffvert
		self.createChrdG(randomGraph,self.MIEdgeList)

	
	def createChrdG(self, grT,edl):
		"""start MDV""" 
		self.HEdgeList = copy.deepcopy(self.GEdgeList)
		#self.H = copy.deepcopy(self.G)
		#self.H = nx.Graph(self.H)

		print "Start Minimum Vertex Process"
		#self.H = nx.Graph(self.H)
		#diff = list(set(self.HEdgeList) - set(edl))
		#print "Getting it", diff
		self.Minvertex(self.diffvert,self.HEdgeList, grT)
		self.FinalGraph(self.NEdgeList,self.MIEdgeList,self.vertexList)
		print "End Minimum Vertex Process"
		return True


	def Minvertex(self,MvertexList,edgeList, graphtoCons):
		graphtoCons = nx.Graph(graphtoCons)
		#self.H = nx.Graph(self.H)
		#random.shuffle(MvertexList)
		#self.H = nx.Graph(self.H)
		for v in MvertexList:
			print "Starting",v
			#self.H = nx.Graph(self.H)
			dv = list(graphtoCons.degree(graphtoCons)) #list of tuples
			dvdict = dict(dv)
			print dv
			print dvdict
			self.minv = dict(sorted(dvdict.items(), key=lambda kv:(kv[1], kv[0])))
			print self.minv
			#self.H = nx.Graph(self.H)
			mincp = copy.deepcopy(self.minv)
			try:
				for key,value in mincp.iteritems():
					if value < 2:
						self.minv.pop(key)
				graphtoCons = nx.Graph(graphtoCons)
				#nodeH = self.H.nodes()
				nodeH = graphtoCons.nodes()
				graphtoCons.add_nodes_from(list(self.minv))
				graphtoCons.remove_nodes_from(list(list(set(nodeH) - set(list(self.minv)))))
				graphtoCons = nx.to_dict_of_lists(graphtoCons)
				self.m_vert = min(self.minv.keys(), key=(lambda k:self.minv[k]))
				print "Minimum degree vertex is:",self.m_vert
				graphtoCons = nx.Graph(graphtoCons)
				print "The chosen Minimum vertex is", self.m_vert
				
				self.neb = list(graphtoCons.neighbors(self.m_vert))
				print "Neighbors of the chosen vertex are:",self.neb
				neblen = len(self.neb)
				graphtoCons = nx.Graph(graphtoCons)
				graphtoCons.remove_node(self.m_vert)
				self.neighbcomp(self.m_vert,graphtoCons)
				print "Diction1", graphtoCons
				graphtoCons = nx.Graph(graphtoCons)
			except ValueError as e:
				print "Dictionary is Empty now"
				print "Diction", graphtoCons
				break


	def neighbcomp(self,chosvert,graphtoRecreate):
		#self.H = nx.Graph(self.H)
		graphtoRecreate = nx.Graph(graphtoRecreate)
		nebcomb = list(itertools.combinations(self.neb,2))
		for p in nebcomb:
			v1 =  p[0]
			v2 = p[1]
			if graphtoRecreate.has_edge(*p) :
				print "Already Edge"
				continue
			else:
				graphtoRecreate.add_edge(*p)
				self.NEdgeList.append(p)
				print "Edge added between",p
				continue
		#graphtoRecreate= nx.to_dict_of_lists(graphtoRecreate)


	def FinalGraph(self,newaddedgelist,anotheredgeList,vertexlist):
		print "EdgeList verifying",newaddedgelist
		print "Total Edges added in Minimum Degree Process is ",len(newaddedgelist)
		print "Total Edges added in  Mutually Independent Vertices is ",len(anotheredgeList)
		print "Total Edges added in graph",(len(newaddedgelist)+ len(anotheredgeList))
		GD = nx.Graph(self.G)
		pos = nx.spring_layout(GD)

		B = copy.deepcopy(self.G)
		B = nx.Graph(B)
		B.add_nodes_from(vertexlist)
		B.add_edges_from(newaddedgelist)
		B.add_edges_from(anotheredgeList)
		##Recognition----
		graph = nx.Graph(B)
		if nx.is_chordal(graph):
			print "IT IS CHORDAL"
		else :
			print "NO IT IS NOT CHORDAL"
		nx.draw_networkx_nodes(GD, pos, nodelist=vertexlist, node_color='red', node_size=300, alpha=0.8,label='Min degree')
			
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_edges(GD, pos, edgelist=newaddedgelist, width=8.0, alpha=0.5, edge_color='blue',label='Min degree')
		nx.draw_networkx_edges(GD, pos, edgelist=anotheredgeList, width=6.0, alpha=0.5, edge_color='green',label='Min degree')
		nx.draw_networkx_labels(GD,pos)
		plt.draw()
		#plt.show(block=False)
		plt.show()
		self.welsch_powell(B)

	def welsch_powell(self,graphVC):
		"""Minimum Vertex Coloring"""
		print "Check if welsh"
		#sorting the nodes based on its valency
		node_list = sorted(graphVC.nodes(), key =lambda x:graphVC.neighbors(x))
		print "Welsch nodeList",node_list
		col_val = {} #dictionary to store the colors assigned to each node
		col_val[node_list[0]] = 0 #assign the first color to the first node
		#print "Pallate", col_val
		# Assign colors to remaining N-1 nodes
		for node in node_list[1:]:
			available = [True] * len(graphVC.nodes()) #boolean list[i] contains false if the node color 'i' is not available
			#print available

			#iterates through all the adjacent nodes and marks it's color as unavailable, if it's color has been set already
			for adj_node in graphVC.neighbors(node): 
				#print "Valer",col_val
				if adj_node in col_val.keys():
					col = col_val[adj_node]
					available[col] = False
			clr = 0
			for clr in range(len(available)):
				if available[clr] == True:
					break
			col_val[node] = clr
		print "Final",col_val
		print type(col_val)
		abc = []
		for key,value in col_val.iteritems():
			abc.append(value)
		print "The Chromatic number is",len(set(abc))
		#return col_val
		#col_val = welsch_powell(graphVC)
		#print "My raph"
		self.DrawGraph(graphVC,col_val)
		#print "Total colors added"
		#print "See welu"

	def DrawGraph(self,graphy,col_val):
		print "Check if I can draw"
		##Recognition----
		graph = nx.Graph(graphy)
		if nx.is_chordal(graph):
			print "IT IS CHORDAL"
		else :
			print "NO IT IS NOT CHORDAL"
		GD = nx.Graph(graphy)
		pos = nx.spring_layout(GD)
		#graphy = nx.Graph(graphy)
		#pos = nx.spring_layout(graphy)
		values = [col_val.get(node, 'blue') for node in graphy.nodes()]
		#nx.draw(graphy, pos, with_labels = True, node_color = values, edge_color = 'black' ,width = 1, alpha = 0.7)  #with_labels=true is to show the node number in the output graph
		nx.draw_networkx_edges(GD, pos, width=1.0, alpha=0.5)
		nx.draw_networkx_nodes(GD, pos, with_labels=True,node_color=values, node_size=300, alpha=0.8)
		nx.draw_networkx_labels(GD,pos)
		plt.show()
		



val1 = int(raw_input("Enter no. of nodes:"))
val2 = int(raw_input("Enter no. of edges:"))
gd = DirMd(val1,val2)
gd.ArbitraryGraph()
#gd.createChrdG()
