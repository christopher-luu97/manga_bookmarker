import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import { SearchBar } from "./filters/SearchBar";
import { EditButton } from "./content/EditButton";
import { ResultsGrid } from "./content/ResultsGrid";
import { BookmarksList } from "./status/BookmarksList";
import { Modal } from "./modal/Modal";
import { RefreshButton } from "./content/refreshButton";
import { WebsiteData } from "./data/websiteData";
import { AlphabetFilter } from "./filters/AlphabetFilter";
import { DateFilter } from "./filters/DateFilter";
import { mangaDataInterface } from "./data/mangaData";

export const ApplicationContent: React.FC = () => {
  const [mangaData, setMangaData] = useState<mangaDataInterface[]>([]);
  const [isModalOpen, setModalOpen] = useState(false);
  const [refreshData, setRefreshData] = useState(false);
  const [bookmarksData, setBookmarksData] = useState([]);
  const [supportedWebsitesData, setSupportedWebsitesData] = useState<
    WebsiteData[]
  >([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sortAlphabetOption, setSortAlpabetOption] = useState("none");
  const [sortDateOption, setSortDateOption] = useState("none");

  const handleSortChange = (newSortOption: string) => {
    setSortAlpabetOption(newSortOption);
  };

  const sortedAndFilteredMangaData = useMemo(() => {
    /**
     * Memoized function to sort and filter manga data based on specified options.
     *
     * This function performs combined sorting, grouping by alphabet, and ordering within groups.
     * It first sorts the data alphabetically if the option is selected, then groups by alphabet.
     * After that, it sorts each group by date (newest to oldest) if the date option is selected.
     *
     * @returns {mangaDataInterface[]} - Sorted and filtered manga data.
     */
    const performSortingAndFiltering = () => {
      // Initial sorted data is a copy of the mangaData array
      let sortedData: mangaDataInterface[] = [...mangaData];

      // Sort alphabetically if the option is selected
      if (sortAlphabetOption !== "none") {
        sortedData = [...mangaData].sort((a, b) =>
          sortAlphabetOption === "alphabetical"
            ? a.title.localeCompare(b.title)
            : b.title.localeCompare(a.title)
        );
      }

      // Group data by alphabet and sort within groups based on date if the date option is selected
      if (sortDateOption !== "none") {
        const groupedData: mangaDataInterface[][] = sortedData.reduce(
          (acc: mangaDataInterface[][], manga) => {
            const lastGroup = acc[acc.length - 1];

            if (
              !lastGroup ||
              (sortAlphabetOption === "alphabetical" &&
                manga.title.charAt(0).toLowerCase() !==
                  lastGroup[lastGroup.length - 1].title
                    .charAt(0)
                    .toLowerCase()) ||
              (sortAlphabetOption === "reverse-alphabetical" &&
                manga.title.charAt(0).toLowerCase() !==
                  lastGroup[lastGroup.length - 1].title.charAt(0).toLowerCase())
            ) {
              // If it's a new group, create a new group with the current manga
              acc.push([manga]);
            } else {
              // If it's the same group, add the manga to the existing group
              lastGroup.push(manga);
            }

            return acc;
          },
          []
        );

        // Sort each group based on date and flatten the array
        sortedData = groupedData
          .map((group) =>
            group.sort((a, b) => {
              const dateA = new Date(a.lastUpdated).getTime();
              const dateB = new Date(b.lastUpdated).getTime();

              return sortDateOption === "newest-date"
                ? dateB - dateA
                : dateA - dateB;
            })
          )
          .flat();
      }

      // Filter the sorted data based on the search term
      return sortedData.filter((manga) =>
        manga.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
    };

    // Execute the sorting and filtering function, and memoize the result
    return performSortingAndFiltering();
  }, [mangaData, searchTerm, sortAlphabetOption, sortDateOption]);

  const handleDateChange = (newSortOption: string) => {
    setSortDateOption(newSortOption);
  };

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

  // Add use effect to poll backend API for data from database
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://192.168.8.167:8000/get_data"); //"http://192.168.8.167:8000/get_data"
        setMangaData(response.data);

        const bookmarksResponse = await axios.get(
          "http://192.168.8.167:8000/get_bookmarks_data" //"http://192.168.8.167:8000/get_bookmarks_data"
        );
        setBookmarksData(bookmarksResponse.data);

        const supportedWebsiteResponse = await axios.get(
          "http://192.168.8.167:8000/get_supported_websites" //"http://192.168.8.167:8000/get_supported_websites"
        );
        setSupportedWebsitesData(supportedWebsiteResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [refreshData]);

  const handleRefreshClick = async () => {
    setIsLoading(true); // Start loading
    try {
      await axios.get("http://192.168.8.167:8000/refresh_data");
      setRefreshData(!refreshData);
    } catch (error) {
      console.error("Error refreshing data:", error);
    }
    setIsLoading(false); // Stop loading
  };

  return (
    <div className="ApplicationContent p-4 bg-[#333D79]">
      {/* Top row for filters and search */}
      <div className="flex flex-wrap gap-4 mb-4">
        {/* TODO Genre, Type, Order Filters */}

        {/* <GenreFilter />
          <TypeFilter />
          <OrderFilter /> */}
        <SearchBar
          searchTerm={searchTerm}
          onSearchChange={handleSearchChange}
          disabled={isLoading}
        />
        <EditButton onClick={handleEditButtonClick} disabled={isLoading} />
        {isModalOpen && (
          <Modal
            mangaData={mangaData}
            onUpdate={handleUpdateData}
            onClose={handleCloseModal}
            supportedWebsitesData={supportedWebsitesData.map(
              (website) => website.link
            )} // Assuming each website object has a `link` property
          />
        )}
        <AlphabetFilter onSortChange={handleSortChange} disabled={isLoading} />
        <DateFilter onSortChange={handleDateChange} disabled={isLoading} />
        <RefreshButton onClick={handleRefreshClick} disabled={isLoading} />
      </div>

      <div className="flex flex-col md:flex-row gap-4 md:gap-8">
        <div
          className={`flex-grow md:w-2/3 relative ${
            isLoading ? "pointer-events-none" : ""
          }`}
        >
          {/* Conditional rendering of the loading overlay */}
          {isLoading && (
            <div className="absolute top-0 left-0 right-0 bottom-0 bg-gray-200 bg-opacity-75 flex justify-center items-center z-10 border rounded-md">
              <svg
                aria-hidden="true"
                className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                viewBox="0 0 100 101"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                  fill="currentColor"
                />
                <path
                  d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                  fill="currentFill"
                />
              </svg>
              <span className="sr-only">Loading...</span>
            </div>
          )}
          <div className={`${isLoading ? "blur-sm" : ""}`}>
            <ResultsGrid mangaData={sortedAndFilteredMangaData} />
          </div>
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
