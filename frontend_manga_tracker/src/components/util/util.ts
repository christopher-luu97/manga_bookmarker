export const capitalizeFirstLetterOfEachWord = (str: string): string => {
  return str.replace(/\b\w/g, (char) => char.toUpperCase());
};
