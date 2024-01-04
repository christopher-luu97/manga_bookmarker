System Process

1. Backend CRON job calls Python script to scrape data into database
2. Database gets updated from CRON web scrape
3. User gets notified of latest changes in email
4. User browses to website and logs in
5. User can now observes latest changes

Project Workflow:

1. Track features, issues etc. using Github projects
2. Names are for example frontend-epic-0001-X where X defines what the epic is
   - The epic in the comments should identify what features should be associated
   - We can then break down the associated features into their own tickets
3. Features are tied to an epic id e.g. frontend-epic-0001-X-submit-button
   - These features are in the comments of the epic
4. Make changes in code and update the ticket to point to the branch and/or PR
5. Resolve tickets / update them as we chug along

Git Workflow:

1. Create a branch that takes in an issue name e.g. git checkout -b frontend-epic-0002-feature-0001-scrollable-list
2. Make edits in this branch
3. Commit to this branch
4. Push changes to this remote e.g. git push origin frontend-epic-0002-feature-0001-scrollable-list
5. Create pull request in github
6. Review
7. Merge if okay
8. Resolve ticket in github projects and add comment pointing to the PR of interest

## DB Schema to be built

<div align="center">
    <img src="/assets/images/20231222_db_schema_v1.PNG?raw=true"</img> 
</div>

## Fixes

### API Stuff

- Created test_app.py as the test API for the following processes below:
- Frontend Modal currently submits entire table which is okay, we just need a way to confirm the additions and deletions when sent to API
- Test DB Insertions
- Setup API to accept and parse specific data format which can then be passed into the processing + database operations
- Database tables should have history so when we inner join on the new records, we maintain a history of everything for rollback
- Frontend modal reads from DB specific columns and data
  - We need to also read in the ID but hide it from the user, this will be used for the user
    - When sent to API, we can then filter on missing ID's or NA ID's these we know will remove (missing) or add new (NA ID)
      - This also will update all other records if needed
        - So there is no need for an "Delete" or "Update" API. We only need a single process
