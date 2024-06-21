import json

# Cargar el archivo JSON
with open('tones.json', 'r') as file:
    data = json.load(file)


data = data[0]['tones']


for strings in data:
    print(data[strings])
    



# Iterar sobre cada objeto en la lista y agregar la nueva clave
for obj in data:
    tones = obj.get('tones', {})  # Obtener el diccionario 'tones' del objeto actual

    for string in tones:
        for fret in string:
            for frett in fret:
                print(frett)

    # print(tones)
    new_data = {
        "note": "F4",
        "freq": 349.23
    }
    tones["1"] = new_data  # Agregar el nuevo dato bajo la clave '1' en 'tones'
    obj['tones'] = tones  # Actualizar el diccionario 'tones' en el objeto actual

# Guardar los cambios de vuelta al archivo JSON
# with open('tones.json', 'w') as file:
    # json.dump(data, file, indent=2)  # indent=2 para una mejor legibilidad

print("Nueva clave agregada exitosamente a cada objeto en el archivo JSON.")
