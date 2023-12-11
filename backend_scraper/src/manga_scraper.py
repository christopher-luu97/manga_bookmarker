import requests
import bs4
import re
from typing import List, Union, Any, Dict, Tuple

class MangaScraper:
    def __init__(self, manga_list:List[str]):
        self.manga_list = manga_list

    def scrape_manga(self, website_name:str, manga_name:str):
        website_url, manga_url = self.get_urls(website_name, manga_name)
        complete_url = self.normalize_url(website_url + manga_url)
        response = requests.get(complete_url)

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            return self.parse_html(soup, website_url, complete_url)
        else:
            return None, None, f'Failed to retrieve webpage, status code: {response.status_code}'

    def get_urls(self, website_name:str, manga_name:str) -> Tuple[str, str]:
        """_summary_

        Args:
            self (_type_): _description_
            str (_type_): _description_

        Returns:
            _type_: _description_
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
            str: normalized url
        """
        # Pattern to find '//' that are not preceded by 'https:'
        pattern = re.compile(r'(?<!https:)//')
        # Replace '//' with '/'
        normalized_url = pattern.sub('/', url)
        return normalized_url
    
    def extract_last_part(self, input_string: str) -> str:
        """_summary_

        Args:
            input_string (str): _description_

        Returns:
            str: _description_
        """
        # Regex pattern to capture the last part after the final dash
        pattern = re.compile(r'-(\d+)$')

        # Search for the pattern in the input string
        match = pattern.search(input_string.strip())

        # Return the matched part if found, otherwise return an empty string
        return match.group(1) if match else ""

    def parse_html(self, soup:bs4.BeautifulSoup, base_url:str, complete_url:str):
        """_summary_

        Args:
            soup (_type_): _description_
            base_url (_type_): _description_
            complete_url (_type_): _description_

        Raises:
            NotImplementedError: _description_
        """
        # This method needs to be overridden in subclasses to handle different parsing logic for different websites
        raise NotImplementedError("Subclasses should implement this method")
    


class TcbScansScraper(MangaScraper):
    def parse_html(self, soup, base_url, complete_url):
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
    def parse_html(self, soup, base_url, complete_url):
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

class MangaDemonScraper(MangaScraper):
    def parse_html(self, soup, base_url, complete_url):
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



