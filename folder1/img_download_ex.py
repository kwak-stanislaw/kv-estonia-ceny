path = file_name + ".png"

foto = requests.get(url, headers=headers, stream=True)
with open(path, "b+w") as f:
    f.write(foto.content)