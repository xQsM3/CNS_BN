import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes
nodes = [
    "Risk_of_Crash", "Communication_Failure", "Navigation_Failure", "Surveillance_Failure",
    "VHF_Data_Link_Failure", "Satellite_Failure", "Cellular_Failure",
    "GNSS_Failure", "PNT_Failure",
    "UAT_Failure", "ACAS_X_Failure", "K_Band_RADAR_Failure", "LIDAR_Failure", "RF_Detection_Failure"
]
G.add_nodes_from(nodes)

# Add edges (arcs)
edges = [
    ("Communication_Failure", "Risk_of_Crash"),
    ("Navigation_Failure", "Risk_of_Crash"),
    ("Surveillance_Failure", "Risk_of_Crash"),
    ("VHF_Data_Link_Failure", "Communication_Failure"),
    ("Satellite_Failure", "Communication_Failure"),
    ("Cellular_Failure", "Communication_Failure"),
    ("GNSS_Failure", "Navigation_Failure"),
    ("PNT_Failure", "Navigation_Failure"),
    ("UAT_Failure", "Surveillance_Failure"),
    ("ACAS_X_Failure", "Surveillance_Failure"),
    ("K_Band_RADAR_Failure", "Surveillance_Failure"),
    ("LIDAR_Failure", "Surveillance_Failure"),
    ("RF_Detection_Failure", "Surveillance_Failure")
]
G.add_edges_from(edges)

# Draw the graph
pos = nx.spring_layout(G)  # You can choose different layouts
nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', arrowsize=20)
plt.title("Bayesian Network Structure")
plt.show()
