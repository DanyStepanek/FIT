from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from ikrlib import png2fea, wav16khz2mfcc
import re

data_folder_path = "../data/eval"
img_model_path = "cnn_image.h5"
voice_model_path = "nn_voice.h5"

data = []
labels = []

voice_model = load_model(voice_model_path, compile=True)
img_model = load_model(img_model_path, compile=True)

data = {}
img_data = png2fea(data_folder_path)
img_model.summary()

output_file = open('./predict_image_output.txt','w')

print("[INFO] evaluating image classifier...")
for k, v in img_data.items():
    #prepare data for model
    i_test_x = np.vstack(tuple(v))
    i_test_x = i_test_x.reshape(1, 80, 80, 3)
    i_test_x = np.r_[i_test_x]
    i_test_x = i_test_x.astype('float32')
    i_test_x /= 255
    #prediction
    predictions = img_model.predict_proba(i_test_x)
    p = np.argmax(predictions)
    name = re.search('.*/(\w*).png', k).group(1)
    #get result and write to output file
    result = predictions[0][1] * 10
    result = float("{:.2f}".format(result))
    if result >= 1.0:
        output_file.write(k + " " + " " + str(result) + " " + "1\n")
    else:
        output_file.write(k + " " + " " + str(result) + " " + "0\n")
    #add prediction result to data dict for detecting person
    data[name] = [predictions[0][1]]

output_file.close()

v_data = wav16khz2mfcc(data_folder_path)
voice_model.summary()

output_file = open('./predict_voice_output.txt', 'w')

print("[INFO] evaluating voice classifier...")
a = []
count = 0
#average value of results
mean = 1020
for k, v in v_data.items():
    #prepare data for model
    v_test_x = np.vstack(tuple(v))
    v_test_x = np.r_[v_test_x]
    v_test_x = v_test_x.astype('float32')
    v_test_x /= 255
    #predict
    predictions = voice_model.predict_proba(v_test_x)
    p = np.argmax(predictions)
    result = p - mean
    name = re.search('.*/(\w*).wav', k).group(1)

#    a.append(p)
    #write result to output file
    if result >= mean:
        output_file.write(k + " " + " " + str(result) + " " + "1\n")
        count +=1
    else:
        output_file.write(k + " " + " " + str(result) + " " + "0\n")

    #add prediction result to data dict for detecting person
    data[name].append(result)

#arithmetic average
#s = 0
#for v in a:
#    s += v
# mean = s / len(a)

output_file.close()

#complete person detection
output_file = open('./predict_person_output.txt', 'w')
count = 0
for k, v in data.items():
    #P = P(A) * P(B)
    result = v[0] * v[1] / 100
    result = float("{:.2f}".format(result))
    if result >= 0.5:
        output_file.write(k + " " + " " + str(result) + " " + "1\n")
        count += 1
    else:
        output_file.write(k + " " + " " + str(result) + " " + "0\n")

output_file.close()
print(count)
