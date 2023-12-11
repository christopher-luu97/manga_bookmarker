import pytest
import requests_mock

# This dictionary defines the storage mechanism of which we will contain the data as a json object
# TODO: Migrate to become a CRUD app where this forms the backend database to perform search on
manga_list = {
    "tcb_scans":{
        "url":"https://tcbscans.com/",
        "manga_paths":{
            "one_piece": "/mangas/5/one-piece",
            "my_hero_academia": "/mangas/6/my-hero-academia",
            "chainsaw_man": "/mangas/13/chainsaw-man",
            "jujutsu_kaisen": "/mangas/4/jujutsu-kaisen"
        }
    },
    "mangakakalot":{
        "url":"https://chapmanganato.com/",
        "manga_paths":{
            "battle_through_the_heavens":"/manga-gv952204"
        }
    },
    "flamescans":{
        "url":"https://flamecomics.com/",
        "manga_paths":{
        }
    },
    "mangademon":{
        "url":"https://manga-demon.org/",
        "manga_paths":{
            "overgeared":"/manga/Overgeared-VA45"
        }
    },
    "webtoons":{
        "url":"https://webtoons.com/",
        "manga_paths":{
        }
    },
    "creepyscans":{
        "url":"https://creepyscans.com/",
        "manga_paths":{
        }
    },
    "luminousscans":{
        "url":"https://luminousscans.net/",
        "manga_paths":{
        }
    },
    "asurascans":{
        "url":"https://asuratoon.com/",
        "manga_paths":{
        }
    }
    
}

def test_tcb_scans_scraper():
    scraper = TcbScansScraper(manga_list)
    with requests_mock.Mocker() as m:
        m.get("https://tcbscans.com/mangas/5/one-piece", text='<a href="/chapters/7565/one-piece-chapter-1101" class="block border border-border bg-card mb-3 p-3 rounded">')
        full_link, href, chapter_value = scraper.scrape_manga("tcb_scans", "one_piece")
        assert full_link == "https://tcbscans.com/chapters/7565/one-piece-chapter-1101"
        assert href == "/chapters/7565/one-piece-chapter-1101"
        assert chapter_value is None

def test_tcb_scans_scraper_failure():
    scraper = TcbScansScraper(manga_list)
    with requests_mock.Mocker() as m:
        m.get("https://tcbscans.com/mangas/5/one-piece", status_code=404)
        full_link, href, error_message = scraper.scrape_manga("tcb_scans", "one_piece")
        assert full_link is None
        assert href is None
        assert "Failed to retrieve webpage, status code: 404" in error_message

def test_manga_kakalot_scraper():
    scraper = MangaKakalotScraper(manga_list)
    with requests_mock.Mocker() as m:
        m.get("https://chapmanganato.com/manga-gv952204", text='<a class="chapter-name text-nowrap" href="/chapter-123">Chapter 123</a>')
        full_link, href, chapter_value = scraper.scrape_manga("mangakakalot", "battle_through_the_heavens")
        assert full_link == "https://chapmanganato.com/chapter-123"
        assert href == "/chapter-123"
        assert chapter_value == "chapter-123"

def test_manga_kakalot_scraper_failure():
    scraper = MangaKakalotScraper(manga_list)
    with requests_mock.Mocker() as m:
        m.get("https://chapmanganato.com/manga-gv952204", status_code=404)
        full_link, href, error_message = scraper.scrape_manga("mangakakalot", "battle_through_the_heavens")
        assert full_link is None
        assert href is None
        assert "Failed to retrieve webpage, status code: 404" in error_message

def test_manga_demon_scraper():
    scraper = MangaDemonScraper(manga_list)
    with requests_mock.Mocker() as m:
        m.get("https://manga-demon.org/manga/Overgeared-VA45", text='<ul class="chapter-list"><li><a href="/chapter-50">Chapter 50</a></li></ul>')
        full_link, href, chapter_value = scraper.scrape_manga("mangademon", "overgeared")
        assert full_link == "https://manga-demon.org/chapter-50"
        assert href == "/chapter-50"
        assert chapter_value == "50"

def test_manga_demon_scraper_failure():
    scraper = MangaDemonScraper(manga_list)
    with requests_mock.Mocker() as m:
        m.get("https://manga-demon.org/manga/Overgeared-VA45", status_code=404)
        full_link, href, error_message = scraper.scrape_manga("mangademon", "overgeared")
        assert full_link is None
        assert href is None
        assert "Failed to retrieve webpage, status code: 404" in error_message