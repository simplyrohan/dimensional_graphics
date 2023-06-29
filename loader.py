def get_points(data: list):
    points = []
    for line in data:
        split_line = line.split()
        try:
            if split_line[0] == "v":
                points.append([float(i) for i in split_line[1:]])
        except IndexError:
            # print("Found Line Break!")
            pass

    return points


def get_edges(data):
    edges = []
    for line in data:
        split_line = line.split()
        try:
            if split_line[0] == "f":
                inds = split_line[1:]
                inds = [i.split("/")[:2] for i in inds]
                edges.append(inds)
        except IndexError:
            pass
            # print("Found Line Break!")

    return edges

def get_uvs(data):
    points = []
    for line in data:
        split_line = line.split()
        try:
            if split_line[0] == "vt":
                points.append([float(i) for i in split_line[1:3]])
        except IndexError:
            pass
            # print("Found Line Break!")
    if not points:
        points = [(0, 0), (1, 0), (0, 1)]
    return points

def get_faces(path: str) -> list:
    with open(path, "r") as file:
        lines = file.readlines()
        points = get_points(lines)
        edges = get_edges(lines)
        uvs = get_uvs(lines)

        faces = []

        for edge in edges:
            face = []
            for ind in edge:
                i,u = ind
                point = points[int(i)-1]
                print(len(uvs))
                print(int(u)-1)
                uv = uvs[int(u)-1]
                
                face.append(point+uv)
            
            faces.append(face)
        
        # faces = faces[::10]




    return faces

def load(file):
    return get_faces(file)