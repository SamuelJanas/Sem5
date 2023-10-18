
import torch

from model.HomeBrewRNN import HomeBrewRNN


if __name__ == "__main__":
    checkpoint = torch.load("checkpoints/checkpoint.pt")
    print(checkpoint.keys())
    model = HomeBrewRNN()
    model.load_state_dict(checkpoint["model"])
    epoch = checkpoint["epoch"]