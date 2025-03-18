import yaml
from jinja2 import Environment, FileSystemLoader

# Load the network definition
with open("network.yaml", "r") as file:
    network = yaml.safe_load(file)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader("."), trim_blocks=True, lstrip_blocks=True)
template = env.get_template("router_template.j2")

# Generate configurations for each router
for router_name, router_data in network["routers"].items():
    # Add networks to BGP configuration
    router_data["bgp"]["networks"] = [
        details["ip"] for details in router_data["interfaces"].values()
    ]

    # Render the template
    config = template.render(router_name=router_name, **router_data)

    # Write the configuration to a file
    with open(f"configs/{router_name}_startup-config.cfg", "w") as f:
        f.write(config)

print("Configurations generated successfully!")
