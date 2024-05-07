import bpy
import json
import numpy as np

blend_filepath = 'C:/Users/kopan/OneDrive/Desktop/ГИИС/GIIS #6/project.blend'

with bpy.data.libraries.load(blend_filepath) as (data_from, data_to):
    data_to.objects = data_from.objects

all_vertices = []

for obj in data_to.objects:
    if obj.type == 'MESH':
        vertices = [v.co for v in obj.data.vertices]
        if vertices:
            all_vertices.append({
                "object_name": obj.name,
                "vertices": np.array(vertices).tolist()
            })

if all_vertices:
    output_filepath = './points.json'
    print('HI')
    with open(output_filepath, 'w') as file:
        json.dump(all_vertices, file)
else:
    print("Не удалось найти объекты типа 'Mesh' с вершинами в проекте.")