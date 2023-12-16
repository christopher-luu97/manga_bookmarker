// src/components/ResultsGrid.tsx
import React from "react";
import { mangaData } from "../data/mangaData";

export const ResultsGrid: React.FC = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4 p-4 border border-gray-200 shadow-lg rounded-lg overflow-hidden">
      {mangaData.map((manga) => (
        <div
          key={manga.id}
          className="border border-gray-200 shadow-sm rounded-lg overflow-hidden"
        >
          <a href={manga.link} className="block">
            <div className="w-full h-64 overflow-hidden">
              <img
                src={manga.imageUrl}
                alt={manga.title}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="text-center p-2">
              <p>{manga.title}</p>
              <p>{manga.chapter}</p>
              <p>{manga.lastUpdated}</p>
            </div>
          </a>
        </div>
      ))}
    </div>
  );
};
