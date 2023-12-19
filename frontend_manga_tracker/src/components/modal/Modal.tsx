import React, { useRef } from "react";
import { mangaData } from "../data/mangaData";

export const Modal: React.FC<{
  onClose: () => void;
  onSelect: (id: number) => void;
}> = ({ onClose, onSelect }) => {
  const modalRef = useRef<HTMLDivElement>(null);

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 backdrop-blur-sm">
      <div
        ref={modalRef}
        className="relative top-20 mx-auto p-5 border w-1/3 shadow-lg rounded-md bg-white z-50"
      >
        <h3 className="text-lg font-semibold mb-4">Edit Manga List</h3>
        <ul className="max-h-64 overflow-auto">
          {mangaData.map((manga) => (
            <li
              key={manga.id}
              className="mb-2 cursor-pointer hover:bg-blue-100"
              onClick={() => onSelect(manga.id)}
            >
              {manga.title}
            </li>
          ))}
        </ul>
        <button
          onClick={onClose}
          className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Close
        </button>
      </div>
    </div>
  );
};
