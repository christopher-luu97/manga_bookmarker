export const getStatusColor = (status: string) => {
  switch (status) {
    case "Good":
      return "bg-green-500";
    case "Down":
      return "bg-red-500";
    case "200":
      return "bg-green-500";
    case "401":
      return "bg-red-500";
    default:
      return "bg-gray-500";
  }
};
