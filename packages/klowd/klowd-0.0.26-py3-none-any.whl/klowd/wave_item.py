import numpy as np

WAVE_HEADER_SIZE = 20

class WaveItem:
    delays = []
    indices = []
    samples = []
    steps = []

    def __init__(self, blobData, indexType='ByDepth'):
        header_type=np.dtype([('index', 'd'), ('delay', 'f4'), ('step', 'f4'), ('count', 'i4')])
        offset = 0
        x = 0

        while offset < len(blobData):
            header = np.ndarray(1,header_type,blobData,offset)[0]
            offset = offset + WAVE_HEADER_SIZE
            count = header['count']
            values = np.frombuffer(blobData, dtype=np.int16, count=count, offset=offset)
            offset = offset + count * 2
            index = header['index']
            if index == index:
                self.delays.append(header['delay'])
                self.indices.append(index)
                self.samples.append(values)
                self.steps.append(header['step'])
