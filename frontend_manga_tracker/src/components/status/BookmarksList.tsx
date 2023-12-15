// src/components/BookmarksList.tsx
import React from "react";
import { mangaData } from "../data/mangaData";

export const BookmarksList: React.FC = () => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "Good":
        return "bg-green-500";
      case "Down":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  return (
    <ul className="border border-gray-200 shadow-lg rounded-lg p-4">
      {mangaData.map((manga) => (
        <li key={manga.id} className="flex items-center mb-2">
          <span
            className={`inline-block h-4 w-4 rounded-full mr-2 ${getStatusColor(
              manga.status
            )}`}
          ></span>
          <a href={manga.link} className="text-blue-600 hover:text-blue-800">
            {manga.title}
          </a>
        </li>
      ))}
    </ul>
  );
};
