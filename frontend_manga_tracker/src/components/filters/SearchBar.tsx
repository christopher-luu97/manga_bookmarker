import React from "react";

interface SearchBarProps {
  searchTerm: string;
  onSearchChange: (newSearchTerm: string) => void;
  disabled?: boolean; // Optional disabled prop
}

export const SearchBar: React.FC<SearchBarProps> = ({
  searchTerm,
  onSearchChange,
  disabled,
}) => {
  return (
    <input
      type="text"
      value={searchTerm}
      onChange={(e) => onSearchChange(e.target.value)}
      disabled={disabled}
      placeholder="Search..."
      className="p-2 border border-gray-300 rounded w-full md:w-auto"
    />
  );
};
