// src/components/OrderFilter.tsx
import React from "react";

export const OrderFilter: React.FC = () => {
  return (
    <select className="p-2 border border-gray-300 rounded">
      <option value="alphabetical">Alphabetical</option>
      <option value="date-added">Date Added</option>
      <option value="last-updated">Last Updated</option>
    </select>
  );
};
