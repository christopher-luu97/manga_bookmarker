import React from "react";

interface AlphabetFilterProps {
  onSortChange: (sortOption: string) => void;
}

export const AlphabetFilter: React.FC<AlphabetFilterProps> = ({
  onSortChange,
}) => {
  return (
    <select
      className="p-2 border border-gray-300 rounded bg-[#FAEBEF] text-[#333D79] font-semibold"
      onChange={(e) => onSortChange(e.target.value)}
      defaultValue="placeholder"
    >
      <option value="placeholder" disabled>
        Sort Alphabetically
      </option>{" "}
      <option value="none">None</option>
      <option value="alphabetical">A-Z</option>
      <option value="reverse-alphabetical">Z-A</option>
    </select>
  );
};
