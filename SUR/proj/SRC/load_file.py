import matplotlib.pyplot as plt
from glob import glob
import numpy as np

# load image as pixel array
def load_file(dir_name):
    features = {}
    for f in glob(dir_name + '/*.png'):
        print('Processing file: ', f)
        features[f] = np.average(plt.imread(f), weights=[0.299, 0.587, 0.114], axis=2)
    return features
