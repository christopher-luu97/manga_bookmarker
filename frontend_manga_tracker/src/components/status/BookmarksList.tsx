import React from "react";
import { getStatusColor } from "./statusColour";

export const BookmarksList: React.FC<{
  bookmarksData: any[];
  supportedWebsitesData: any[];
}> = ({ bookmarksData, supportedWebsitesData }) => {
  return (
    <div className="border border-gray-200 shadow-xl rounded-lg p-4 bg-white">
      {/* Supported Websites Section */}
      <h3 className="text-lg font-semibold mb-4 text-left">
        Supported Websites
      </h3>
      <div className="max-h-84 mb-6 overflow-auto shadow-inner rounded-lg p-2">
        <ul>
          {supportedWebsitesData.map((website) => (
            <li
              key={website.id} // Use the unique id as the key
              className="flex items-center mb-2 text-left"
            >
              <span
                className={`inline-block h-4 w-4 rounded-full mr-2 ${getStatusColor(
                  website.status
                )}`}
              ></span>
              <a
                href={website.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800"
              >
                {website.title} : {website.link}
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* Manga Bookmarks Section */}
      <h3 className="text-lg font-semibold mb-4 text-left">Manga Bookmarks</h3>
      {bookmarksData.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-4">
          <p className="text-lg md:text-xl font-semibold mb-3">
            No data in the database!
          </p>
          <p className="text-md md:text-lg mb-2">
            Add records by clicking the Edit button on the computer.
          </p>
          <div className="hidden md:block">
            <p className="text-sm text-gray-600 italic">
              (The Edit button is not available on mobile devices)
            </p>
          </div>
        </div>
      ) : (
        <div className="max-h-64 overflow-auto shadow-inner rounded-lg p-2">
          <ul>
            {bookmarksData.map((manga) => (
              <li key={manga.id} className="mb-4 text-left">
                <div className="flex">
                  <span
                    className={`inline-block h-4 w-4 rounded-full mt-1 mr-2 ${getStatusColor(
                      manga.status
                    )}`}
                  ></span>
                  <div className="flex-grow">
                    <a
                      href={manga.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800"
                    >
                      {manga.title}
                    </a>
                    <div className="text-sm text-gray-600">
                      {manga.lastUpdated}
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
