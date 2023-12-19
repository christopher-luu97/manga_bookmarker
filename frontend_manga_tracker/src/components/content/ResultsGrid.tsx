// src/components/ResultsGrid.tsx
import React, { useState } from "react";
import { mangaData } from "../data/mangaData";

export const ResultsGrid: React.FC = () => {
  const itemsPerRow = 5; // Adjust based on your grid setup
  const initialRows = 2;
  const initialItemCount = itemsPerRow * initialRows;
  const [visibleItems, setVisibleItems] = useState(initialItemCount);

  const showMore = () => {
    setVisibleItems(
      (prevVisibleItems) => prevVisibleItems + itemsPerRow * initialRows
    );
  };

  const showLess = () => {
    setVisibleItems(initialItemCount);
  };

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4 border border-gray-200 shadow-lg rounded-lg overflow-hidden">
        {mangaData.slice(0, visibleItems).map((manga) => (
          <div
            key={manga.id}
            className="border border-gray-200 shadow-sm rounded-lg overflow-hidden transform transition duration-300 ease-in-out hover:scale-105"
          >
            <a
              href={manga.link}
              target="_blank"
              rel="noopener noreferrer"
              className="block"
            >
              <div className="w-full h-64 overflow-hidden">
                <img
                  src={manga.imageUrl}
                  alt={manga.title}
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="text-center p-2">
                <p className="transition duration-300 ease-in-out hover:text-blue-500">
                  {manga.title}
                </p>
                <p>{manga.chapter}</p>
                <p>{manga.lastUpdated}</p>
              </div>
            </a>
          </div>
        ))}
      </div>
      <div className="flex justify-center space-x-4 mt-4">
        {visibleItems < mangaData.length && (
          <button
            onClick={showMore}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Show More
          </button>
        )}
        {visibleItems > initialItemCount && (
          <button
            onClick={showLess}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Show Less
          </button>
        )}
      </div>
    </>
  );
};
