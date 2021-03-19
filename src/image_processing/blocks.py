import numpy as np

c = np.arange(640*640).reshape(640, 640)
print(c.shape)


def slice_array(array, depth, width):
    h, w = array.shape
    return (array.reshape(h // depth, depth, -1, width)
            .swapaxes(1, 2)
            .reshape(-1, depth, width))

def unslice_array(array):
    h = 640
    w = 640
    n, nrows, ncols = array.shape
    return (array.reshape(h//nrows, -1, nrows, ncols)
               .swapaxes(1,2)
               .reshape(h, w))

c = slice_array(c, 20, 20)
print(c.shape)
c = unslice_array(c)
print(c.shape)
