import sys

import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

longitud, altura = 150, 150
modelo = './modelo/modelo.h5'
pesos_modelo = './modelo/pesos.h5'
cnn = load_model(modelo)
cnn.load_weights(pesos_modelo)

data_trained= {'blastoise': 0, 'bulbasaur': 1, 'charizard': 2, 'charmander': 3, 'charmeleon': 4, 'ivysaur': 5, 'squirtle': 6, 'venusaur': 7, 'wartortle': 8}

def predict(file):
  x = load_img(file, target_size=(longitud, altura))
  x = img_to_array(x)
  x = np.expand_dims(x, axis=0)
  array = cnn.predict(x)
  print("array=", array)
  result = array[0]
  answer = np.argmax(result)
  print(np.sum(result))
  return [k for k,v in data_trained.items() if v == answer]
#   return answer

if __name__ == "__main__":
    file =  sys.argv[1]
    res = predict(file)
    print("res=", res[0])
# print("res=", predict("./to_predict/char.jpeg"))