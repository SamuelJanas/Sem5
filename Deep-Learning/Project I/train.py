import torch
import hydra
import random
import numpy as np
import torch.nn as nn

from tqdm import tqdm
from omegaconf import OmegaConf
from model.HomeBrewRNN import HomeBrewRNN
from data.create_dataloader import create_dataloader

def set_seed(seed: int):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    # use deterministic algorithm
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True)



def train_epoch(model, loader, criterion, optimizer, epoch, cfg):
    model.train()
    train_loss = 0
    progress_bar = tqdm(loader, desc="Training")
    for inputs, labels in progress_bar:
        inputs = inputs.to(cfg.device)
        labels = labels.to(cfg.device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        progress_bar.set_postfix({"loss": loss.item()})
    train_loss /= len(loader)
    # save checkpoint
    checkpoint = {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "epoch": epoch,
        "config": OmegaConf.to_container(cfg),
    }
    torch.save(checkpoint, f"checkpoints/checkpoint.pt") # TODO: add checkpointing to config
    # Print for each epoch
    print(f"Epoch: {epoch}, Training Loss: {train_loss:.4f}")


@torch.no_grad()
def test_epoch(model, loader, criterion, epoch, cfg):
    model.eval()
    test_loss = 0
    progress_bar = tqdm(loader, desc="Testing")
    for inputs, labels in progress_bar:
        inputs = inputs.to(cfg.device)
        labels = labels.to(cfg.device)

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        test_loss += loss.item()
        progress_bar.set_postfix({"loss": loss.item()})
    test_loss /= len(loader)
    print(f"Epoch: {epoch}, Testing Loss: {test_loss:.4f}")


@hydra.main(config_path="config", config_name="train", version_base=None)
def train(cfg: OmegaConf):
    # initialize model
    model = HomeBrewRNN(
        hidden_size=cfg.hidden_size, 
        num_layers=cfg.num_layers, 
        num_classes=cfg.num_classes, 
        dropout=cfg.dropout,
    ).to(cfg.device)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.lr) # use Adam optimizer

    train_loader, test_loader = create_dataloader(cfg.batch_size) 

    # train model
    for epoch in range(1, cfg.epochs + 1):
        train_epoch(
            model=model, 
            loader=train_loader, 
            criterion=criterion, 
            optimizer=optimizer, 
            epoch=epoch, 
            cfg=cfg,
            )
        test_epoch(
            model=model, 
            loader=test_loader, 
            criterion=criterion, 
            epoch=epoch, 
            cfg=cfg,
            )



if __name__ == "__main__":
    set_seed(42)
    train()