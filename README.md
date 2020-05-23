# K-Chromatic
Implementation of Dirac's method with Minimum Degree Vertex.
The process of generating K-Chromatic chordal graphs is as follows:
• Step 1: Generate an arbitrary graph G = (V,E) with |V| = n and |E| = m.
• Step 2: Finding mutually independent vertices M from the graph G, make
them chordal say H by making such vertices simplicial and then remove
from the input graph.
• Step 3: Apply Minimum Degree Vertex heuristic to the non-mutual set of
vertices and make graph chordal, say C.
• Step 4: Combine graphs in Step 2 and 3 i.e., H ∪C and check for chordality and name this graph as I
• Step 5: Perform minimum vertex coloring algorithm (Welsch Powell algorithm) on the graph I.
(Additional Feature)
