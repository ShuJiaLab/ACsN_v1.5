import os
from skimage import io
import numpy as np
import pickle

# Assumes the input the user enters is a directory with only
# tiff files

#####################
# Offset and Variance Calculations

images_folder_path = input("Enter Folder Path: ")
if not os.path.isdir(images_folder_path):
    print("User did not enter a readable directory.")
else:
    Offset = []
    Variance = []
    list_of_images = os.listdir(images_folder_path)
    L = len(list_of_images)
    for i in range(0, L): #change to L after triall runs
        print("Loading: " + list_of_images[i])
        full_image_name = images_folder_path + "/" + list_of_images[i] #get full name of the file
        im = io.imread(full_image_name)
        imarray = np.array(im)
        imarray = np.transpose(imarray).copy() #transposing the first dimension to be the third dimension
        Offset.append(np.mean(imarray, axis=2))
        Variance.append(np.var(imarray, axis=2))

Offset = np.transpose(Offset).copy()
Variance = np.transpose(Variance).copy()

Offset = np.mean(Offset, 2)
Variance = np.mean(Variance, 2)

print("Done calculating offset and variance\n")

with open('Pickle Files/Offset.pkl', 'wb') as f:
    pickle.dump(Offset, f)
with open('Pickle Files/Variance.pkl', 'wb') as f:
    pickle.dump(Variance, f)


#######################
# Gain Calibration

N = 10

G = []
V = []

for i in range (0,N):
    images_folder_path = input("\nEnter Folder Path: ")
    if not os.path.isdir(images_folder_path):
        print("User did not enter a readable directory.")
    else:
        list_of_images = os.listdir(images_folder_path)
        L = len(list_of_images)

        G_temp = []
        V_temp = []

        for k in range(0, L):
            full_image_name = images_folder_path + "/" + list_of_images[i] #get full name of the file
            im = io.imread(full_image_name)
            imarray = np.array(im)
            imarray = np.transpose(imarray).copy() #transposing the first dimension to be the third dimension
            G_temp.append(np.mean(imarray, axis=2))
            V_temp.append(np.var(imarray, axis=2))
        
        G_temp = np.transpose(G_temp).copy()
        V_temp = np.transpose(V_temp).copy()

        G.append(np.mean(G_temp, axis=2))
        V.append(np.mean(V_temp, axis=2))


G = np.array(G)
V = np.array(V)
G = np.transpose(G).copy()
V = np.transpose(V).copy()

row = len(G)
col = len(G[0])
Gain = np.zeros((row, col))

for i in range(0, row):
    for j in range(0, col):
        A = np.array(([(V[i][j] - Variance[i][j])])).transpose()
        B = np.array(([(G[i][j] - Offset[i][j])])).transpose()
        Gain[i][j] = (np.linalg.lstsq(B, A, rcond=None))[0]

with open('Pickle Files/Gain.pkl', 'wb') as f:
    pickle.dump(Gain, f)