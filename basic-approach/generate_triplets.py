import pandas as pd
import random


def generate_triplets(outfit_ds_path: str):
    outfits = pd.read_csv(outfit_ds_path)
    triplets = []

    # Group by outfit
    grouped = outfits.groupby('cod_outfit')

    for outfit, group in grouped:
        # List of items in the current outfit
        items_in_outfit = group['cod_modelo_color'].tolist()

        # All other items not in the current outfit
        other_items = outfits[outfits['cod_outfit'] != outfit]['cod_modelo_color'].tolist()

        # Generate triplets
        for anchor in items_in_outfit:
            positive = random.choice([item for item in items_in_outfit if item != anchor])
            negative = random.choice(other_items)
            triplets.append((anchor, positive, negative))

    return triplets

# anchor1, pos1, negative1, anchor2, pos2, negative2, ...
def triplets_to_img_paths(product_data_path: str, triplets):
    product_data = pd.read_csv(product_data_path)
    image_paths = []
    for triplet in triplets:
        for i in range(3):
            image_paths.append(product_data[product_data['cod_modelo_color'] == triplet[i]]['des_filename'].iloc[0])

    image_paths = [p.split('/')[-1] for p in image_paths]
    return image_paths