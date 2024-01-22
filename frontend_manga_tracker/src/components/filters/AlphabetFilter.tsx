import React from "react";

interface AlphabetFilterProps {
  onSortChange: (sortOption: string) => void;
  disabled?: boolean;
}

export const AlphabetFilter: React.FC<AlphabetFilterProps> = ({
  onSortChange,
  disabled,
}) => {
  return (
    <select
      className="p-2 border border-gray-300 rounded bg-[#FAEBEF] text-[#333D79] font-semibold"
      onChange={(e) => onSortChange(e.target.value)}
      defaultValue="placeholder"
      disabled={disabled}
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
