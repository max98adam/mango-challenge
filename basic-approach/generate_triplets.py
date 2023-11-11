import pandas as pd
import random


def generate_triplets(outfit_ds_path: str, DEBUG_USE_SMALL_DATASET_FRACTION):
    outfits = pd.read_csv(outfit_ds_path)
    triplets = []

    # Group by outfit
    grouped = outfits.groupby('cod_outfit')

    i = 0
    for outfit, group in grouped:
        i += 1

        if DEBUG_USE_SMALL_DATASET_FRACTION and i > len(grouped) * 0.01:
            break

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


def triplets_to_img_filenames(product_data_path: str, triplets):
    product_data = pd.read_csv(product_data_path)
    triplet_filenames = []
    for triplet in triplets:
        triplet_filenames.append({
            "anchor": product_data[product_data['cod_modelo_color'] == triplet[0]]['des_filename'].iloc[0].split('/')[
                -1],
            "positive": product_data[product_data['cod_modelo_color'] == triplet[1]]['des_filename'].iloc[0].split('/')[
                -1],
            "negative": product_data[product_data['cod_modelo_color'] == triplet[2]]['des_filename'].iloc[0].split('/')[
                -1]
        })
    return triplet_filenames
