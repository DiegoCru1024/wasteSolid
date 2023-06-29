from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
import os

savedModel = './learningModel/savedModel.h5'


def cargarModelo():
    if os.path.isfile(savedModel):
        loadedModel = load_model(savedModel)
        print("Modelo cargado exitosamente.")
        return loadedModel
    else:
        print("Modelo no encontrado, generando nuevo modelo.")
        generatedModel = generarModelo()
        print("Modelo generado exitosamente.")
        return generatedModel


def generarModelo():
    # Iniciamos el modelo y agregamos sus parámetros
    newModel = Sequential()
    newModel.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
    newModel.add(MaxPooling2D((2, 2)))
    newModel.add(Conv2D(64, (3, 3), activation='relu'))
    newModel.add(MaxPooling2D((2, 2)))
    newModel.add(Conv2D(128, (3, 3), activation='relu'))
    newModel.add(MaxPooling2D((2, 2)))
    newModel.add(Flatten())
    newModel.add(Dense(128, activation='relu'))
    newModel.add(Dense(1, activation='sigmoid'))

    # Compilamos el modelo generado
    newModel.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Seleccionamos los datos de entrenamiento y de prueba
    train_datagen = ImageDataGenerator(rescale=1.0 / 255.0, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    training_set = train_datagen.flow_from_directory('./dataset/train', target_size=(64, 64), batch_size=32,
                                                     class_mode='binary')
    test_set = test_datagen.flow_from_directory('./dataset/test', target_size=(64, 64), batch_size=32,
                                                class_mode='binary')

    newModel.fit(training_set, steps_per_epoch=len(training_set), epochs=10, validation_data=test_set,
                 validation_steps=len(test_set))

    test_loss, test_accuracy = newModel.evaluate(test_set, steps=len(test_set))
    print("Loss:", test_loss)
    print("Accuracy:", test_accuracy)

    newModel.save('./learningModel/savedModel.h5')
    return newModel