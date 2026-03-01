from collections import deque
import numpy as np

class SequenceBuffer:
    def __init__(self, window_size):
        self.buffer = deque(maxlen=window_size)

    def add(self, x):
        self.buffer.append(x)

    def is_ready(self):
        return len(self.buffer) == self.buffer.maxlen

    def get_sequence(self):
        return np.array(self.buffer).reshape(1, self.buffer.maxlen, -1)