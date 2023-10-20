import os
import hydra
from matplotlib import pyplot as plt
from omegaconf import OmegaConf
import torch
from torch import nn
from tqdm import tqdm

from model.HomeBrewRNN import HomeBrewRNN
from data.create_dataloader import create_dataloader
from train import set_seed

def load_checkpoint(checkpoint_path, config):
    """Load model and optimizer from a checkpoint."""
    checkpoint = torch.load(checkpoint_path)
    model = HomeBrewRNN(
        hidden_size=config.hidden_size, 
        num_layers=config.num_layers, 
        num_classes=config.num_classes, 
        dropout=config.dropout,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr)
    model.load_state_dict(checkpoint["model"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    epoch = checkpoint["epoch"]
    return model, optimizer, epoch

def plot_loss_chart(losses, save_path):
    plt.figure(figsize=(10,6))
    plt.plot(losses, label="Loss", color='blue')
    
    avg_loss = sum(losses) / len(losses)
    plt.axhline(y=avg_loss, color='orange', linestyle='--', label="Average Loss")
    
    plt.title("Evaluation Loss")
    plt.xlabel("Batch")
    plt.ylabel("Loss")
    plt.legend()
    plt.savefig(save_path)

@torch.no_grad()
def evaluate(model, loader, criterion, cfg):
    model.eval()
    total_predictions = 0
    correct_predictions = 0
    losses = []

    progress_bar = tqdm(loader, desc="Evaluating")
    for inputs, labels in progress_bar:
        inputs = inputs.to(cfg.device)
        labels = labels.to(cfg.device)

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        losses.append(loss.item())

        # Convert outputs to binary predictions
        predicted = (outputs > 0.5).float()

        # Count correct predictions
        correct_predictions += (predicted == labels).sum().item()
        total_predictions += predicted.numel()  # or alternatively: labels.size(0) * labels.size(1)

    accuracy = 100.0 * correct_predictions / total_predictions
    return losses, accuracy


@hydra.main(config_path="../config", config_name="train", version_base=None)
def main(cfg: OmegaConf):
    model, optimizer, epoch = load_checkpoint("checkpoints/checkpoint_002.pt", config=cfg)
    _, test_loader = create_dataloader(cfg.batch_size) 
    criterion = nn.BCELoss()

    losses, accuracy = evaluate(model, test_loader, criterion, cfg)
    print(f"Overall Accuracy: {accuracy:.2f}%")

    os.makedirs("charts", exist_ok=True)
    plot_loss_chart(losses, 'charts/evaluation_loss.png')


if __name__ == "__main__":
    set_seed(42)
    main()