import os
import cv2
import torch
from torch.utils.data import Dataset


class ItemDataset(Dataset):
    def __init__(self, image_dir, transform=None, DEBUG_USE_SMALL_DATASET_FRACTION=False):
        self.image_dir = image_dir
        self.item_filenames = sorted(os.listdir(image_dir))
        self.transform = transform

        if DEBUG_USE_SMALL_DATASET_FRACTION:
            self.item_filenames = self.item_filenames[0:int(len(self.item_filenames) * 0.01)]

    def __len__(self):
        return len(self.item_filenames)

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
        return self._process_img(self.item_filenames[idx])

    def get_filename(self, idx):
        return self.item_filenames[idx]
