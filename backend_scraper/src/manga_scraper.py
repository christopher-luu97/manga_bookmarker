import bs4
import requests
import re
import time
import jellyfish
from urllib.parse import urlparse, urljoin
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

    @staticmethod
    def get_base_url(url:str) -> str:
        """
        Get the base URL from a website.

        Args:
            url (str): URL of input website

        Returns:
            base_url (str): Base url of the input website
        
        Example usage
        url1 = "https://chat.openai.com/c/ac154504-d217-4ed1-b4c3-0db4cee603a2"
        url2 = "https://anaconda.org/anaconda/psycopg2"

        print(get_base_url(url1))  # Output: https://chat.openai.com
        print(get_base_url(url2))  # Output: https://anaconda.org
        """
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return base_url

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

    def extract_thumbnail(self, url:str) -> str:
        """
        Method to extract thumbnail from MangaKakalot if it exists.
        Method can be overriden by inheriting classes if thumbnails exists that we can scrape

        Args:
            url (str): URL to scrape from

        Returns:
            str: the image tag as a str or error strings
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
            NotImplementedError: Error to indicate this method for inherited classes has not been implemented

        Returns:
            Dict: Object containing the data object to be inserted into the database
        """
        raise NotImplementedError("Subclasses should implement this method")
    
    def get_chapter_number(self, url:str) -> int:
        """
        Method to extract chapter number from provided link

        Args:
            url (str): Main manga link

        Raises:
            NotImplementedError: Error to indicate this method for inherited classes has not been implemented

        Returns:
            Dict: Object containing the data object to be inserted into the database
        """
        raise NotImplementedError("Subclasses should implement this method")

    def extract_chapter_length(self, url:str) -> int:
        """
        Method to extract chapter length from provided link

        Args:
            url (str): Main manga link

        Raises:
            NotImplementedError: Error to indicate this method for inherited classes has not been implemented

        Returns:
            Dict: Object containing the data object to be inserted into the database
        """
        raise NotImplementedError("Subclasses should implement this method")
        
class MangaKakalotScraper(MangaScraper):
    def __init__(self, manga_list: List[dict]):
        super().__init__(manga_list)
        self.base_url = "https://manganato.com/"

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
    
    def find_manga_link(self, search_query:str) -> Optional[str]:
        """
        Find the manga link with a title matching the query_string in the provided BeautifulSoup object.

        Args:
            search_query (str): The query string to match (case-insensitive).

        Returns:
            Optional[str]: The URL of the manga if found, None otherwise.
        """
        search_query_link = search_query.strip().replace(" ", "_")
        search_string = f"https://chapmanganato.to/https://manganato.com/search/story/{search_query_link}"
        response = requests.get(search_string)

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')

        item_right = soup.find('div', class_='item-right')
        if item_right:
            links = item_right.find_all('a', class_='a-h text-nowrap item-title')
            for link in links:
                similarity = jellyfish.jaro_similarity(search_query.lower(), link.get('title','').lower())
                if similarity > 0.80:  
                    return link.get('href')
        return None
    

    def extract_name(self, url:str) -> str:
        """
        Get name from website via scraping

        Args:
            url (str): URL of website to scrape from

        Returns:
            str: Name of website or error
        """
        response = requests.get(url)

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
        # Regular expression to extract the part after the last '/'
            story_info_right_div = soup.find('div', class_='story-info-right')
            if story_info_right_div:
                h1_tag = story_info_right_div.find('h1')
                if h1_tag:
                    return h1_tag.get_text().strip()
        return "Manga title not found"
    
    def extract_manga_path(self, url:str) -> str:
        """
        Extract manga path from url. 
        
        Example url:"https://chapmanganato.to/manga-ax951880". This is Tales of Demons and Gods manhua
        Example output: /manga-ax951880

        Args:
            url (str): URL of website to scrape from

        Returns:
            str: Manga path which exists after the domain/ or error
        """
        # Regular expression to extract everything after '.com'
        match = re.search(r'https?://[^/]+(/.*)', url)

        if match:
            return match.group(1)
        else:
            return "No match found"

    def extract_latest_chapter(self, url:str) -> Tuple[Tuple, str]:
        """
        Grab the link to the latest chapter

        Args:
            url (str): URL of website to scrape from

        Returns:
            tuple(tuple, str): Returns a tuple of various parsed objects and a status code
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            return self.parse_html(soup, self.base_url, url), response.status_code
    
    ##TODO: Page number on viz is rendered dynamically through JS which can't be fetched with bs4 or requests
    def extract_chapter_length(self, url: str) -> Union[int, str]:
        """
        URL comes from latest_chapter in parse_html_obj[0] from self.extract_latest_chapter

        Args:
            url (str): URL of website to scrape from

        Returns:
            Union[int, str]: Either the extracted integer chapter length or a string indicating no integer found or div not found.
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
        
    def get_latest_chapter(self, url: str) -> Union[str, None]:
        """
        Grabs only the latest chapter from a given URL.

        Args:
            url (str): The URL of the manga page.

        Returns:
            str: The URL of the latest chapter, or None if not found or an error occurred.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            html_content = response.text

            soup = bs4.BeautifulSoup(html_content, 'html.parser')
            ul = soup.find('ul', class_='row-content-chapter')
            first_link = ul.find('a', class_='chapter-name') if ul else None
            return first_link.get('href') if first_link else None
        except Exception as e:
            print(f"Error occurred while fetching the latest chapter: {e}")
            return None

    def create_record(self, url: str, base_url: str) -> Dict[str, Any]:
        """
        This method is used for first time additions of new manga.

        Args:
            url (str): The URL of the manga page.
            base_url (str): The base URL of the manga website.

        Returns:
            Dict[str, Any]: A dictionary containing the manga record details.
        """
        parse_html_obj, response_code = self.extract_latest_chapter(url)
        record = {
            "manga_name": self.extract_name(url), # Get the manga name
            "manga_path": self.extract_manga_path(url),
            "chapter_url": self.get_latest_chapter(url),
            "date_checked":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), # Convert epoch time to ymdhms
            "number_of_pages": 0, # self.extract_chapter_length(parse_html_obj[0]),
            "chapter_url_status":response_code,
            "manga_thumbnail_url": self.extract_thumbnail(url),
            "website_url": base_url,
            "chapter_number": parse_html_obj[2]
        }
        return record
    
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
        

    def extract_name(self, url: str) -> str:
        """
        Extracts the manga name from the URL.

        Args:
            url (str): The URL of the manga page.

        Returns:
            str: The extracted manga name.
        """
        # Regular expression to extract the part after the last '/'
        match = re.search(r'/([^/]*)/?$', url)
        
        if match:
            # Extract the matched part and replace '-' with ' '
            result = match.group(1).replace('-', ' ')
            return result
        else:
            return "No match found"
    
    def extract_manga_path(self, url: str) -> str:
        """
        Extracts the manga path from the URL.

        Args:
            url (str): The URL of the manga page.

        Returns:
            str: The extracted manga path.
        """
        # Regular expression to extract everything after '.com'
        match = re.search(r'\.com(.*)', url)
        
        if match:
            # Extract the matched part
            return match.group(1)
        else:
            return "No match found"

    def extract_latest_chapter(self, url: str) -> Tuple:
        """
        Grabs the link to the latest chapter.

        Args:
            url (str): The URL of the manga page.

        Returns:
            Tuple: A tuple containing the result of parse_html and the HTTP response status code.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            return self.parse_html(soup, self.base_url, url), response.status_code

    ## TODO: Page number on viz is rendered dynamically through JS, which can't be fetched with bs4 or requests
    def extract_chapter_length(self, url: str) -> int:
        """
        Extracts the length of the manga chapter.

        Args:
            url (str): The URL of the manga chapter.

        Returns:
            int: The number of pages in the manga chapter.
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
                return 0  # Default value if no integer found in the text
        else:
            return 0  # Default value if <div> not found
        
    def create_record(self, url: str) -> Dict:
        """
        Creates a record for a new manga.

        Args:
            url (str): The URL of the manga page.

        Returns:
            Dict: A dictionary containing all the data required for database insertion.
        """
        parse_html_obj, response_code = self.extract_latest_chapter(url)
        record = {
            "manga_name": self.extract_name(url),  # Get the manga name
            "manga_path": self.extract_manga_path(url),
            "chapter_url": parse_html_obj[0],
            "date_checked": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),  # Convert epoch time to ymdhms
            "number_of_pages": 0 if self.extract_chapter_length(parse_html_obj[0]) == "Div not found" else self.extract_chapter_length(parse_html_obj[0]),
            "chapter_url_status": response_code,
            "manga_thumbnail_url": self.extract_thumbnail(url),
            "website_url": self.get_base_url(parse_html_obj[0]),
            "chapter_number": self.get_chapter_number(parse_html_obj[0])
        }
        return record
    
    def get_chapter_number(self, url: str) -> int:
        """
        Get the chapter number from the link.

        Args:
            url (str): The URL of the manga chapter.

        Returns:
            int: The chapter number if found, otherwise None.
        """
        pattern = r"chapter-(\d+)"
        match = re.search(pattern, url)
    
        # Return the matched group (digits after "chapter-") if found
        return int(match.group(1)) if match else None

    def extract_thumbnail(self, url: str) -> str:
        """
        Extract the thumbnail URL from the website.

        Args:
            url (str): The URL of the manga page.

        Returns:
            str: The URL of the manga thumbnail if found, otherwise an error message.
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
        
    def extract_name(self, url:str) -> str:
        """
        Extracts the manga name from the URL.

        Args:
            url (str): The URL of the manga page.

        Returns:
            str: The extracted manga name.
        """
        # REGEX as we know the name apears after the third / in the url
        match = re.search(r'www.webtoons.com/[^/]+/[^/]+/([^/]+)/', url)
        
        if match:
            # Extract the matched part and replace '-' with ' '
            result = match.group(1).replace('-', ' ')
            return result
        else:
            return "No match found"
    
    def extract_manga_path(self, url: str) -> str:
        """
        Extracts the manga path from the URL.

        Args:
            url (str): The URL of the manga page.

        Returns:
            str: The extracted manga path.
        """
        # Regular expression to extract everything after '.com'
        match = re.search(r'\.com(.*)', url)
        
        if match:
            # Extract the matched part
            return match.group(1)
        else:
            return "No match found"

    def extract_latest_chapter(self, url: str) -> Tuple:
        """
        Grabs the link to the latest chapter.

        Args:
            url (str): The URL of the manga page.

        Returns:
            Tuple: A tuple containing the result of parse_html and the HTTP response status code.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            return self.parse_html(soup, self.base_url, url), response.status_code
    
    def extract_chapter_length(self, url: str) -> int:
        """
        Leave empty for now

        Args:
            url (str): _description_

        Returns:
            int: _description_
        """
        # Conditional statement that returns div not found potentially
        ## method
        return 0
    
    def create_record(self, url: str) -> Dict:
        """
        Creates a record for a new manga.

        Args:
            url (str): The URL of the manga page.

        Returns:
            Dict: A dictionary containing all the data required for database insertion.
        """
        parse_html_obj, response_code = self.extract_latest_chapter(url)
        record = {
            "manga_name": self.extract_name(url), # Get the manga name
            "manga_path": self.extract_manga_path(url),
            "chapter_url": parse_html_obj[0],
            "date_checked":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), # Convert epoch time to ymdhms
            "number_of_pages": 0 if self.extract_chapter_length(parse_html_obj[0]) == "Div not found" else self.extract_chapter_length(parse_html_obj[0]),
            "chapter_url_status":response_code,
            "manga_thumbnail_url": self.extract_thumbnail(url),
            "website_url": self.get_base_url(parse_html_obj[0]),
            "chapter_number": self.get_chapter_number(parse_html_obj[0])
        }
        return record
    

    def get_chapter_number(self, url: str) -> int:
        """
        Get the chapter number from the link.

        Args:
            url (str): The URL of the manga chapter.

        Returns:
            int: The chapter number if found, otherwise None.
        """
        # Regex pattern to find digits after "episode-"
        pattern = r"episode_no=(\d+)"
        match = re.search(pattern, url)
        
        # Return the matched group (digits after "episode-") if found
        return int(match.group(1)) if match else None
    
class ComickScraper:
    """
    A specialized scraper for extracting manga details from comick.cc.

    Attributes:
        manga_list (List[Dict]): A list of dictionaries containing manga details.
        base_url (str): The base URL of the comick.cc website.
    """

    def __init__(self, manga_list: list):
        """
        Initializes the ComickScraper with a list of manga.

        Args:
            manga_list (List[dict]): List of manga with their details.
        """
        self.manga_list = manga_list
        self.base_url = "https://comick.cc"

    def extract_name(self, url: str) -> str:
        """
        Extracts the manga name from the provided URL.

        Args:
            url (str): URL of the manga page.

        Returns:
            str: The name of the manga or an error message if not found.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            h1_tag = soup.find('h1')
            if h1_tag:
                return h1_tag.text.strip()
        return "Manga title not found"

    def extract_manga_path(self, url: str) -> str:
        """
        Extracts the manga path from the URL.

        Args:
            url (str): The full URL of the manga page.

        Returns:
            str: The path of the manga.
        """
        return urlparse(url).path

    def get_latest_chapter_url(self, soup: bs4.BeautifulSoup) -> Optional[str]:
        """
        Finds the latest chapter URL from the parsed HTML content.

        Args:
            soup (bs4.BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            Optional[str]: The full URL of the latest chapter or None if not found.
        """
        # Assuming the first <a> tag in the <tbody> is the latest chapter
        tbody = soup.find('tbody')
        if tbody:
            chapter_link = tbody.find('a', href=True)
            if chapter_link and 'href' in chapter_link.attrs:
                # Construct the full URL using urljoin to handle relative URLs properly
                return urljoin(self.base_url, chapter_link['href'])
        return None

    def extract_thumbnail(self, soup: bs4.BeautifulSoup, manga_path: str) -> str:
        """
        Finds the manga thumbnail URL by first locating the specific href that
        matches the manga_path + "/covers", then extracts the thumbnail src.

        Args:
            soup (bs4.BeautifulSoup): The BeautifulSoup object containing the parsed HTML.
            manga_path (str): The path of the manga used to construct the target href.

        Returns:
            str: The URL of the manga thumbnail or an error message if not found.
        """
        # Construct the target href we're looking for
        target_href = manga_path + "/covers"

        # Find the <a> tag with the specific href
        cover_link = soup.find('a', href=target_href)
        if cover_link:
            # Within the <a> tag's context, find the <img> tag
            img_tag = cover_link.find_next('img')
            if img_tag and 'src' in img_tag.attrs:
                # Return the src attribute of the <img> tag
                return img_tag['src']

        return "Thumbnail not found"

    def create_record(self, url: str) -> Dict[str, Union[str, int]]:
        """
        Creates a record of manga details from the given URL.

        Args:
            url (str): The URL of the manga page.

        Returns:
            Dict[str, Union[str, int]]: A dictionary containing manga details.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            manga_name = self.extract_name(url)
            manga_path = self.extract_manga_path(url)
            chapter_url = self.get_latest_chapter_url(soup)
            manga_thumbnail_url = self.extract_thumbnail(soup)
            chapter_number = self.get_chapter_number(chapter_url) if chapter_url else 0

            record = {
                "manga_name": manga_name,
                "manga_path": manga_path,
                "chapter_url": chapter_url,
                "date_checked": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                "number_of_pages": 0,  # Implement extract_chapter_length for actual length
                "chapter_url_status": response.status_code,
                "manga_thumbnail_url": manga_thumbnail_url,
                "website_url": self.base_url,
                "chapter_number": chapter_number,
            }
            return record
        else:
            return {"error": f"Failed to retrieve webpage, status code: {response.status_code}"}

    def get_chapter_number(self, url: str) -> int:
        """
        Extracts the chapter number from the chapter URL.

        The chapter number is expected to be between two hyphens, following the
        word 'chapter' and before the last part of the URL, which can vary (e.g., 'en').

        Args:
            url (str): The URL of the chapter.

        Returns:
            int: The chapter number or 0 if not found.
        """
        # The regex captures digits (\d+) that follow 'chapter-' and precede
        # a hyphen. This assumes the chapter number is followed by a hyphen and some text.
        match = re.search(r'chapter-(\d+)-[^-]+$', url)
        if match:
            return int(match.group(1))
        return 0


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