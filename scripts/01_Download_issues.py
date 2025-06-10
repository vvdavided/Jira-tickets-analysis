from jira import JIRA
import pickle


JIRA_URL = 'https://redacted.atlassian.net'
JIRA_USER = 'redacted'
JIRA_API_TOKEN = 'redacted'
JQL_QUERY = "project in (redacted) order by created desc"

start_at = 0
max_results = 100
limit = None

jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_USER, JIRA_API_TOKEN))

issues = []
total_fetched = 0

while True:
    if limit and total_fetched >= limit:
        break

    batch = jira.search_issues(
        jql_str=JQL_QUERY,
        startAt=start_at,
        maxResults=max_results
    )

    if not batch:
        break

    issues.extend(batch)
    fetched_count = len(batch)
    total_fetched += fetched_count
    start_at += fetched_count

    print(f"Fetched {fetched_count} issues, total so far: {total_fetched}")

    if fetched_count < max_results:
        break  # No more issues

print(f"Total issues fetched: {len(issues)}")


# Save issues
with open("data\raw\issues_jira_api.pkl", "wb") as f:
    pickle.dump(issues, f)

print("Issues saved in .pkl")




