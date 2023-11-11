import os
import cv2
import torch
from torch.utils.data import Dataset


class TripletDataset(Dataset):
    def __init__(self, image_dir, triplet_filenames, transform=None):
        self.image_dir = image_dir
        self.triplet_filenames = triplet_filenames
        self.transform = transform

    def __len__(self):
        return len(self.triplet_filenames)

    def _process_img(self, image_path):
        img_name = os.path.join(self.image_dir, image_path)

        image = cv2.imread(img_name)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            transformed = self.transform(image=image)
            image = transformed["image"].float()
        else:
            image = torch.from_numpy(image).float()

        return image

    def __getitem__(self, idx):
        triplet = self.triplet_filenames[idx]

        anchor = self._process_img(triplet["anchor"])
        positive = self._process_img(triplet["positive"])
        negative = self._process_img(triplet["negative"])
        triplet = torch.stack([anchor, positive, negative], dim=0)
        return triplet
