// src/components/GenreFilter.tsx
import React from "react";

export const GenreFilter: React.FC = () => {
  return (
    <select className="p-2 border border-gray-300 rounded">
      <option value="">Select Genre</option>
      <option value="action">Action</option>
      <option value="adventure">Adventure</option>
      {/* ... more genres */}
    </select>
  );
};
