import ImageGrid from "@/components/ImageGrid";
import { readFileSync, readdirSync } from "fs";
import Image from "next/image";
import path from "path";

export const IMAGES_DIR = path.join(
  process.env.ROOT_DIR || process.cwd(),
  "public/images"
);

const getOutfitImages = async (ids: string[]) => {
  "use server";

  const filenames = readdirSync(IMAGES_DIR);
  const productImages: string[] = [];

  const outfitFilenames = filenames.filter((f) =>
    ids.some((id) => f.includes(id.split("-")[0]))
  );

  outfitFilenames.forEach((filename) => {
    if (filename.endsWith(".jpg")) {
      productImages.push(path.join("/", "images", filename));
    }
  });

  return productImages;
};

const getProductImage = async (id: string) => {
  "use server";

  return path.join("/", "images", `${id}.jpg`);
};

export default async function ProductPage({
  params,
}: {
  params: { id: string };
}) {
  const { id } = params;

  const sanitizedIdForApi = id.slice(5).replace("_", "-");
  const productImagePath = await getProductImage(id);

  const apiResponse = await fetch(
    `http://localhost:8000/product/${sanitizedIdForApi}`
  );
  const relatedProducts = await apiResponse.json();

  const outfitImages = await getOutfitImages(
    relatedProducts["related_products"]
  );

  const getImageId = (imagePath: string) => {
    return imagePath.split("/").shift()?.split(".jpg")[0];
  };

  return (
    <main className="flex h-full flex-col items-center justify-between p-24">
      <div className="z-10 w-full items-center justify-between font-mono text-sm lg:flex flex-col pb-24">
        <div className="grid grid-cols-12 w-full">
          <h2 className="text-2xl col-span-4">Selected item</h2>
          <h2 className="text-2xl col-span-8">
            The proposed outfit for the chosen product would be
          </h2>
        </div>

        <div className="grid grid-cols-12 w-full">
          <div className="flex flex-col col-span-4">
            <Image
              className="w-52 h-58"
              src={productImagePath}
              alt={`Product ${id}`}
              width={800}
              height={1000}
            />
          </div>

          <div className="col-span-8 flex flex-wrap">
            <ImageGrid images={outfitImages} />
          </div>
        </div>
      </div>
    </main>
  );
}
