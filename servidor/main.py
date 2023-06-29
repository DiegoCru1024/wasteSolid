from flask import Flask, jsonify, request
from flask_cors import CORS
from learningModel import initializeModel
from PIL import Image
import numpy as np

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Llamamos la inicialización del modelo
modelo = initializeModel.cargarModelo()


@app.post('/api/sendData')
def recibirVideo():
    if 'frame' not in request.files:
        return jsonify({'error': 'No se proporcionó ninguna imagen'})

    image = request.files['frame']
    if image.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo'})

    image_file = request.files['frame']

    # Carga la imagen y la convierte en un tensor
    img = Image.open(image_file)
    img = img.resize((64, 64))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)


    # Realiza la predicción con el modelo
    prediction = modelo.predict(img_array)

    # Interpreta el resultado de la predicción
    if prediction[0] > 0.75:
        result = 'Reciclable'
    else:
        result = 'Residuo Orgánico'

    # Envía la respuesta
    return jsonify({'cat': result, 'pred': float(prediction[0])})


if __name__ == "__main__":
    app.run()
