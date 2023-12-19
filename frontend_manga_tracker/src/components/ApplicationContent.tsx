import React, { useState } from "react";
import { GenreFilter } from "./filters/GenreFilter";
import { TypeFilter } from "./filters/TypeFilter";
import { OrderFilter } from "./filters/OrderFilter";
import { SearchBar } from "./filters/SearchBar";
import { EditButton } from "./content/EditButton";
import { ResultsGrid } from "./content/ResultsGrid";
import { BookmarksList } from "./status/BookmarksList";
import { Modal } from "./modal/Modal";

export const ApplicationContent: React.FC = () => {
  const [isModalOpen, setModalOpen] = useState(false);

  const handleEditButtonClick = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleSelectItem = (id: number) => {
    // Logic to handle item selection for edit
    console.log("Selected item with id:", id);
    // You can add or delete the item from the list here
  };
  return (
    <div className="p-4">
      {/* Top row for filters and search */}
      <div className="flex flex-wrap gap-4 mb-4">
        <GenreFilter />
        <TypeFilter />
        <OrderFilter />
        <SearchBar />
        <EditButton onClick={handleEditButtonClick} />
        {isModalOpen && (
          <Modal onClose={handleCloseModal} onSelect={handleSelectItem} />
        )}
      </div>

      {/* Main content area */}
      <div className="flex flex-col md:flex-row gap-4 md:gap-8">
        {/* Results Grid */}
        <div className="flex-grow md:w-2/3">
          <ResultsGrid />
        </div>

        {/* Bookmarked websites list */}
        <div className="md:w-1/3">
          <BookmarksList />
        </div>
      </div>
    </div>
  );
};
