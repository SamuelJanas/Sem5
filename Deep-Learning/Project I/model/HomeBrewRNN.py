from torch import nn

class HomeBrewRNN(nn.Module):
    """
    A model that first uses convolutional layers to extract features from the signal,
    then uses LSTM to model the sequence, and finally classifies using fully connected layers.
    Input: (batch_size, 3, 60)
    """
    def __init__(self, hidden_size=128, num_layers=1, num_classes=5, dropout=0.5):
        super(HomeBrewRNN, self).__init__()
        
        # Convolutional layers for feature extraction
        self.conv_layers = nn.Sequential(
            nn.Conv1d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            
            nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
        )
        
        # LSTM for sequence modeling
        self.lstm = nn.LSTM(
            input_size=15,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        
        # Fully connected layers for classification
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, num_classes),  # Connect last LSTM hidden state to the output layer
            nn.Sigmoid()  # Activation function for multi-label classification
        )
        
    def forward(self, x):
        # Extract features using convolutional layers
        x = self.conv_layers(x)
        
        # Pass extracted features through LSTM
        _, (h_n, _) = self.lstm(x)
        
        # Take the last hidden state of the last layer of LSTM
        x = h_n[-1]
        
        # Classify using fully connected layers
        x = self.fc(x)
        return x