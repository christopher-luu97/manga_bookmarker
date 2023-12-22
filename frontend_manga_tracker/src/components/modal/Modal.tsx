import React, { useState } from "react";
import { getStatusColor } from "../status/statusColour";

export const Modal: React.FC<{
  mangaData: any[];
  onUpdate: (data: any[]) => void;
  onClose: () => void;
}> = ({ mangaData, onUpdate, onClose }) => {
  const [draftData, setDraftData] = useState([...mangaData]);
  const [newLink, setNewLink] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleAdd = () => {
    const newData = {
      id: Date.now(),
      title: "New Manga",
      chapter: "Chapter 1",
      lastUpdated: new Date().toISOString(),
      imageUrl: "",
      link: newLink,
      status: "Good",
    };
    setDraftData([...draftData, newData]);
  };

  const handleDelete = (id: number) => {
    setDraftData(draftData.filter((item) => item.id !== id));
  };

  const handleConfirm = () => {
    onUpdate(draftData);
    setSuccessMessage("Changes confirmed successfully!");
    setTimeout(() => setSuccessMessage(""), 3000); // Clear message after 3 seconds
  };

  const handleDiscard = () => {
    setDraftData([...mangaData]);
    setSuccessMessage("Changes discarded!");
    setTimeout(() => setSuccessMessage(""), 3000); // Clear message after 3 seconds
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 backdrop-blur-sm">
      <div className="relative top-20 mx-auto p-5 border w-2/3 shadow-lg rounded-md bg-white z-50">
        <button
          onClick={onClose}
          className="absolute top-2 right-3 text-xl text-gray-600 hover:text-gray-800"
        >
          &times;
        </button>
        <h3 className="text-lg font-semibold mb-4 text-blue-600">
          Edit Manga List
        </h3>
        <div className="my-4 border p-2 rounded-lg shadow">
          <input
            type="text"
            value={newLink}
            onChange={(e) => setNewLink(e.target.value)}
            className="border p-1 mr-2 rounded"
            placeholder="Enter new manga link"
          />
          <button
            onClick={handleAdd}
            className="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
          >
            Add
          </button>
        </div>
        <table className="min-w-full text-left border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-4 py-2">Title</th>
              <th className="border px-4 py-2">Link</th>
              <th className="border px-4 py-2">Status</th>
              <th className="border px-4 py-2">Delete</th>
            </tr>
          </thead>
          <tbody>
            {draftData.map((manga) => (
              <tr key={manga.id}>
                <td className="border px-4 py-2 max-w-xs overflow-auto whitespace-nowrap">
                  {manga.title}
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
        <div className="flex justify-between mt-4">
          <button
            onClick={handleConfirm}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Confirm changes
          </button>
          <button
            onClick={handleDiscard}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Discard Changes
          </button>
        </div>
        {successMessage && (
          <div className="text-green-500 mt-3">{successMessage}</div>
        )}
      </div>
    </div>
  );
};
