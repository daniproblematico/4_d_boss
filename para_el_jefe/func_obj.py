import json
import numpy as np

with open("project.geom", "r") as f:
    building_data = json.load(f)
    print(type(building_data))

levels = {}
acumulator_heigths = 0


def create_node(id, global_info_nodes, story_heigth_acum):
    """Node information constructor

    Args:
        id (string): Node id
        global_info_nodes (dict): Coordinates information of all nodes
        story_heigth_acum (float): Height of the current level

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


def geometric_info(
    beam_nodei_coordinates,
    beam_nodej_coordinates,
    column_node_coordinates,
):
    """calculates the lenght of the beam and the angle between the beam and the referency vector

    Args:
        beam_nodei_coordinates (list): coordinates of the node i of the beam in the order [x,y]
        beam_nodej_coordinates (list): coordinates of the node j of the beam in the order [x,y]
        column_node_coordinates (list): coordinates of the node of the column in the order [x,y]
        referency_vector (list): vector that will be used as referency to calculate the angle in the order [x,y]

    Returns:
        beam_lenght: lenght of the beam
        angle: angle between the beam and the referency vector in radians clockwise
    """

    #calculates the lenght of the beam
    beam_lenght = np.sqrt(
        (beam_nodej_coordinates[1] - beam_nodei_coordinates[1]) ** 2
        + (beam_nodej_coordinates[0] - beam_nodei_coordinates[0]) ** 2
    )
    
    #calculates the angle between the beam and the referency vector
    x_coord_diference = (
        beam_nodej_coordinates[0]
        + beam_nodei_coordinates[0]
        - 2 * column_node_coordinates[0]
    )
    y_coord_diference = (
        beam_nodej_coordinates[1]
        + beam_nodei_coordinates[1]
        - 2 * column_node_coordinates[1]
    )
    

    referency_vector = [1, 0]
    normal_vector = np.array([x_coord_diference, y_coord_diference])
    referency_vector = np.array(referency_vector)
    angle = np.arccos(
        np.dot(normal_vector, referency_vector)
        / (np.linalg.norm(normal_vector) * np.linalg.norm(referency_vector))
    )

    if y_coord_diference<0:
        angle = 2*np.pi - angle

    return beam_lenght, angle


cont = 0

# For each level, the information will be storaged
for story in reversed(building_data["pisos"]):
    #define keys for the levels dict
    levels[story] = dict(
        id=story,
        key_nodes=[],
        key_cols=list(building_data["col_piso"][story].keys()),
        key_beams=list(building_data["vig_piso"][story].keys()),
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


columnas = {}

#for each level
for n in levels:
    #for each column in the level
    for i in levels[n]["key_cols"]:
        connected_beam = {}
        columnas[i + n] = dict(connected_beams=connected_beam)

        for j in levels[n]["key_beams"]:
            #check if the beam is connected to the column
            if (
                levels[n]["info_cols"][i]["node_j"]
                in levels[n]["info_beams"][j]["connectivity"]
            ):
                #extract the geometric information of the beam connected to the column
                beam_nodei_coordinates = [
                    levels[n]["nodes"][levels[n]["info_beams"][j]["node_i"]]["x_coord"],
                    levels[n]["nodes"][levels[n]["info_beams"][j]["node_i"]]["y_coord"],
                ]
                beam_nodej_coordinates = [
                    levels[n]["nodes"][levels[n]["info_beams"][j]["node_j"]]["x_coord"],
                    levels[n]["nodes"][levels[n]["info_beams"][j]["node_j"]]["y_coord"],
                ]
                column_node_coordinates = [
                    levels[n]["nodes"][levels[n]["info_cols"][i]["node_j"]]["x_coord"],
                    levels[n]["nodes"][levels[n]["info_cols"][i]["node_j"]]["y_coord"],
                ]
                #calcules the lenght and angle of the beam connected to the column
                lenght, angle = geometric_info(
                    beam_nodei_coordinates,
                    beam_nodej_coordinates,
                    column_node_coordinates,
                )
                #stores the information of the beam
                connected_beam[j] = dict(
                    orientacion=angle,
                )


def extraer_vigas(levels):
    vigas = {}
    """Extracts the information of the beams making them objects of the class Beam

    Args:
        levels (dict): contains all the informatios of the building by level
    """
    for n in levels:
        for i in levels[n]["key_beams"]:

            seccion = {}
            datos_refuerzo = {}

            vigas[i] = dict(
                id=i,
                datos_seccion=seccion,
                refuerzo=datos_refuerzo,
                orientacion=[2, 3],
                longitud=2,
            )
    return vigas


print(columnas)
x = 2
