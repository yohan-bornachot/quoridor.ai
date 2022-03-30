from torch import nn, reshape, hstack, clone

class QNet(nn.Module):
    def __init__(self, board_size, nb_channels, kernel_size, mlp_sizes, nb_futur_states) -> None:
        super().__init__()
        
        self.board_size = board_size
        self.nb_conv_layers = len(nb_channels)
        self.nb_channels = [2] + nb_channels
        self.kernel_size = kernel_size
        self.nb_mlp_layers = len(mlp_sizes) - 1
        self.mlp_sizes = mlp_sizes
        self.nb_futur_state = nb_futur_states

        self.conv_pool = nn.ModuleList(
            [nn.Sequential(nn.Conv2d(self.nb_channels[i], self.nb_channels[i+1], self.kernel_size, stride = 1, padding = "same"),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)) for i in range(self.nb_conv_layers)]
        )
        

        self.mlp = nn.ModuleList(
            [nn.Sequential(
                nn.Linear(mlp_sizes[i], mlp_sizes[i+1]),
                nn.ReLU()
            ) for i in range(self.nb_mlp_layers)]
        )

        self.head = nn.Linear(self.mlp_sizes[-1],nb_futur_states)
    
    def forward(self, board, positions, goals, nb_walls):
        
        x = clone(board)
        for i in range(len(self.conv_pool)):
            x = self.conv_pool[i](x)
        
        b, c, h, w = x.shape
        x = reshape(x, (b, c*h*w))
        x = hstack((x,positions,goals,nb_walls))
        
        for i in range(len(self.mlp)):
            x = self.mlp[i](x)

        x = self.head(x)

        return x


        
