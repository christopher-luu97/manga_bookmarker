// src/components/SearchBar.tsx
import React from "react";

export const SearchBar: React.FC = () => {
  return (
    <input
      type="text"
      placeholder="Search..."
      className="p-2 border border-gray-300 rounded w-full md:w-auto"
    />
  );
};
