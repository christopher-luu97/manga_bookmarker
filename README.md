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

- Do checks on data being inserted to handle duplicate records based off of string distance on name so we don't get dupes ## COMPLETE
- Add frontend loading screens when waiting for API responses ## COMPLETE
- Test CRON jobs
- Add thumbnail searching for mangakakalot ## COMPLETE
- Add mangakakalot into the backend scraping mechanism ## COMPLETE
- Add website checks for additional data to see if they are in the supported websites.
