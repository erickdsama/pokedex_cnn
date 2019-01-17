import sys

import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

from index_classes import get_class_by_index
from Pokemon import Pokemon

longitud, altura = 150, 150
modelo = './modelo/modelo.h5'
pesos_modelo = './modelo/pesos.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)

def predict(file):
  x = load_img(file, target_size=(longitud, altura))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = cnn.predict(x)
  print("array", array)
  result = array[0]
  answer = np.argmax(result)
  return get_class_by_index(answer)

if __name__ == "__main__":
    file =  sys.argv[1]
    res = predict(file)
    pokemon = Pokemon(res)
    print("POkemon", pokemon.name)
    print("POkemon", pokemon.id)
    print("POkemon", pokemon.types[0]["type"])
    print("POkemon", pokemon.flavor_text_entries[1]['flavor_text'])


# print("res=", predict("./to_predict/char.jpeg"))