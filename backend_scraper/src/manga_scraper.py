import bs4
import requests
import re

from typing import Optional, List, Dict, Union, Any, Tuple

class MangaScraper:
    def __init__(self, manga_list: List[dict]):
        """
        Initializes the MangaScraper with a list of manga.

        Args:
            manga_list (List[dict]): List of manga with their details.
        """
        self.manga_list = manga_list
        self.soup: Optional[bs4.BeautifulSoup] = None

    def scrape_manga(self, website_name: str, manga_name: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Scrapes manga data from a given website.

        Args:
            website_name (str): The name of the website to scrape.
            manga_name (str): The name of the manga to scrape.

        Returns:
            Tuple[Optional[str], Optional[str], str]: Returns the most recent URL, the href, and the chapter value or error message.
        """
        website_url, manga_url = self.get_urls(website_name, manga_name)
        complete_url = self.normalize_url(website_url + manga_url)
        response = requests.get(complete_url)

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            self.soup = soup
            return self.parse_html(soup, website_url, complete_url)
        else:
            return None, None, f'Failed to retrieve webpage, status code: {response.status_code}'

    def get_urls(self, website_name:str, manga_name:str) -> Tuple[str, str]:
        """
        Provided a website name and manga name, return the URL's
        This is an interim-method that reads in the data from a list

        Args:
            website_name (str): Name of the website
            manga_name (str): Name of manga

        Returns:
            (website_url, manga_url): Tuple containing the website url and manga url
        """
        website_url = self.manga_list[website_name]["url"]
        manga_url = self.manga_list[website_name]["manga_paths"][manga_name]
        return website_url, manga_url

    def normalize_url(self,url:str) -> str:
        """
        util function to remove any unnecessary '/'

        Args:
            url (str): url as a string

        Returns:
            normalized_url (str): normalized url
        """
        # Pattern to find '//' that are not preceded by 'https:'
        pattern = re.compile(r'(?<!https:)//')
        # Replace '//' with '/'
        normalized_url = pattern.sub('/', url)
        return normalized_url
    
    def extract_last_part(self, input_string: str) -> str:
        """
        Extracting the end of an input URL

        Args:
            input_string (str): URL input

        Returns:
            str: Matching string
        """
        # Regex pattern to capture the last part after the final dash
        pattern = re.compile(r'-(\d+)$')

        # Search for the pattern in the input string
        match = pattern.search(input_string.strip())

        # Return the matched part if found, otherwise return an empty string
        return match.group(1) if match else ""

    def parse_html(self, soup: bs4.BeautifulSoup, base_url: str, complete_url: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Parses the HTML content from the soup object. 
        This method should be overridden in subclasses.

        Args:
            soup (bs4.BeautifulSoup): Parsed HTML content.
            base_url (str): Base URL of the manga website.
            complete_url (str): Complete URL of the manga page.

        Raises:
            NotImplementedError: Indicates the method needs implementation in subclasses.

        Returns:
            Tuple[Optional[str], Optional[str], str]: Returns parsed data or error message.
        """
        raise NotImplementedError("Subclasses should implement this method")
    


class TcbScansScraper(MangaScraper):
    def parse_html(self, soup: bs4.BeautifulSoup, base_url: str, complete_url: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Parses the HTML content from TCBScans website.

        Args:
            soup (bs4.BeautifulSoup): Parsed HTML content.
            base_url (str): Base URL of TCBScans website.
            complete_url (str): Complete URL of the manga page.

        Returns:
            Tuple[Optional[str], Optional[str], str]: Returns the most recent URL, the href, and the chapter value or error message.
        """       
        a_tag = soup.find('a', class_='block border border-border bg-card mb-3 p-3 rounded')
        if a_tag:
            href = a_tag.get('href')
            most_recent_url = self.normalize_url(base_url + href)
            chapter_value = self.extract_last_part(most_recent_url)
            print(f"Complete url: {complete_url}")
            return most_recent_url, href, chapter_value
        else:
            return None, None, 'Tag not found'
    
        
class MangaKakalotScraper(MangaScraper):
    def parse_html(self, soup: bs4.BeautifulSoup, base_url: str, complete_url: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Parses the HTML content from MangaKakalot website.

        Args:
            soup (bs4.BeautifulSoup): Parsed HTML content.
            base_url (str): Base URL of MangaKakalot website.
            complete_url (str): Complete URL of the manga page.

        Returns:
            Tuple[Optional[str], Optional[str], str]: Returns the most recent URL, the href, and the chapter value or error message.
        """
        a_tag = soup.find('a', class_='chapter-name text-nowrap')

        if a_tag:
            href = a_tag.get('href')
            chapter_match = re.search(r'chapter-\d+', href)

            if chapter_match:
                chapter_value = self.extract_last_part(chapter_match.group())
                most_recent_url = self.normalize_url(complete_url)
                return most_recent_url, href, chapter_value

            return None, href, 'Chapter value not found'
        return None, None, 'Tag not found'
    
    def get_genres(self, soup: bs4.BeautifulSoup) -> dict:
        """
        Get genres from the soup object specific to MangaKakalot.

        Args:
            soup (bs4.BeautifulSoup): Parsed HTML content.

        Returns:
            dict: Dictionary containing genres.
        """
        # Find the element containing 'info-genres' icon
        genre_icon = soup.find('i', class_='info-genres')

        # Ensure we have found the correct element and it has a parent
        if genre_icon and genre_icon.parent:
            genres_td = genre_icon.parent.find_next_sibling('td')

            if genres_td:
                genre_links = genres_td.find_all('a', class_='a-h')
                genres = [link.get_text() for link in genre_links]
                return {"genres": genres}

        return {"genres": []}


class MangaDemonScraper(MangaScraper):
    def parse_html(self, soup: bs4.BeautifulSoup, base_url: str, complete_url: str) -> Tuple[Optional[str], Optional[str], str]:
        """
        Parses the HTML content from MangaDemon website.

        Args:
            soup (bs4.BeautifulSoup): Parsed HTML content.
            base_url (str): Base URL of MangaDemon website.
            complete_url (str): Complete URL of the manga page.

        Returns:
            Tuple[Optional[str], Optional[str], str]: Returns the most recent URL, the href, and the chapter value or error message.
        """
        ul_tag = soup.find('ul', class_='chapter-list')

        if ul_tag:
            li_tag = ul_tag.find('li')

            if li_tag:
                a_tag = li_tag.find('a', href=True)

                if a_tag:
                    href = a_tag['href']
                    chapter_match = re.search(r'chapter/([0-9a-zA-Z-]+)', href)

                    if chapter_match:
                        chapter_value = chapter_match.group(1)
                        full_link = self.normalize_url(base_url + href)
                        return full_link, href, chapter_value

                    return base_url + href, href, 'Chapter value not found'

                return None, None, '<a> tag not found'

            return None, None, '<li> tag not found'

        return None, None, '<ul> tag with class "chapter-list" not found'

## Example usage
# manga_list = {
#     "tcb_scans":{
#         "url":"https://tcbscans.com/",
#         "manga_paths":{
#             "one_piece": "/mangas/5/one-piece",
#             "my_hero_academia": "/mangas/6/my-hero-academia",
#             "chainsaw_man": "/mangas/13/chainsaw-man",
#             "jujutsu_kaisen": "/mangas/4/jujutsu-kaisen"
#         }
#     },
#     "mangakakalot":{
#         "url":"https://chapmanganato.com/",
#         "manga_paths":{
#             "battle_through_the_heavens":"/manga-gv952204"
#         }
#     },
#     "mangademon":{
#         "url":"https://manga-demon.org/",
#         "manga_paths":{
#             "overgeared":"/manga/Overgeared-VA45"
#         }
#     }
# }
# kakalot_scraper = MangaKakalotScraper(manga_list)
# full_link, href, chapter_value = kakalot_scraper.scrape_manga("mangakakalot", "battle_through_the_heavens")
# genres = kakalot_scraper.get_genres(kakalot_scraper.soup)
# print(genres)