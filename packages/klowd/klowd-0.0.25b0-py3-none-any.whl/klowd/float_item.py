import numpy as np

class FloatItem:
    values=[]
    indices=[]

    def __init__(self, blobData, indexType='ByDepth'):
        dto=np.dtype([('index', 'd'), ('value', 'd')])
        pairs=np.ndarray(int(len(blobData)/16),dto,blobData,0)
        non_nan=pairs[(pairs['value'] == pairs['value'])]
        self.indices=non_nan['index']
        self.values=non_nan['value']
