// src/components/TypeFilter.tsx
import React from "react";

export const TypeFilter: React.FC = () => {
  return (
    <select className="p-2 border border-gray-300 rounded">
      <option value="">Select Type</option>
      <option value="manga">Manga</option>
      <option value="manhua">Manhua</option>
      <option value="light-novel">Light Novel</option>
      {/* ... more types */}
    </select>
  );
};
