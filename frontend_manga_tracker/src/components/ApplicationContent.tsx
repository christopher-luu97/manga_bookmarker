import React, { useState, useEffect } from "react";
import axios from "axios";
import { SearchBar } from "./filters/SearchBar";
import { EditButton } from "./content/EditButton";
import { ResultsGrid } from "./content/ResultsGrid";
import { BookmarksList } from "./status/BookmarksList";
import { Modal } from "./modal/Modal";
import { mangaPathData as initialMangaData } from "./data/mangaPathData";

export const ApplicationContent: React.FC = () => {
  const [mangaData, setMangaData] = useState(initialMangaData);
  const [isModalOpen, setModalOpen] = useState(false);

  const handleEditButtonClick = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleUpdateData = (newData: any[]) => {
    setMangaData(newData);
  };

  // Add use effect to poll backend API for data from database
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/get_data");
        setMangaData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
        // Optionally handle the error (e.g., show an error message)
      }
    };

    fetchData();
  }, []);

  return (
    <div className="p-4">
      {/* Top row for filters and search */}
      <div className="flex flex-wrap gap-4 mb-4">
        {/* TODO Genre, Type, Order Filters */}

        {/* <GenreFilter />
        <TypeFilter />
        <OrderFilter /> */}
        <SearchBar />
        <EditButton onClick={handleEditButtonClick} />
        {isModalOpen && (
          <Modal
            mangaData={mangaData}
            onUpdate={handleUpdateData}
            onClose={handleCloseModal}
          />
        )}
      </div>

      <div className="flex flex-col md:flex-row gap-4 md:gap-8">
        <div className="flex-grow md:w-2/3">
          <ResultsGrid mangaData={mangaData} />
        </div>

        <div className="md:w-1/3">
          <BookmarksList />
        </div>
      </div>
    </div>
  );
};
