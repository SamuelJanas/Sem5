import torch.nn as nn

class HomeBrewRNN(nn.Module):
    """
        A simple RNN model for sequence classification.

        Input: (batch_size, 3, 60)
    """
    def __init__(self):
        super(HomeBrewRNN, self).__init__()
        
        self.conv_layers = nn.Sequential(
            nn.Conv1d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            
            nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),

            nn.Conv1d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2)
        )
        
        self.fc_layers = nn.Sequential(
            nn.Linear(256*7, 128),  # Note: 7 is due to three MaxPooling operations on a sequence of length 60
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, 5),
            nn.Sigmoid()  # Activation function for multi-label classification
        )
        
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)  # Flatten
        x = self.fc_layers(x)
        return x