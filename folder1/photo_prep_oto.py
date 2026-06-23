from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image_path = '/Users/drizzleinthebottle/Downloads/paths_check/otomoto_0_0.png'
img = Image.open(image_path).convert('RGB')  # RGB mode
img_array = np.array(img)  # Shape: (height, width, 3)
print(img_array.shape)

plt.imshow(img_array)
# plt.axis('off')
plt.show()

# Wyciągniij pierwsze zdjęcie z każdego ogłoszenia.
# Stwórz skrypt do przygotowania danych (oczyszczenie i aaugemntacji (min. 10 transformacji)
