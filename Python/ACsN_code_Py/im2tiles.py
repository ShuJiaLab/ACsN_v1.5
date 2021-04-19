import numpy as np
import skimage
import os
import math

def im2tiles(a, Overlap = None, nx = None, ny = None, nz = None):
    
    Nx = 128
    Ny = 128
    Nz = a.shape[2]
    overlap = 0

    if Overlap != None:
        overlap = Overlap
    if nx != None:
        Nx = nx
    if ny != None:
        Ny = ny
    if nz != None:
        Nz = nz

    overlap = max(0, round(overlap))
    ny = math.floor(a.shape[0]/Ny)
    reminder_y = a.shape[0] % Ny

    dimyDist = Ny * np.ones((1 , ny))

    if reminder_y <= overlap:
        dimyDist[-1] = dimyDist[-1] + reminder_y
    else:
        dimyDist = np.concatenate((dimyDist, reminder_y), axis = 1)

    nx = math.floor(a.shape[1]/Nx)
    reminder_x = a.shape[1] % Nx

    dimxDist = Nx * np.ones((1, nx))

    if reminder_x <= overlap:
        dimxDist[-1] = dimxDist[-1] + reminder_x
    else:
        dimxDist = np.concatenate((dimxDist, reminder_x), axis = 1)
    
    if overlap == 0:
        if len(a[0][0]) == 1:
            A = [a, dimyDist, dimxDist]
        else:
            nz = math.floor(len(a[0][0])/Nz)
            reminder_z = len(a[0][0]) % Nz
            dimzDist = Nz * np.ones((1, nz))

            if reminder_z != 0:
                dimzDist = np.concatenate((dimzDist, np.array([[reminder_z]])), axis=1)

            A = a
    
    else:
        if len(a[0][0]) == 1:
            sizey = dimyDist.shape[1]
            sizex = dimxDist.shape[1]

            A = []

            for i in range(0, sizey):
                for j in range(0, sizex):

                    if i == 0:
                        head_y = 0
                    else:
                        head_y = (i - 1) * dimyDist[i - 1]
                    
                    if j == 0:
                        head_x = 0
                    else:
                        head_x = (j - 1) * dimxDist[j - 1]
                    
                    if i == (sizey - 1):
                        tail_y = (dimyDist[0:i+1]).sum(axis = 0)
                    else:
                        tail_y = (dimyDist[0:i+1]).sum(axis = 0) + overlap

                    if j == (sizex - 1):
                        tail_x = (dimxDist[0:i+1]).sum(axis = 0)
                    else:
                        tail_x = (dimxDist[0:i+1]).sum(axis = 0) + overlap

                    temp = a[head_y:tail_y+1, head_x:tail_x+1]
                
                A.append(temp)


        else:
            nz = math.floor(len(a[0][0])/Nz)
            reminder_z = len(a[0][0]) % Nz
            dimzDist = Nz * np.ones((1, nz))

            dimzDist = np.concatenate((dimzDist, reminder_z), axis=1)

            sizey = dimyDist.shape[1]
            sizex = dimxDist.shape[1]
            sizez = dimzDist.shape[1]

            A = []

            for i in range(0, sizey):
                for j in range(0, sizex):
                    temp2 = []
                    for k in range(0, sizez):

                        if i == 0:
                            head_y = 0
                        else:
                            head_y = (i - 1) * dimyDist[i - 1]
                    
                        if j == 0:
                            head_x = 0
                        else:
                            head_x = (j - 1) * dimxDist[j - 1]

                        if k == 0:
                            head_z = 0
                        else:
                            head_z = (k - 1) * dimxDist[k - 1]

                        if i == (sizey - 1):
                            tail_y = (dimyDist[0:i+1]).sum(axis = 0)
                        else:
                            tail_y = (dimyDist[0:i+1]).sum(axis = 0) + overlap

                        if j == (sizex - 1):
                            tail_x = (dimxDist[0:i+1]).sum(axis = 0)
                        else:
                            tail_x = (dimxDist[0:i+1]).sum(axis = 0) + overlap
                        
                        tail_z = (dimzDist[0:k+1]).sum(axis = 0)

                        temp = a[head_y:tail_y+1, head_x:tail_x+1, head_z:tail_z+1]                           

                    temp2.append(temp)
                
                A.append(temp2)
    
    return np.array(A)