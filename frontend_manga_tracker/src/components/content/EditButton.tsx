// src/components/EditButton.tsx
import React from "react";

export const EditButton: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="hidden md:inline-block p-2 border border-gray-300 rounded bg-blue-500 text-white"
    >
      Edit
    </button>
  );
};
