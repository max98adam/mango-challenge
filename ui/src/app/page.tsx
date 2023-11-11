import ImageGrid from "@/components/ImageGrid";
import { readdirSync } from "fs";
import path from "path";

export const IMAGES_DIR = path.join(
  process.env.ROOT_DIR || process.cwd(),
  "public/images"
);

const getProductImages = async () => {
  "use server";

  const filenames = readdirSync(IMAGES_DIR);
  const productImages: string[] = [];

  filenames.forEach((filename) => {
    if (filename.endsWith(".jpg")) {
      productImages.push(path.join("/", "images", filename));
    }
  });

  return productImages;
};

export default async function Home() {
  const productImages = await getProductImages();

  const getImageId = (imagePath: string) => {
    return imagePath.split("/").shift()?.split(".jpg")[0];
  };

  return (
    <main className="flex h-full flex-col items-center justify-between p-24">
      <div className="z-10 w-full items-center justify-between font-mono text-sm lg:flex flex-col pb-24">
        <h2 className="text-2xl">
          Select a product for to create a matching outfit for
        </h2>
        <ImageGrid images={productImages} showSuffle={true} />
      </div>
    </main>
  );
}
