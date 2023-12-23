import os
import hydra
from matplotlib import pyplot as plt
import numpy as np
from omegaconf import OmegaConf
import torch
from torch import nn
from tqdm import tqdm

from model.HomeBrewRNN import HomeBrewRNNAttention
from data.create_dataloader import create_dataloader
from train import set_seed

def load_checkpoint(checkpoint_path, config):
    """Load model and optimizer from a checkpoint."""
    checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    model = HomeBrewRNNAttention(
        hidden_size=config.hidden_size, 
        num_layers=config.num_layers, 
        num_classes=config.num_classes, 
        dropout=config.dropout,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint["epoch"]
    return model, optimizer, epoch

def analyze_model(model, loader):
    model.eval()
    label_attn_weights = {}
    with torch.no_grad():
        for inputs, labels in loader:
            _, attn_weights = model(inputs)
            attn_weights = attn_weights.cpu().numpy()

            for label, weight in zip(labels, attn_weights):
                # Convert label to string key
                label_key = ''.join(label.numpy().astype(int).astype(str))

                # Initialize the list for this key if not already done
                if label_key not in label_attn_weights:
                    label_attn_weights[label_key] = []

                # Append the attention weights for this label
                label_attn_weights[label_key].append(weight)

    return label_attn_weights

def analyze_model_whole(model, loader):
    model.eval()
    all_attn_weights = []
    with torch.no_grad():
        for inputs, label in loader:
            _, attn_weights = model(inputs)
            all_attn_weights.append(attn_weights.cpu().numpy())
    return all_attn_weights

def plot_attention_weights(attn_weights, sensor_idx):
    # Average attention weights across all samples for a specific sensor
    avg_weights = np.mean(np.array(attn_weights)[:, :, sensor_idx], axis=0)
    fig = plt.figure(figsize=(10,6))
    plt.plot(avg_weights)
    plt.title(f"Average Attention Weights for Sensor {sensor_idx}")
    plt.xlabel("Time Step")
    plt.ylabel("Attention Weight")
    return fig

def plot_small_multiples(all_attn_weights, exclude_last=20):
    # Determine the number of subplots
    num_plots = len(all_attn_weights)
    num_cols = 4  # Adjust the number of columns as needed
    num_rows = (num_plots + num_cols - 1) // num_cols

    # Create a figure with subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, num_rows * 3))
    axes = axes.flatten()  # Flatten the axes array for easy iteration

    for idx, (label_key, weights) in enumerate(all_attn_weights.items()):
        avg_weights = np.mean(np.array(weights)[:, :-exclude_last], axis=0)
        ax = axes[idx]
        ax.plot(avg_weights)
        ax.set_title(f"Label: {label_key}")
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Average Attention Weight")

        # Hide x and y ticks for clarity
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.yaxis.set_tick_params(labelleft=False)

    # Hide unused subplots
    for idx in range(len(all_attn_weights), len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    return fig


@hydra.main(config_path="../config", config_name="train", version_base=None)
def main(cfg: OmegaConf):
    model, optimizer, epoch = load_checkpoint("checkpoints/checkpoint_attention.pth", config=cfg)
    _, test_loader = create_dataloader(cfg.batch_size) 
    all_attn_weights = analyze_model(model, test_loader)
    
    # sort by number of 1s in label ascending then lexographically
    all_attn_weights = dict(sorted(all_attn_weights.items(), key=lambda x: (sum([int(i) for i in x[0]]), x[0])))


    fig = plot_small_multiples(all_attn_weights, exclude_last=15)
    fig.savefig("charts/small_multiples.png")


if __name__ == "__main__":
    set_seed(42)
    main()