def get_map(filename):
    """
    This function loads an array based on a map stored as a list of
    numbers separated by commas.
    See http://arcade.academy/examples/sprite_csv_map.html for 
    a more detailed example.
    """
    with open(filename) as file:
        map_array = []
        for line in file:
            line = line.strip()
            map_row = line.split(",")
            for index, item in enumerate(map_row):
                map_row[index] = int(item)
            map_array.append(map_row)
        return map_array