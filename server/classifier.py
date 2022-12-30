import numpy as np
import cv2
import pywt
import json
import pickle
from matplotlib import pyplot as plt
import base64

# ------------------ IMPORT MODEL AND DICTIONARY ------------------
dict_name = {}
dict_number = {}
final_model = None

def load_model():
    print("Loading final model")
    global dict_name
    global dict_number

    with open("./final_model/class_dictionary.json", "r") as file:
        dict_name = json.load(file)
        dict_number = {v:k for k,v in dict_name.items()}

    global final_model
    if final_model is None:
        with open('./final_model/best_model.pkl', 'rb') as file:
            final_model = pickle.load(file)

    print("Done!")

# ------------------ BASE 64 ------------------
def get_base64(b64str):
    encoded_data = b64str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    return img

# ------------------ DETECT FACE AND EYES ------------------
face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

def get_cropped_image_if_2_eyes(image_path, image_b64):

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_base64(image_b64)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cropped_faces = []
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
            #plt.figure()
            #plt.imshow(roi_color)
            #plt.show()
    
    return cropped_faces

# ------------------ WAVELETS ------------------
def w2d(img, mode='haar', level=1):
    imArray = img
    #Datatype conversions
    #convert to grayscale
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    #convert to float
    imArray =  np.float32(imArray)
    imArray /= 255;
    # compute coefficients
    coeffs=pywt.wavedec2(imArray, mode, level=level)

    #Process Coefficients
    coeffs_H=list(coeffs)
    coeffs_H[0] *= 0;

    # reconstruction
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)

    return imArray_H


# -------------- CLASSIFY IMAGE --------------
def classify_image(image_b64, image_path):

    imgs = get_cropped_image_if_2_eyes(image_path, image_b64)
    
    result = []
    for img in imgs:

        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = w2d(img, 'db1', 5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32 * 32 * 3, 1), scalled_img_har.reshape(32 * 32, 1)))

        len_image_array = 32*32*3 + 32*32
        final = combined_img.reshape(1,len_image_array).astype(float)

        class_predicted = final_model.predict(final)[0]
        class_prob = final_model.predict_proba(final)[0]
        class_prob = np.around(class_prob*100,2).tolist() # para converter para JSON não pode ter arrays nem números inteiros

        result.append({
                    'class_predicted': dict_number[class_predicted], 
                    'class_probability': class_prob,
                    'class_dictionary': dict_name,
                    })

    return result


if __name__ == '__main__':
    load_model()
    #image_path = "./test_images/Jennifer_test1.jpeg"
    image_path = None
    image_b64 = True
    
    if image_b64 is True:
        with open("./test_images/b64_courteney.txt") as file:
            image_b64 = file.read()

    result = classify_image(image_b64, image_path)
    print(result)






