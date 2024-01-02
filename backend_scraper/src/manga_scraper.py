import bs4
import requests
import re
import time

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

    def extract_thumbnail(self, url:str):
        """
        Method to extract thumbnail from MangaKakalot if it exists.
        Method can be overriden by inheriting classes if thumbnails exists that we can scrape

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            # Navigate to the div with the class 'story-info-left'
            div_tag = soup.find('div', class_='story-info-left')
            if div_tag:
                # Find the img tag within the nested span
                image_tag = div_tag.find('span', class_='info-image').find('img')
                if 'src' in image_tag.attrs:
                    return image_tag.attrs['src']
                else:
                    return "Image or src attribute not found"
            else:
                return "Div with specified class not found"
        else:
            return f"Failed to retrieve webpage, status code: {response.status_code}"
    

    def create_record(self,url:str) -> Dict:
        """
        Method to create the dataset required for database insertion

        Args:
            url (str): Main manga link

        Raises:
            NotImplementedError: _description_

        Returns:
            Dict: Object containing the data object to be inserted into the database
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
    
    def create_record(self, url: str) -> Dict:
        return super().create_record(url)
    
        
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
    
    def find_manga_link(self, search_string:str, search_query:str) -> Optional[str]:
        """
        Find the manga link with a title matching the query_string in the provided BeautifulSoup object.

        Args:
            soup (bs4.BeautifulSoup): BeautifulSoup object of the parsed HTML content.
            query_string (str): The query string to match (case-insensitive).

        Returns:
            Optional[str]: The URL of the manga if found, None otherwise.
        """
        response = requests.get(search_string)

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

        item_right = soup.find('div', class_='item-right')
        if item_right:
            links = item_right.find_all('a', class_='a-h text-nowrap item-title')
            for link in links:
                if link.get('title', '').lower() == search_query.lower():
                    return link.get('href')
        return None

    def create_record(self, url: str) -> Dict:
        return super().create_record(url)


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

    def create_record(self, url: str) -> Dict:
        return super().create_record(url)
    
class vizScraper(MangaScraper):
    def __init__(self, manga_list: List[dict]):
        super().__init__(manga_list)
        self.base_url = "https://www.viz.com/"

    def parse_html(self, soup: bs4.BeautifulSoup, base_url: str, complete_url: str) -> Tuple[str | None, str | None, str]:
        """
        Parses the HTML content from the Viz website to find the first href within the 'chpt_rows' div.

        Args:
            soup (bs4.BeautifulSoup): Parsed HTML content.
            base_url (str): Base URL of the Viz website.
            complete_url (str): Complete URL of the manga page.

        Returns:
            Tuple[str | None, str | None, str]: The most recent URL (None if not found),
            the href (None if not found), and the chapter value or an error message.
        """
        chpt_rows_div = soup.find('div', id='chpt_rows')
        if chpt_rows_div:
            first_link = chpt_rows_div.find('a', href=True)
            if first_link:
                href = first_link.get('href')
                most_recent_url = self.normalize_url(base_url + href)
                chapter_value = self.extract_last_part(most_recent_url)
                return (most_recent_url, href, chapter_value)
            else:
                return None, None, 'No link found in the specified div'
        else:
            return None, None, 'Div with id "chpt_rows" not found'
        

    def extract_name(self, url:str):
        """
        Viz manga always has name at the end

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        # Regular expression to extract the part after the last '/'
        match = re.search(r'/([^/]*)/?$', url)
        
        if match:
            # Extract the matched part and replace '-' with ' '
            result = match.group(1).replace('-', ' ')
            return result
        else:
            return "No match found"
    
    def extract_manga_path(self, url:str):
        """
        Extract manga path from url. 
        

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        # Regular expression to extract everything after '.com'
        match = re.search(r'\.com(.*)', url)
        
        if match:
            # Extract the matched part
            return match.group(1)
        else:
            return "No match found"

    def extract_latest_chapter(self, url:str):
        """
        Grab the link to the latest chapter

        Args:
            url (str): _description_
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            return self.parse_html(soup, self.base_url, url), response.status_code
    
    ##TODO: Page number on viz is rendered dynamically through JS which can't be fetched with bs4 or requests
    def extract_chapter_length(self, url:str):
        """
        URL comes from latest_chapter in parse_html_obj[0] from self.extract_latest_chapter

        Args:
            url (_type_): _description_
        """
         # Parse the HTML content
        soup = bs4.BeautifulSoup(url, 'html.parser')
        
        # Find the <div> with the specific class
        div = soup.find('div', class_='page_slider_label left')
        
        if div:
            # Extract the text from the <div>
            text = div.get_text().strip()
            
            # Use regular expression to find the integer
            match = re.search(r'\d+', text)
            if match:
                return int(match.group(0))
            else:
                return "No integer found in the text"
        else:
            return "Div not found"
        
    def create_record(self, url:str) -> Dict:
        """
        This method is used for first time additions of new manga.
        Each record will contain all the data required for database insertion

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        parse_html_obj, response_code = self.extract_latest_chapter(url)
        record = {
            "manga_name": self.extract_name(url), # Get the manga name
            "manga_path": self.extract_manga_path(url),
            "chapter_url": parse_html_obj[0],
            "date_checked":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), # Convert epoch time to ymdhms
            "number_of_pages":self.extract_chapter_length(parse_html_obj[0]),
            "chapter_url_status":response_code,
            "manga_thumbnail_url": self.extract_thumbnail(url)
        }
        return record

    def extract_thumbnail(self, url:str):
        """
        Extract the thumbnail from the website

        Args:
            url (str): string url of the website

        Returns:
            _type_: _description_
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            image_tag = soup.find('img', class_='o_hero-media')
            if 'src' in image_tag.attrs.keys():
                return image_tag.attrs['src']
            else:
                return "Image or src attribute not found"
        else:
            return f"Failed to retrieve webpage, status code: {response.status_code}"


class webtoonScraper(MangaScraper):
    def __init__(self, manga_list: List[dict]):
        super().__init__(manga_list)
        self.base_url = "https://www.webtoons.com/"

    def parse_html(self, soup: bs4.BeautifulSoup, base_url: str, complete_url: str) -> Tuple[str | None, str | None, str]:
        """
        Parses the HTML content from the Webtoon website to find the first href within the 'ul' with id '_listUl'.

        Args:
            soup (bs4.BeautifulSoup): Parsed HTML content.
            base_url (str): Base URL of the Webtoon website.
            complete_url (str): Complete URL of the manga page.

        Returns:
            Tuple[str | None, str | None, str]: The most recent URL (None if not found),
            the href (None if not found), and the chapter value or an error message.
        """
        list_ul = soup.find('ul', id='_listUl')
        if list_ul:
            first_link = list_ul.find('a', href=True)
            if first_link:
                href = first_link.get('href')
                return href, None, "Success"
            else:
                return None, None, 'No link found in the specified ul'
        else:
            return None, None, 'Ul with id "_listUl" not found'
        
    def extract_name(self, url:str):
        """
        Viz manga always has name at the end

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        # REGEX as we know the name apears after the third / in the url
        match = re.search(r'www.webtoons.com/[^/]+/[^/]+/([^/]+)/', url)
        
        if match:
            # Extract the matched part and replace '-' with ' '
            result = match.group(1).replace('-', ' ')
            return result
        else:
            return "No match found"
    
    def extract_manga_path(self, url:str):
        """
        Extract manga path from url. 
        

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        # Regular expression to extract everything after '.com'
        match = re.search(r'\.com(.*)', url)
        
        if match:
            # Extract the matched part
            return match.group(1)
        else:
            return "No match found"

    def extract_latest_chapter(self, url:str):
        """
        Grab the link to the latest chapter

        Args:
            url (str): _description_
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            return self.parse_html(soup, self.base_url, url), response.status_code
    
    def create_record(self, url:str) -> Dict:
        """
        This method is used for first time additions of new manga.

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        parse_html_obj, response_code = self.extract_latest_chapter(url)
        record = {
            "manga_name": self.extract_name(url), # Get the manga name
            "manga_path": self.extract_manga_path(url),
            "chapter_url": parse_html_obj[0],
            "date_checked":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), # Convert epoch time to ymdhms
            "number_of_pages":self.extract_chapter_length(parse_html_obj[0]),
            "chapter_url_status":response_code,
            "manga_thumbnail_url": self.extract_thumbnail(url)
        }
        return record

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