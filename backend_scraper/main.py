from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Dict, Any
from datetime import timedelta
from src.manga_scraper_service import MangaScraperService
from data_models.manga_records import MangaList
from src.auth import create_access_token, get_current_user, oauth2_scheme, TokenData


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate MangaScraperService
manga_scraper_service = MangaScraperService()

# Dummy database of users
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    """
    Authenticate users and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): User login credentials.

    Returns:
        Dict[str, str]: Access token and token type.
    """
    # Authentication logic here
    # This is a simplified placeholder logic

    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_id = user_dict.get("user_id")  # Assuming you have user_id stored in your fake user DB
    access_token_expires = timedelta(minutes=30) # set 30
    access_token = create_access_token(
        data={"sub": form_data.username, "user_id": user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Now let's adjust the endpoints to require authentication
@app.get("/users/me")
async def read_users_me(current_user: TokenData = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get current user profile.

    Args:
        current_user (TokenData): Current user's token data, injected by dependency.

    Returns:
        Dict[str, Any]: User information.
    """
    return {"username": current_user.username, "user_id": current_user.user_id}

@app.post("/insert_record")
async def update_manga_list(manga_list: MangaList):
    """
    Endpoint to update the manga list.

    Args:
        manga_list (MangaList): The manga list to be processed.

    Returns:
        Dict: A dictionary containing the confirmation message, URL, response data, and database upload status.
    """
    # Process the manga_list using MangaScraperService
    output_list, error_list = manga_scraper_service.scrape_record(manga_list)
    insert_record_response = manga_scraper_service.bulk_insert_record(output_list, refresh_data=False)
    manga_scraper_service.delete_record(manga_list)
    response = manga_scraper_service.ms_db.get_frontend_data()

    return {
        "message": "Successfully confirmed", 
        "url": "http://127.0.0.1:8000/insert_record", 
        "confirmation": response,
        "db_upload_status": insert_record_response
    }

@app.get("/get_data", response_model=List[Dict[str, Any]])
async def get_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend.

    Returns:
        List[Dict[str, Any]]: List of manga data for the frontend.
    """
    manga_list = manga_scraper_service.ms_db.get_frontend_data()
    return manga_list

@app.get("/get_bookmarks_data", response_model=List[Dict[str, Any]])
async def get_frontend_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend bookmarks component.

    Returns:
        List[Dict[str, Any]]: List of manga data for the frontend bookmarks component.
    """
    manga_list = manga_scraper_service.ms_db.get_bookmarks_data()
    return manga_list

@app.get("/get_supported_websites", response_model=List[Dict[str, Any]])
async def get_supported_websites_data_api() -> List[Dict[str, Any]]:
    """
    Endpoint to retrieve manga data for the frontend supported websites component within bookmarks.

    Returns:
        List[Dict[str, Any]]: List of manga data for the frontend supported websites component.
    """
    manga_list = manga_scraper_service.ms_db.get_supported_websites()
    return manga_list

@app.get("/refresh_data")
async def refresh_data():
    """
    Endpoint to refresh data by scraping existing websites for new chapters using MangaScraperService.

    Returns:
        str: A message indicating the status of the data refresh.
    """
    response = manga_scraper_service.refresh_backend_data()
    return response