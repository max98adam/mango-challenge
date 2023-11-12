import os
import cv2
import pandas as pd
import torch
from torch.utils.data import Dataset


class TripletDataset(Dataset):
    def __init__(self, image_dir, product_csv_file, triplet_filenames, transform=None):
        self.image_dir = image_dir
        self.product_metadata = pd.read_csv(product_csv_file)
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
        triplet_filenames = self.triplet_filenames[idx]

        anchor = self._process_img(triplet_filenames["anchor"])
        positive = self._process_img(triplet_filenames["positive"])
        negative = self._process_img(triplet_filenames["negative"])
        triplet = torch.stack([anchor, positive, negative], dim=0)

        anchor_metadata = self.product_metadata[
            self.product_metadata["des_filename"] == os.path.join("datathon", self.image_dir.replace("../", ""),
                                                                  triplet_filenames["anchor"])].to_dict()
        positive_metadata = self.product_metadata[
            self.product_metadata["des_filename"] == os.path.join("datathon", self.image_dir.replace("../", ""),
                                                                  triplet_filenames["positive"])].to_dict()
        negative_metadata = self.product_metadata[
            self.product_metadata["des_filename"] == os.path.join("datathon", self.image_dir.replace("../", ""),
                                                                  triplet_filenames["negative"])].to_dict()



        return {"img": triplet, "metadata": [
            anchor_metadata,
            positive_metadata,
            negative_metadata
        ]}
