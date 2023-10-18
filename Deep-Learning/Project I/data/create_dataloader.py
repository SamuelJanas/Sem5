import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

from data.generate_data import generate_data


class SequenceDataset(Dataset):
    def __init__(self, data, labels):
        self.data = [torch.FloatTensor(d).permute(1, 0) for d in data]  # Swap the 1st and 2nd dimensions
        self.labels = [torch.FloatTensor(l) for l in labels]
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]
    
def create_dataloader(batch_size=32) -> (DataLoader, DataLoader):
    x_train, y_train, x_test, y_test = generate_data(50_000)
    # add padding to the sequences
    x_train = [np.vstack([x, np.zeros((60-x.shape[0], 3))]) for x in x_train]
    x_test = [np.vstack([x, np.zeros((60-x.shape[0], 3))]) for x in x_test]


    train_dataset = SequenceDataset(x_train, y_train)
    test_dataset = SequenceDataset(x_test, y_test)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_dataloader, test_dataloader