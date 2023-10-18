import numpy as np

def createRow(n, classes):
    base = np.sin(np.linspace((np.random.rand(3)),(np.random.rand(3) + np.array([10,15,7])),n))
    if classes[0] > 0:
        base[np.random.randint(0,n), 0] += 2
    if classes[1] > 0:
        base[np.random.randint(0,n), 1] -= 2
    if classes[2] > 0:
        x = np.random.randint(0,n-5)
        base[x:x+4,2] = 0
    if classes[3] > 0:
        x = np.random.randint(0,n-10)
        base[x:x+8,1] += 1.5
    if classes[4] > 0:
        x = np.random.randint(0,n-7)
        base[x:x+6,0] += 1.5
        base[x:x+6,2] -= 1.5
    base += np.random.rand(*base.shape)*.2
    return base

def generate_data(n: int) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
    """
    Generates data with n rows
    the samples are then split into training and testing sets (80/20)

    :param n: number of rows to generate
    :return: x_train, y_train, x_test, y_test
    """
    xl, yl = [], []
    for _ in range(n):
        cl = np.random.rand(5)<.25
        xl.append(createRow(np.random.randint(40,60), cl))
        yl.append(cl)

    # create a split for training and testing
    split = int(n*.8)
    x_train = np.array(xl[:split])
    y_train = np.array(yl[:split])
    x_test = np.array(xl[split:])
    y_test = np.array(yl[split:])
    return x_train, y_train, x_test, y_test