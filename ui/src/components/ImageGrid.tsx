"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

type Props = {
  images: string[];
  showSuffle?: boolean;
};

const ImageGrid: React.FC<Props> = ({ images, showSuffle }) => {
  const [imagesToShow, setImagesToShow] = useState(images.slice(0, 200));

  const shuffleImages = () => {
    const tmp = images;
    for (let i = tmp.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [tmp[i], tmp[j]] = [tmp[j], tmp[i]];
    }
    setImagesToShow(tmp.slice(0, 200));
  };

  const getImageId = (imagePath: string) => {
    return imagePath.split("/")[2].split(".jpg")[0];
  };

  return (
    <div className="flex flex-wrap gap-2 justify-center">
      {showSuffle && (
        <button
          className="px-2 py-1 bg-slate-600 text-white absolute top-20 right-100 text-2xl rounded"
          onClick={shuffleImages}
        >
          Shuffle
        </button>
      )}
      {imagesToShow.map((image) => (
        <Link href={`/product/${getImageId(image)}`} key={image}>
          <Image
            className="w-40 h-40 cursor-pointer hover:scale-[1.05]"
            src={image}
            height={400}
            width={400}
            alt={`Product Image ${getImageId(image)}`}
          />
        </Link>
      ))}
    </div>
  );
};

export default ImageGrid;
