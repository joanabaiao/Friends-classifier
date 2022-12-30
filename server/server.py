from flask import Flask, request, jsonify
import classifier

app = Flask(__name__)

@app.route('/classify_image', methods=['GET', 'POST'])

def classify_image():

    image_data = request.form['image_data']
    #print(image_data)
    response = classifier.classify_image(image_data, None)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Friends Image Classification")
    classifier.load_model()
    app.run(port=5000)

