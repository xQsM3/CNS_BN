import pysmile
from pysmile_license import register
register()

# Load the network from the file
net = pysmile.Network()
net.read_file("cns_bn.xdsl")

# Set evidence (if applicable)
# Example: Set evidence that VHF_Data_Link_Failure has occurred
#net.set_evidence("Navigation_Failure", "Yes")
net.set_evidence("Weather_Conditions", "Good")
net.set_evidence("Airspace_Congestion", "High")
net.set_evidence("Ground_Population_Density", "High")

# Update the beliefs in the network
net.update_beliefs()

# Get the probability distribution for the Risk_of_Crash node
risk_of_crash = net.get_node_value("Risk_of_Crash")

# Print the probability of each state
print(f"Probability of No Crash: {risk_of_crash[0]:.2e}")
print(f"Probability of Crash: {risk_of_crash[1]:.2e}")
