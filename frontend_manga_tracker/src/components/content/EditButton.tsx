import React from "react";

interface EditButtonProps {
  onClick: () => void;
  disabled?: boolean; // Optional disabled prop
}

export const EditButton: React.FC<EditButtonProps> = ({
  onClick,
  disabled,
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled} // Use the disabled prop
      className={`hidden md:inline-block p-2 border border-gray-300 rounded bg-[#FAEBEF] text-[#333D79] hover:bg-gradient-to-r hover:from-[#FAEBEF] hover:to-[#FADCE6] cursor-pointer transition ease-in duration-200 ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`} // Apply additional styles when disabled
    >
      Edit
    </button>
  );
};
