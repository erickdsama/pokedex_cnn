import os
import sys

from tensorflow.python.keras import optimizers
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation, Convolution2D, MaxPooling2D
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

# limpiar sesiones que pudieron estar corriendo
# K.clear_session()


training_data = "./pruebas"
validation_data = "./validation"

dirs = next(os.walk(training_data))[1]

epochs = 10
target_size = 150, 150
batch_size = 32
steps = 
validatation_steps = 1000
conv1_filters = 32
conv2_filters = 64
conv3_filters = 128
conv4_filters = 256
filter_size1 = (3, 3)
filter_size2 = (3, 3)
filter_size3 = (2, 2)
filter_size4 = (2, 2)
pool_size = (2, 2)
classes = len(dirs)
lr = 0.0005
print(classes)


traing_imgs = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2, 
    horizontal_flip=True
)

test_data = ImageDataGenerator(rescale=1. /255)

generator_train = traing_imgs.flow_from_directory(
    training_data,
    target_size=target_size, 
    batch_size=batch_size,
    class_mode='categorical'
)

print("data=", generator_train.class_indices)
generator_validate = traing_imgs.flow_from_directory(
    validation_data,
    target_size=target_size, 
    batch_size=batch_size,
    class_mode='categorical'
)

cnn = Sequential()
model = load_model('./modelo/modelo.h5')
for layer in model.layers:
    cnn.add(layer)
cnn.layers.pop()
for layer in cnn.layers:
    layer.trainable = False


# cnn.add(Convolution2D(conv1_filters, filter_size1, padding="same", input_shape=target_size+(3,), activation="relu"))

# cnn.add(MaxPooling2D(pool_size=pool_size))

# cnn.add(Convolution2D(conv2_filters, filter_size1, padding="same"))

# cnn.add(MaxPooling2D(pool_size=pool_size))

# cnn.add(Flatten())
# # numero de neuronas al mismo tiempo
# cnn.add(Dense(256, activation="relu"))
# # apagar neuronas al azar
# # cnn.add(Dropout(0.5))
# # normalizar la salida con softmax y el numero de clases que se entreno
# cnn.add(Dense(classes, activation='softmax'))

cnn.compile(loss="categorical_crossentropy",
                    optimizer=optimizers.Adam(lr=lr), 
                    
                    metrics=["accuracy"])

cnn.fit_generator(
    generator_train,
    steps_per_epoch=steps,
    epochs=epochs,
    validation_data=generator_validate,
    validation_steps=validatation_steps)

target_dir = './modelo/'
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
cnn.save('./modelo/modelo.h5')
cnn.save_weights('./modelo/pesos.h5')


