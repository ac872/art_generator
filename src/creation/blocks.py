
def slice_array(array, num_rows, num_cols):
    h, w = array.shape
    return (array.reshape(h // num_rows, num_rows, -1, num_cols)
            .swapaxes(1, 2)
            .reshape(-1, num_rows, num_cols))


def combine_array(arr, h, w):
    n, num_rows, num_cols = arr.shape
    return (arr.reshape(h // num_rows, -1, num_rows, num_cols)
            .swapaxes(1, 2)
            .reshape(h, w))
