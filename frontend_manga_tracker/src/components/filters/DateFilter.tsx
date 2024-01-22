import React from "react";

interface DateFilterProps {
  onSortChange: (sortOption: string) => void;
  disabled?: boolean;
}

export const DateFilter: React.FC<DateFilterProps> = ({
  onSortChange,
  disabled,
}) => {
  return (
    <select
      className="p-2 border border-gray-300 rounded bg-[#FAEBEF] text-[#333D79] font-semibold"
      onChange={(e) => onSortChange(e.target.value)}
      defaultValue="placeholder-date"
      disabled={disabled}
    >
      <option value="placeholder-date" disabled>
        Sort Date
      </option>
      <option value="none">None</option>
      <option value="newest-date">Newest</option>
      <option value="oldest-date">Oldest</option>
    </select>
  );
};
