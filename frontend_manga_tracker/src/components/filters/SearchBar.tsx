export const SearchBar: React.FC<{
  searchTerm: string;
  onSearchChange: (searchTerm: string) => void;
}> = ({ searchTerm, onSearchChange }) => {
  return (
    <input
      type="text"
      value={searchTerm}
      onChange={(e) => onSearchChange(e.target.value)}
      placeholder="Search..."
      className="p-2 border border-gray-300 rounded w-full md:w-auto"
    />
  );
};
