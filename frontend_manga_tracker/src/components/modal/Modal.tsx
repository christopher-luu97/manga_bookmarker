import React, { useState, useEffect, useRef } from "react";
import { getStatusColor } from "../status/statusColour";
import {
  capitalizeFirstLetterOfEachWord,
  getBaseUrl,
  isSupportedWebsite,
} from "../util/util";
import axios from "axios";

export const Modal: React.FC<{
  mangaData: any[];
  onUpdate: (data: any[]) => void;
  onClose: () => void;
  supportedWebsitesData: string[]; // Add supported websites as a prop
}> = ({ mangaData, onUpdate, onClose, supportedWebsitesData }) => {
  const [draftData, setDraftData] = useState([...mangaData]);
  const [newLink, setNewLink] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const lastTableRowRef = useRef<HTMLTableRowElement>(null);
  const [isNewRecordAdded, setIsNewRecordAdded] = useState(false); // state to track addition of new record

  useEffect(() => {
    setDraftData([...mangaData]); // Update the local state when mangaData prop changes
  }, [mangaData]);

  useEffect(() => {
    if (isNewRecordAdded && lastTableRowRef.current) {
      lastTableRowRef.current.scrollIntoView({ behavior: "smooth" });
      setIsNewRecordAdded(false); // Reset the flag after scrolling
    }
  }, [draftData, isNewRecordAdded]);

  const handleConfirm = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:8000/", {
        manga_records: draftData,
      });
      if (response.data) {
        setSuccessMessage(response.data.db_upload_status);
        onUpdate(draftData);
      }
    } catch (error) {
      console.error("Error confirming changes:", error);
      setSuccessMessage("Failed to confirm changes");
    }
    setIsLoading(false); // Set loading to false
    setTimeout(() => setSuccessMessage(""), 3000);
  };

  const handleAdd = () => {
    // Create new data for new records that match the format the backend is expecting
    // There are various placeholders besides newLink
    if (!isSupportedWebsite(newLink, supportedWebsitesData)) {
      alert(
        `The website ${newLink} is not supported. \nSee supported websites on the right pane of the home page`
      ); // Notify the user
      return; // Do not proceed with adding the new data
    }
    const newData = {
      chapter_number: 0, // Placeholder
      id: `new_${Date.now()}`,
      imageUrl: "",
      lastUpdated: new Date().toISOString(),
      link: newLink,
      status: "Good", // Placeholder
      title: "New Manga", // Placeholder
    };
    setDraftData([...draftData, newData]);
    setIsNewRecordAdded(true); // Set flag to true when new record is added
  };

  const handleDelete = (id: string) => {
    setDraftData(
      draftData.map((item) =>
        item.id === id ? { ...item, status: "Delete" } : item
      )
    );
  };

  const handleDiscard = () => {
    setDraftData([...mangaData]);
    setSuccessMessage("Changes discarded!");
    setTimeout(() => setSuccessMessage(""), 3000); // Clear message after 3 seconds
    console.log(draftData);
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 backdrop-blur-sm">
      <div
        className="relative top-20 mx-auto p-5 border shadow-lg rounded-md bg-[#333D79] z-50"
        style={{ width: "80%" }}
      >
        <button
          onClick={onClose}
          className="absolute top-2 right-3 text-xl text-[#FAEBEF] hover:text-[#FAEBEF]"
        >
          &times;
        </button>
        <h3 className="text-lg font-semibold mb-4 text-[#FAEBEF] ">
          Edit Manga List
        </h3>
        <div className="my-4 border p-2 rounded-lg shadow bg-[#FAEBEF]">
          {isLoading && (
            <div className="absolute top-0 left-0 right-0 bottom-0 bg-gray-200 bg-opacity-75 flex justify-center items-center">
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
          <input
            type="text"
            value={newLink}
            onChange={(e) => setNewLink(e.target.value)}
            className="border p-1 mr-2 rounded"
            placeholder="Enter new manga link"
          />
          <button
            onClick={handleAdd}
            className="bg-[#333D79] text-white px-2 py-1 rounded hover:bg-[#195190]"
          >
            Add
          </button>
        </div>
        <div className="max-h-96 overflow-y-auto">
          {" "}
          <table className="min-w-full text-left border-collapse border border-gray-300">
            <thead>
              <tr className="bg-gray-100">
                <th className="border px-4 py-2">Title</th>
                <th className="border px-4 py-2">Latest Chapter Link</th>
                <th className="border px-4 py-2">Status</th>
                <th className="border px-4 py-2">Delete</th>
              </tr>
            </thead>
            <tbody className="bg-[#FAEBEF]">
              {draftData
                .filter((item) => item.status !== "Delete")
                .map((manga, index) => (
                  <tr
                    key={manga.id}
                    ref={
                      index === draftData.length - 1 ? lastTableRowRef : null
                    }
                  >
                    <td className="border px-4 py-2 max-w-xs overflow-auto whitespace-nowrap text-[#333D79] font-semibold">
                      {capitalizeFirstLetterOfEachWord(manga.title)}
                    </td>
                    <td className="border px-4 py-2 max-w-xs overflow-auto whitespace-nowrap">
                      <a
                        href={manga.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                        style={{ maxWidth: "50ch" }}
                      >
                        {manga.link}
                      </a>
                    </td>
                    <td className="border px-4 py-2 text-center">
                      <span
                        className={`inline-block h-4 w-4 rounded-full mr-2 ${getStatusColor(
                          manga.status
                        )}`}
                        title={manga.status}
                      ></span>
                    </td>
                    <td className="border px-4 py-2">
                      <button
                        onClick={() => handleDelete(manga.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
        <div className="flex justify-between mt-4">
          <button
            onClick={handleConfirm}
            className="px-4 py-2 bg-[#1a7a4c] text-white rounded hover:bg-green-600"
          >
            Confirm changes
          </button>
          <button
            onClick={handleDiscard}
            className="px-4 py-2 bg-[#990011] text-white rounded hover:bg-red-600"
          >
            Discard Changes
          </button>
        </div>
        {successMessage && (
          <div className="text-white mt-3">{successMessage}</div>
        )}
      </div>
    </div>
  );
};
