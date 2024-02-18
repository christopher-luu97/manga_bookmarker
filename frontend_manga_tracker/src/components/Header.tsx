import React from "react";

interface HeaderProps {
  isAuthenticated?: boolean;
  onLogout?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  isAuthenticated,
  onLogout,
}) => {
  return (
    <header className="font-sans bg-[#333D79] text-white text-xl p-4 border-b-4 border-[#FAEBEF]">
      <h1 className="text-[#FAEBEF]">Manga Tracker</h1>
      {isAuthenticated && (
        <button
          onClick={() => onLogout && onLogout()}
          className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          style={{ float: "right", marginTop: "-40px" }}
        >
          Logout
        </button>
      )}
    </header>
  );
};
