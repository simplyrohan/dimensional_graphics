def get_points(data: list):
    points = []
    for line in data:
        split_line = line.split()
        try:
            if split_line[0] == "v":
                points.append([float(i) for i in split_line[1:]])
        except IndexError:
            print("Found Line Break!")

    return points


def get_edges(data):
    edges = []
    for line in data:
        split_line = line.split()
        try:
            if split_line[0] == "f":
                inds = split_line[1:]
                inds = [i.split("/")[0] for i in inds]
                edges.append(inds)
        except IndexError:
            print("Found Line Break!")

    return edges


def get_faces(path: str) -> list:
    with open(path, "r") as file:
        lines = file.readlines()
        points = get_points(lines)
        edges = get_edges(lines)

        print(len(points))

        faces = []

        for edge in edges:
            face = []
            for ind in edge:
                print(int(ind))
                print("LEN:", (len(points)))

                point = points[int(ind)-1]

                face.append(point)
            
            faces.append(face)
        
        # faces = faces[::10]




    return faces

with open("faces.txt", "w") as f:
    f.write(str(get_faces("Gun.obj")))