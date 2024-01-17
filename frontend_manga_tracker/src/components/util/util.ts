export const capitalizeFirstLetterOfEachWord = (str: string): string => {
  return str.replace(/\b\w/g, (char) => char.toUpperCase());
};

export const getBaseUrl = (url: string): string => {
  try {
    const parsedUrl = new URL(url);
    return `${parsedUrl.protocol}//${parsedUrl.hostname}`;
  } catch (error) {
    console.error("Invalid URL:", error);
    return "";
  }
};

export const isSupportedWebsite = (
  url: string,
  supportedWebsites: string[]
): boolean => {
  const baseUrl = getBaseUrl(url);
  return supportedWebsites.includes(baseUrl);
};
