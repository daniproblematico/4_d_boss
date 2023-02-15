import json

with open("project.geom", "r") as f:
    building_data = json.load(f)
    print(type(building_data))

levels = {}
acumulator_heigths = 0


def create_node(id, global_info_nodes, story_heigth_acum):
    """Node information constructor

    Args:
        id (string): _description_
        global_info_nodes (dict): _description_
        story_heigth_acum (float): _description_

    Returns:
        info_node: Dictionary with node information
    """

    info_node = dict(
        id=id,
        x_coord=global_info_nodes[id][0],
        y_coord=global_info_nodes[id][1],
        z_coord=story_heigth_acum
        if len(global_info_nodes[id]) == 2
        else global_info_nodes[id][2],
    )

    return info_node

cont = 0

for story in reversed(building_data["pisos"]):

    levels[story] = dict(
        id=story,
        key_nodes=[],
        key_cols=list(building_data["col_piso"][story].keys()),
        key_beams=list(building_data["vig_piso"][story]),
        story_heigth=building_data["pisos"][story],
        story_heigth_acum=acumulator_heigths + building_data["pisos"][story],
        info_cols={},
        info_beams={},
        nodes={},
    )

    acumulator_heigths += building_data["pisos"][story]

    # For each element type, element information will be storaged
    for type_element in ["cols", "beams"]:
        # Key name from the building_data dict
        list_to_iterate = levels[story][f"key_{type_element}"]
        # Original name of the key in the building_data dict
        original_key_name = "columnas" if type_element == "cols" else "vigas"

        # For each element in the list, the information will be storaged
        for element in list_to_iterate:

            info_element = dict(
                id=element,
                connectivity=building_data[original_key_name][element],
                node_i=building_data[original_key_name][element][0],
                node_j=building_data[original_key_name][element][1],
            )


            # By element type, the information will be storaged
            if type_element == "cols":
                levels[story]["info_cols"][element] = info_element
            elif type_element == "beams":
                levels[story]["info_beams"][element] = info_element
            
            for j, node in enumerate([info_element["node_i"], info_element["node_j"]]):
                
                # Check if node is already storaged
                if node in levels[story]["nodes"]:
                    continue
                # Check if it is a column node, only will be storaged final node
                if type_element == "cols" and not j:
                    continue

                levels[story]["nodes"][node] = create_node(
                    node, building_data["nodos"], levels[story]["story_heigth_acum"]
                )

                levels[story]["key_nodes"].append(node)

        




print(levels)