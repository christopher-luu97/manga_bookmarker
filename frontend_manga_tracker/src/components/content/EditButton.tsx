// src/components/EditButton.tsx
import React from "react";

export const EditButton: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="hidden md:inline-block p-2 border border-gray-300 rounded bg-[#FAEBEF] text-[#333D79] hover:bg-gradient-to-r hover:from-[#FAEBEF] hover:to-[#FADCE6] cursor-pointer transition ease-in duration-200"
    >
      Edit
    </button>
  );
};
