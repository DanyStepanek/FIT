import matplotlib.pyplot as plt
from ikrlib import raw8khz2mfcc, logpdf_gauss, train_gauss, train_gmm, logpdf_gmm, png2fea, wav16khz2mfcc
import scipy.linalg
import numpy as np
from numpy.random import randint

target_train_v = wav16khz2mfcc('../data/target_train').values()
target_dev_v = wav16khz2mfcc('../data/target_dev').values()
non_target_train_v  = wav16khz2mfcc('../data/non_target_train').values()
non_target_dev_v  = wav16khz2mfcc('../data/non_target_dev').values()

target_train_v = np.vstack(tuple(target_train_v))
target_dev_v = np.vstack(tuple(target_dev_v))
non_target_train_v = np.vstack(tuple(non_target_train_v))
non_target_dev_v = np.vstack(tuple(non_target_dev_v))

dim = target_train_v.shape[1]
print(dim)
# PCA reduction to 2 dimensions

cov_tot = np.cov(np.vstack([target_train_v, non_target_train_v]).T, bias=True)
# take just 2 largest eigenvalues and corresponding eigenvectors
d, e = scipy.linalg.eigh(cov_tot, eigvals=(dim-2, dim-1))

target_train_v_pca = target_train_v.dot(e)
non_target_train_v_pca = non_target_train_v.dot(e)
plt.plot(target_train_v_pca[:,1], target_train_v_pca[:,0], 'b.', ms=1)
plt.plot(non_target_train_v_pca[:,1], non_target_train_v_pca[:,0], 'r.', ms=1)
plt.show()

# LDA reduction to 1 dimenzion (only one LDA dimension is available for 2 tridy)
t_t_v = len(target_train_v)
n_t_t_v = len(non_target_train_v)
cov_wc = (t_t_v*np.cov(target_train_v.T, bias=True) + n_t_t_v*np.cov(non_target_train_v.T, bias=True)) / (t_t_v + n_t_t_v)
cov_ac = cov_tot - cov_wc
d, e = scipy.linalg.eigh(cov_ac, cov_wc, eigvals=(dim-1, dim-1))
plt.figure()
junk = plt.hist(target_train_v.dot(e), 40, histtype='step', color='b', normed=True)
junk = plt.hist(non_target_train_v.dot(e), 40, histtype='step', color='r', normed=True)
plt.show()
