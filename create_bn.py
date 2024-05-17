import pysmile
from pysmile_license import register

register()

# Create a new network
net = pysmile.Network()

# Add risk node
risk_of_crash = net.add_node(pysmile.NodeType.CPT, "Risk_of_Crash")

# Add CNS nodes
communication_failure = net.add_node(pysmile.NodeType.CPT, "Communication_Failure")
navigation_failure = net.add_node(pysmile.NodeType.CPT, "Navigation_Failure")
surveillance_failure = net.add_node(pysmile.NodeType.CPT, "Surveillance_Failure")
coop_surveillance_failure = net.add_node(pysmile.NodeType.CPT, "COOP_Surveillance_Failure")
noncoop_surveillance_failure = net.add_node(pysmile.NodeType.CPT, "NONCOOP_Surveillance_Failure")
flight_control_system_failure = net.add_node(pysmile.NodeType.CPT, "Flight_Control_System_Failure")

# Communication nodes
vhf_failure = net.add_node(pysmile.NodeType.CPT, "VHF_Data_Link_Failure")
g5_failure = net.add_node(pysmile.NodeType.CPT, "G5_Failure")

# Navigation nodes
gnss_failure = net.add_node(pysmile.NodeType.CPT, "GNSS_Failure")
pnt_failure = net.add_node(pysmile.NodeType.CPT, "PNT_Failure")

# Cooperative surveillance nodes
uat_failure = net.add_node(pysmile.NodeType.CPT, "UAT_Failure")
acas_failure = net.add_node(pysmile.NodeType.CPT, "ACAS_X_Failure")

# Non-cooperative surveillance nodes
radar_failure = net.add_node(pysmile.NodeType.CPT, "K_Band_RADAR_Failure")
lidar_failure = net.add_node(pysmile.NodeType.CPT, "LIDAR_Failure")
rf_detection_failure = net.add_node(pysmile.NodeType.CPT, "RF_Detection_Failure")

# Environment nodes
weather_conditions = net.add_node(pysmile.NodeType.CPT, "Weather_Conditions")
airspace_congestion = net.add_node(pysmile.NodeType.CPT, "Airspace_Congestion")
ground_population_density = net.add_node(pysmile.NodeType.CPT, "Ground_Population_Density")

# Define node states
state_names = ["No", "Yes"]
for node in [risk_of_crash, communication_failure, navigation_failure, surveillance_failure,
             coop_surveillance_failure, noncoop_surveillance_failure, flight_control_system_failure,
             vhf_failure, g5_failure, gnss_failure, pnt_failure, uat_failure, acas_failure, radar_failure,
             lidar_failure, rf_detection_failure]:
    for i, state in enumerate(state_names):
        net.set_outcome_id(node, i, state)

# Define states for environment nodes
weather_state_names = ["Bad", "Good"]
for i, state in enumerate(weather_state_names):
    net.set_outcome_id(weather_conditions, i, state)

factor_state_names = ["Low", "High"]
for node in [airspace_congestion, ground_population_density]:
    for i, state in enumerate(factor_state_names):
        net.set_outcome_id(node, i, state)

# Add arcs for CNS systems
net.add_arc(communication_failure, risk_of_crash)
net.add_arc(navigation_failure, risk_of_crash)
net.add_arc(surveillance_failure, risk_of_crash)
net.add_arc(flight_control_system_failure, risk_of_crash)

net.add_arc(coop_surveillance_failure, surveillance_failure)
net.add_arc(noncoop_surveillance_failure, surveillance_failure)

# Add arcs for subsystem nodes
net.add_arc(vhf_failure, communication_failure)
net.add_arc(g5_failure, communication_failure)
net.add_arc(gnss_failure, navigation_failure)
net.add_arc(pnt_failure, navigation_failure)
net.add_arc(uat_failure, coop_surveillance_failure)
net.add_arc(acas_failure, coop_surveillance_failure)
net.add_arc(radar_failure, noncoop_surveillance_failure)
net.add_arc(lidar_failure, noncoop_surveillance_failure)
net.add_arc(rf_detection_failure, noncoop_surveillance_failure)

# Add arcs from environment nodes to the relevant subsystem nodes
net.add_arc(weather_conditions, radar_failure)
net.add_arc(weather_conditions, lidar_failure)
net.add_arc(weather_conditions, flight_control_system_failure)
net.add_arc(airspace_congestion, flight_control_system_failure)
net.add_arc(ground_population_density, flight_control_system_failure)


# Define CPTs for the nodes

# Risk_of_Crash given Communication_Failure, Navigation_Failure, Surveillance_Failure, and Flight_Control_System_Failure
risk_of_crash_cpt = [
    1 - 1e-12, 1e-12,  # No failures (0000)
    1 - 1e-3, 1e-3,  # Flight control system failure only (0001)
    1 - 1e-5, 1e-5,  # Surveillance failure only (0010)
    0.2, 0.8,  # Surveillance and Flight control system failures (0011)
    1 - 1e-4, 1e-4,  # Navigation failure only (0100)
    0.4, 0.6,  # Navigation and Flight control system failures (0101)
    0.3, 0.7,  # Surveillance and Navigation failures (0110)
    0.1, 0.9,  # Surveillance, Navigation, and Flight control system failures (0111)
    1 - 1e-6, 1e-6,  # Communication failure only (1000)
    0.3, 0.7,  # Communication and Flight control system failures (1001)
    0.4, 0.6,  # Communication and Surveillance failures (1010)
    0.1, 0.9,  # Communication, Surveillance, and Flight control system failures (1011)
    0.4, 0.6,  # Communication and Navigation failures (1100)
    0.1, 0.9,  # Communication, Navigation, and Flight control system failures (1101)
    0.1, 0.9,  # Communication, Surveillance, and Navigation failures (1110)
    0, 1,  # All failures (1111)
]

# Communication_Failure given VHF and G5 failures (2^2 combinations * 2 outcomes)
communication_failure_cpt = [
    1 - 1e-12, 1e-12,  # No sub-node failures (00)
    1 - 1e-6, 1e-6,  # G5 failure only (01)
    1 - 1e-6, 1e-6,  # VHF failure only (10)
    0, 1,  # VHF and G5 failure (11)
]

# Navigation_Failure given GNSS and PNT failures (2^2 combinations * 2 outcomes)
navigation_failure_cpt = [
    1 - 1e-12, 1e-12,  # No sub-node failures (00)
    1 - 1e-6, 1e-6,  # PNT failure only (01)
    1 - 1e-6, 1e-6,  # GNSS failure only (10)
    0, 1,  # Both GNSS and PNT failure (11)
]

# Surveillance_Failure given COOP and NONCOOP Surveillance Failures (2^2 combinations * 2 outcomes)
surveillance_failure_cpt = [
    1 - 1e-12, 1e-12,  # No failures (00)
    1 - 1e-3, 1e-3,  # noncoop failure (01)
    1 - 1e-2, 1e-2,  # coop failure (10)
    0, 1,  # Both noncoop and coop failure (11)
]

# COOP_Surveillance_Failure given UAT and ACAS_X failures (2^2 combinations * 2 outcomes)
coop_surveillance_failure_cpt = [
    1 - 1e-12, 1e-12,  # No failures (00)
    1 - 1e-6, 1e-6,  # UAT failure only (01)
    1 - 1e-6, 1e-6,  # ACAS_X failure only (10)
     0, 1,  # Both UAT and ACAS_X failure (11)
]

# NONCOOP_Surveillance_Failure given K_Band_RADAR, LIDAR, and RF detection failures (2^3 combinations * 2 outcomes)
noncoop_surveillance_failure_cpt = [
    1 - 1e-12, 1e-12,  # No failures (000)
    1 - 1e-6, 1e-6,  # RF_Detection failure only (001)
    1 - 1e-6, 1e-6,  # LIDAR failure only (010)
    0.9, 0.1,  # LIDAR and RF_Detection failures (011)
    1 - 1e-6, 1e-6,  # K_Band_RADAR failure only (100)
    0.9, 0.1,  # K_Band_RADAR and RF_Detection failures (101)
    0.9, 0.1,  # K_Band_RADAR and LIDAR failures (110)
    0, 1,  # All failures (111)
]

# Flight_Control_System_Failure given Weather_Conditions, Airspace_Congestion, and Ground_Population_Density (2^3 combinations * 2 outcomes)
flight_control_system_failure_cpt = [
    1 - 1e-10, 1e-10,  # Bad weather, Low congestion, Low population density (000)
    1 - 1e-8, 1e-8,  # Bad weather, Low congestion, High population density (001)
    1 - 1e-6, 1e-6,  # Bad weather, High congestion, Low population density (010)
    1 - 1e-4, 1e-4,    # Bad weather, High congestion, High population density (011)

    1 - 1e-12, 1e-12,    # Good weather, Low congestion, Low population density (100)
    1 - 1e-10, 1e-10,    # Good weather, Low congestion, High population density (101)
    1 - 1e-8, 1e-8,    # Good weather, High congestion, Low population density (110)
    1 - 1e-6, 1e-6,    # Good weather, High congestion, High population density (111)
]

# Adjust leaf node definitions to account for parent nodes
leaf_cpt_no_parents = [1 - 1e-4, 1e-4]  # Example failure probability for nodes without parents

leaf_cpt_with_weather = [
    1 - 1e-2, 1e-2,  # Bad weather
    1 - 1e-4, 1e-4,  # Good weather
]

# Set the CPTs for each node
net.set_node_definition(risk_of_crash, risk_of_crash_cpt)
net.set_node_definition(communication_failure, communication_failure_cpt)
net.set_node_definition(navigation_failure, navigation_failure_cpt)
net.set_node_definition(surveillance_failure, surveillance_failure_cpt)
net.set_node_definition(coop_surveillance_failure, coop_surveillance_failure_cpt)
net.set_node_definition(noncoop_surveillance_failure, noncoop_surveillance_failure_cpt)
net.set_node_definition(flight_control_system_failure, flight_control_system_failure_cpt)

net.set_node_definition(vhf_failure, leaf_cpt_no_parents)
net.set_node_definition(g5_failure, leaf_cpt_no_parents)
net.set_node_definition(gnss_failure, leaf_cpt_no_parents)
net.set_node_definition(pnt_failure, leaf_cpt_no_parents)
net.set_node_definition(uat_failure, leaf_cpt_no_parents)
net.set_node_definition(acas_failure, leaf_cpt_no_parents)

net.set_node_definition(radar_failure, leaf_cpt_with_weather)
net.set_node_definition(lidar_failure, leaf_cpt_with_weather)
net.set_node_definition(rf_detection_failure, leaf_cpt_no_parents)

# Save the network to a file
net.write_file("cns_bn.xdsl")
