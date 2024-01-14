import React, { useState, useEffect, useMemo } from "react";
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
  const [refreshData, setRefreshData] = useState(false);
  const [bookmarksData, setBookmarksData] = useState([]);
  const [supportedWebsitesData, setSupportedWebsitesData] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const handleEditButtonClick = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  const handleUpdateData = (newData: any[]) => {
    setMangaData(newData);
    setRefreshData(!refreshData); // Toggle the state to trigger re-fetch after modal edits
  };

  const handleSearchChange = (newSearchTerm: string) => {
    setSearchTerm(newSearchTerm);
  };

  const filteredMangaData = useMemo(() => {
    return mangaData.filter((manga) =>
      manga.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [mangaData, searchTerm]);

  // Add use effect to poll backend API for data from database
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/get_data");
        setMangaData(response.data);

        const bookmarksResponse = await axios.get(
          "http://127.0.0.1:8000/get_bookmarks_data"
        );
        setBookmarksData(bookmarksResponse.data);

        const supportedWebsiteResponse = await axios.get(
          "http://127.0.0.1:8000/get_supported_websites"
        );
        setSupportedWebsitesData(supportedWebsiteResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [refreshData]);

  return (
    <div className="ApplicationContent p-4">
      {/* Top row for filters and search */}
      <div className="flex flex-wrap gap-4 mb-4">
        {/* TODO Genre, Type, Order Filters */}

        {/* <GenreFilter />
        <TypeFilter />
        <OrderFilter /> */}
        <SearchBar
          searchTerm={searchTerm}
          onSearchChange={handleSearchChange}
        />
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
          <ResultsGrid mangaData={filteredMangaData} />
        </div>

        <div className="md:w-1/3">
          <BookmarksList
            bookmarksData={bookmarksData}
            supportedWebsitesData={supportedWebsitesData}
          />
        </div>
      </div>
    </div>
  );
};
