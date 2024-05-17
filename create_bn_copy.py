import pysmile
from pysmile_license import register

register()
# Create a new network
net = pysmile.Network()

# add risk node
risk_of_crash = net.add_node(pysmile.NodeType.CPT, "Risk_of_Crash")
# add CNS nodes
communication_failure = net.add_node(pysmile.NodeType.CPT, "Communication_Failure")
navigation_failure = net.add_node(pysmile.NodeType.CPT, "Navigation_Failure")
surveillance_failure = net.add_node(pysmile.NodeType.CPT, "Surveillance_Failure")
coop_surveillance_failure = net.add_node(pysmile.NodeType.CPT, "COOP_Surveillance_Failure")
noncoop_surveillance_failure = net.add_node(pysmile.NodeType.CPT, "NONCOOP_Surveillance_Failure")

# communication nodes
vhf_failure = net.add_node(pysmile.NodeType.CPT, "VHF_Data_Link_Failure")
g5_failure = net.add_node(pysmile.NodeType.CPT, "G5_Failure")

# navigation nodes
gnss_failure = net.add_node(pysmile.NodeType.CPT, "GNSS_Failure")
pnt_failure = net.add_node(pysmile.NodeType.CPT, "PNT_Failure")

# cooperative surveillance nodes
uat_failure = net.add_node(pysmile.NodeType.CPT, "UAT_Failure")
acas_failure = net.add_node(pysmile.NodeType.CPT, "ACAS_X_Failure")
# non cooperative surveillance nodes
radar_failure = net.add_node(pysmile.NodeType.CPT, "K_Band_RADAR_Failure")
lidar_failure = net.add_node(pysmile.NodeType.CPT, "LIDAR_Failure")
rf_detection_failure = net.add_node(pysmile.NodeType.CPT, "RF_Detection_Failure")

# Define node states
state_names = ["No", "Yes"]
for node in [risk_of_crash, communication_failure, navigation_failure, surveillance_failure, vhf_failure,
             g5_failure, gnss_failure, pnt_failure, uat_failure, acas_failure, radar_failure,
             lidar_failure, rf_detection_failure]:
    for i, state in enumerate(state_names):
        net.set_outcome_id(node, i, state)

# add arcs for CNS systems
net.add_arc(communication_failure, risk_of_crash)
net.add_arc(navigation_failure, risk_of_crash)
net.add_arc(surveillance_failure, risk_of_crash)
net.add_arc(coop_surveillance_failure, surveillance_failure)
net.add_arc(noncoop_surveillance_failure, surveillance_failure)

# add arcs for subsystem nodes
net.add_arc(vhf_failure, communication_failure)
net.add_arc(g5_failure, communication_failure)

net.add_arc(gnss_failure, navigation_failure)
net.add_arc(pnt_failure, navigation_failure)

net.add_arc(uat_failure, coop_surveillance_failure)
net.add_arc(acas_failure, coop_surveillance_failure)

net.add_arc(radar_failure, noncoop_surveillance_failure)
net.add_arc(lidar_failure, noncoop_surveillance_failure)
net.add_arc(rf_detection_failure, noncoop_surveillance_failure)

# Calculate the size of each CPT based on the number of parent nodes

# Risk_of_Crash given Communication_Failure, Navigation_Failure, and Surveillance_Failure (2^3 combinations * 2 outcomes)
risk_of_crash_cpt = [
    1 - 1e-12, 1e-12,  # No failures (000)
    1 - 1e-5, 1e-5,  # Surveillance failure only (001)
    1 - 1e-4, 1e-4,  # Navigation failure only (010)
    0.1, 0.9,  # Navigation and Surveillance failures (011)
    1 - 1e-6, 1e-6,  # Communication failure only (100)
    0.3, 0.7,  # Communication and Surveillance failures (101)
    0.2, 0.8,  # Communication and Navigation failures (110)
    0, 1,  # All failures (111)
]


# Communication_Failure given VHF, G5 Satellite/Cellular (2^3 combinations * 2 outcomes)
communication_failure_cpt = [
    1 - 1e-12, 1e-12,  # No sub-node failures
    1 - 1e-6, 1e-6,  # G5 failure only
    1 - 1e-6, 1e-6,  # VHF failure only
    0, 1,  # VHF and G5 failure
]

# Navigation_Failure given GNSS and PNT failures (2^2 combinations * 2 outcomes)
navigation_failure_cpt = [
    1 - 1e-12, 1e-12,  # No sub-node failures
    1 - 1e-6, 1e-6,  # PNT failure only
    1 - 1e-6, 1e-6,  # GNSS failure only
    0, 1,  # Both GNSS and PNT failure
]

# surveillance nodes
surveillance_failure_cpt = [
    1 - 1e-12, 1e-12,  # No failures
    1 - 1e-3, 1e-3,  # noncoop failure
    1 - 1e-2, 1e-2,  # coop failure
    0, 1,  # Both noncoop and coop failure
]

# cooperative surveillance nodes
coop_surveillance_failure_cpt = [
    1 - 1e-12, 1e-12,  # No failures
    1 - 1e-6, 1e-6,  # UAT failure only
    1 - 1e-6, 1e-6,  # ACAS_X failure only
    0, 1,  # Both UAT and ACAS_X failure
]

# non cooperative surveillance nodes
noncoop_surveillance_failure_cpt = [
    1 - 1e-12, 1e-12,  # No failures
    1 - 1e-6, 1e-6,  # K_Band_RADAR failure only
    1 - 1e-6, 1e-6,  # LIDAR failure only
    0.9, 0.1,  # K_Band_RADAR and LIDAR failure
    1 - 1e-6, 1e-6,  # RF_Detection failure only
    0.9, 0.1,  # K_Band_RADAR and RF_Detection failure
    0.9, 0.1,  # LIDAR and RF_Detection failure
    0, 1,  # All failures
]


# Set definitions for the leaf nodes (hypothetical values)
leaf_cpt = [1 - 1e-4, 1e-4]  # Example failure probability

# Set the CPTs for each node
net.set_node_definition(risk_of_crash, risk_of_crash_cpt)
net.set_node_definition(communication_failure, communication_failure_cpt)
net.set_node_definition(navigation_failure, navigation_failure_cpt)
net.set_node_definition(surveillance_failure, surveillance_failure_cpt)
net.set_node_definition(coop_surveillance_failure, coop_surveillance_failure_cpt)
net.set_node_definition(noncoop_surveillance_failure, noncoop_surveillance_failure_cpt)

net.set_node_definition(vhf_failure, leaf_cpt)
net.set_node_definition(g5_failure, leaf_cpt)

net.set_node_definition(gnss_failure, leaf_cpt)
net.set_node_definition(pnt_failure, leaf_cpt)
net.set_node_definition(uat_failure, leaf_cpt)
net.set_node_definition(acas_failure, leaf_cpt)
net.set_node_definition(radar_failure, leaf_cpt)
net.set_node_definition(lidar_failure, leaf_cpt)
net.set_node_definition(rf_detection_failure, leaf_cpt)

# Save the network to a file
net.write_file("cns_bn.xdsl")
