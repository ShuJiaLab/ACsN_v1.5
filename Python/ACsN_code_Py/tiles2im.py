import numpy as np

def tiles2im(input, varargin):
    
    overlap = 0

    if varargin != None:
        overlap = varargin
    
    overlap = max(0, np.round(overlap))

    if overlap == 0:
        output = input
    else:
        ncells = input.shape
        ncells[2] = input.shape[2]

        Y = []
        for i in range(0, ncells[0]):
            Y.append(input[i, 0, 0]).shape[0]

        X = []
        for i in range(0, ncells[1]):
            X.append(input[0, i, 0]).shape[1]

        Z = []
        for i in range(0, ncells[2]):
            Z.append(input[0, 0, i]).shape[2]
        
        Y = np.array(Y)
        X = np.array(X)
        Z = np.array(Z)

        szy = Y.sum(axis=0) - overlap * (ncells[0] - 1)
        szx = X.sum(axis=0) - overlap * (ncells[1] - 1)
        output = np.zeros((szy, szx, Z.sum(axis=0)))

        for i in range(0, ncells[0]):
            for j in range(0, ncells[1]):
                for k in range(0, ncells[2]):

                    if i == 0:
                        head_y = 0
                        tail_y = Y[0]
                    else:
                        head_y = (Y[0:i-1]).sum(axis=0) - overlap * i
                        tail_y = (Y[0:i]).sum(axis=0) - overlap * i

                    if j == 0:
                        head_x = 0
                        tail_x = X[0]
                    else:
                        head_x = (X[0:j-1]).sum(axis=0) - overlap * j
                        tail_x = (X[0:j]).sum(axis=0) - overlap * j

                    if k == 0:
                        head_z = 0
                    else:
                        head_z = Z[0:k-1].sum(axis=0)
                    
                    tail_z = Z[0:k].sum(axis=0)

                    a = input[i, j, k]

                    # top left corner
                    # if there is any problem, get rid of "-1"
                    if i == 0 and j == 0:
                        output[head_y:head_y + overlap - 1, head_x:head_x + overlap - 1, head_z:tail_z] = a[0:overlap, 0:overlap, :]
                    else:
                        output[head_y:head_y + overlap - 1, head_x:head_x + overlap - 1, head_z:tail_z] = (output[head_y:head_y + overlap - 1, head_x:head_x + overlap -1, head_z:tail_z] + a[0:overlap, 0:overlap, :])/2
                    
                    # overlap in y
                    if i == 0:
                        output[head_y:head_y + overlap - 1, head_x + overlap:tail_x, head_z:tail_z] = a[0:overlap, 0:overlap, :]
                    else:
                        output[head_y:head_y + overlap - 1, head_x + overlap:tail_x, head_z:tail_z] = (output[head_y:head_y + overlap - 1, head_x + overlap:tail_x, head_z:tail_z] + a[0:overlap, 1 + overlap:, :])/2

                    # overlap in x
                    if j == 0:
                        output[head_y + overlap:tail_y, head_x:head_x + overlap - 1, head_z:tail_z] = a[1 + overlap:, 0:overlap, :]
                    else:
                        output[head_y + overlap:tail_y, head_x:head_x + overlap - 1, head_z:tail_z] = (output[head_y + overlap:tail_y, head_x:head_x + overlap - 1, head_z:tail_z] + a[1 + overlap:, 0:overlap, :])/2

                    output[head_y + overlap:tail_y, head_x + overlap:tail_x, head_z:tail_z] = a[1 + overlap:, 1 + overlap:, :]

    return output