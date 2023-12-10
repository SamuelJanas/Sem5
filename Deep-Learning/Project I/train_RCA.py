import hydra
from omegaconf import OmegaConf
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from data.create_dataloader import create_dataloader
from model.HomeBrewRNN import HomeBrewRNNAttention

def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    for inputs, labels in loader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs, attn_weights = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

def test_epoch(model, loader, criterion, device):
    model.eval()
    total_loss = 0
    all_attn_weights = []
    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs, attn_weights = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            all_attn_weights.append(attn_weights.cpu().numpy())
    return total_loss / len(loader), all_attn_weights

def plot_attention_weights(attn_weights, sample_idx, sensor_idx):
    # Initialize an empty list to collect weights
    collected_weights = []

    # Iterate over each batch's attention weights
    for batch_weights in attn_weights:
        # batch_weights shape is expected to be [batch_size, sequence_length, num_sensors]
        if batch_weights.shape[0] > sample_idx:  # Check if the batch contains the sample
            collected_weights.append(batch_weights[sample_idx, :, sensor_idx])

    # Convert the list of arrays into a single 2D array
    weights = np.vstack(collected_weights)
    plt.imshow(weights, cmap='hot', interpolation='nearest')
    plt.title(f"Attention Weights for Sensor {sensor_idx}")
    plt.xlabel("Time Step")
    plt.ylabel("Batch")
    plt.colorbar()
    plt.show()

@hydra.main(config_path="config", config_name="train", version_base=None)
def main(cfg: OmegaConf):
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Load data
    train_loader, test_loader = create_dataloader(batch_size=32)

    # Initialize model
    model = HomeBrewRNNAttention(        
        hidden_size=cfg.hidden_size, 
        num_layers=cfg.num_layers, 
        num_classes=cfg.num_classes, 
        dropout=cfg.dropout,
        ).to(device)

    # Loss and optimizer
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    epochs = 7
    best_test_loss = float('inf')
    checkpoint_path = "checkpoints/checkpoint_attention.pth"

    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader, criterion, optimizer, device)
        test_loss, attn_weights = test_epoch(model, test_loader, criterion, device=device)
        print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss:.4f}, Test Loss: {test_loss:.4f}")

        # Save the model if it has the best test loss so far
        if test_loss < best_test_loss:
            best_test_loss = test_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': test_loss,
            }, checkpoint_path)
            print(f"Checkpoint saved at epoch {epoch+1}")

        # [Optional] Plot attention weights
        if epoch == epochs - 1:
            plot_attention_weights(attn_weights, sample_idx=0, sensor_idx=0)



if __name__ == "__main__":
    main()
