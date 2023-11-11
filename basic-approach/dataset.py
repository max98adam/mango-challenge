import os
import cv2
import torch
from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self, image_dir, dataset_dir, item_filenames, transform=None):
        self.image_dir = image_dir
        self.dataset_dir = dataset_dir
        self.item_filenames = item_filenames
        self.transform = transform

    def __len__(self):
        return len(self.item_filenames)

    def __getitem__(self, idx):
        import os
        img_name = os.path.join(self.image_dir, self.item_filenames[idx])

        image = cv2.imread(img_name)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            transformed = self.transform(image=image)
            image = transformed["image"].float()
        else:
            image = torch.from_numpy(image).float()

        return image