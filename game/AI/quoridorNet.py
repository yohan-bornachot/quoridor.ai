from torch.nn import Module

class QuoridorNet(Module):

    def __init__(self, input_size, nb_channels) -> None:
        super().__init__()