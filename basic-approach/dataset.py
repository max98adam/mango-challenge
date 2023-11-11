import os
import cv2
import torch
from torch.utils.data import Dataset


class CustomDataset(Dataset):
    def __init__(self, image_dir, item_filenames, transform=None):
        self.image_dir = image_dir
        self.item_filenames = item_filenames
        self.transform = transform

    def __len__(self):
        return len(self.item_filenames)-3

    def _process_img(self, idx):
        img_name = os.path.join(self.image_dir, self.item_filenames[idx])

        image = cv2.imread(img_name)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            transformed = self.transform(image=image)
            image = transformed["image"].float()
        else:
            image = torch.from_numpy(image).float()

        return image

    def __getitem__(self, idx):
        # TODO replace this triplet creation logic by something that makes sense
        anchor = self._process_img(idx)
        positive = self._process_img(idx + 1)
        negative = self._process_img(idx + 2)
        triplet = torch.stack([anchor, positive, negative], dim=0)
        return triplet
