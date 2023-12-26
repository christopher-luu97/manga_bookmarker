# Test backend API with FastAPI
# Only need Django mainly for creating and learning about authentication
# For now, lets just create the process needed with fastapi
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/add_manga")
async def add_manga(content:str, submission_confirmation:bool):
    """
    API that adds records to the database

    Args:
        content (str): URL of the manga link to be added
        submission_confirmation (bool): Additional param sent from frontend to confirm action

    Returns:
        _type_: _description_
    """
    ## Take in a URL string
    ## Do checks on the string
    ## Parse the string and do checks on the parsing
    ## If success, create the appropriate data structure
    ## Call stored procedure and pass in data to each one to populate tables
    if submission_confirmation:
        # Here we run a function to check if the record already exists in the database
        # By doing a link checkup and a simple name check
        # If the match for either, send a response back to the frontend saying "Record exists"
        # Then display the record that exists to the user
        # Give the user the option to then ovveride via another frontend-button, which sends a confirmation action
        # If confirmation action to override, we call update_manga api
        # If confirmation action to not override, we continue here

        if "success":
            return {"message": "Successfully added!"}
        
        return {"message": "Invalid URL!"}

@app.get("/api/v1/delete_manga")
async def delete_manga(content:str, submission_confirmation:bool):
    """
    API that deletes records from the database

    Args:
        content (str): URL of the manga link to be deleted
        submission_confirmation (bool): Additional param sent from frontend to confirm action

    Returns:
        _type_: _description_
    """
    if submission_confirmation:
        if "success":
            return {"message": "Successfully deleted!"}
        
        return {"message": "Invalid URL!"}

@app.get("/api/v1/update_manga")
async def update_manga(content:str, submission_confirmation:bool):
    """
    API that adds records to the database

    Args:
        content (str): URL of the manga link to be updated
        submission_confirmation (bool): Additional param sent from frontend to confirm action

    Returns:
        _type_: _description_
    """
    if submission_confirmation:
        if "success":
            return {"message": "Successfully updated!"}
        
        return {"message": "Invalid URL!"}