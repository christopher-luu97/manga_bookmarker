// src/components/ResultsGrid.tsx
import React, { useState } from "react";
// import { mangaData } from "../data/mangaData";

export const ResultsGrid: React.FC<{ mangaData: any[] }> = ({ mangaData }) => {
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

  if (mangaData.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-4 min-h-screen">
        <p className="text-lg md:text-xl font-semibold mb-3">
          No data in the database!
        </p>
        <p className="text-md md:text-lg mb-2">
          Add records by clicking the Edit button on the computer.
        </p>
        <div className="hidden md:block">
          <p className="text-sm text-gray-600 italic">
            (The Edit button is not available on mobile devices)
          </p>
        </div>
      </div>
    );
  }

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
