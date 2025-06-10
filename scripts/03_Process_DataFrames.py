import pickle
import pandas as pd

# Import data
with open("data/raw/combined_issues.pkl", "rb") as f:
    issues = pickle.load(f)

issue_dicts = []

for issue in issues:
    issue_data = issue.raw
    issue_fields = issue_data.get("fields", {})
    
    issue_fields["id"] = issue_data.get("id")
    issue_fields["key"] = issue_data.get("key")

    issue_dicts.append(issue_fields)

df = pd.DataFrame(issue_dicts)

# Replace column names with more friendly names
fields_dict = pd.read_csv("data/processed/fields_dict.csv", usecols=['id','name'])
rename_map = dict(zip(fields_dict["id"], fields_dict["name"]))
df = df.rename(columns=rename_map)

# Only keep fields we're enterested in
df = df[['id','key','Summary','Description','Status','Priority','Created','Resolved','Resolution','Impact','Labels',
         'Project Number','Note','Linked Issues','Task Number','Assignee','Components','Reporter','Issue Type',
         'Work category','Client Name','Watchers','Updated','[CHART] Date of First Response','Comment','First Time Right',
         'Fix versions','Creator','OLA CNXT Team - Resolution Time','OLA CNXT Team - Response Time','Reopened','Time Spent',
         'Work Ratio','Requested Target Date','Attachment','Parent','Development','Time tracking']]

# Rename repeated columns
df.columns = [f"{col}_{i}" if list(df.columns).count(col) > 1 else col for i, col in enumerate(df.columns)]

# Transform JSON columns
df['Status'] = df['Status'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df['Priority'] = df['Priority'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df['Impact'] = df['Impact'].apply(lambda x: x['value'] if isinstance(x, dict) else None)
df['Assignee'] = df['Assignee'].apply(lambda x: x['accountId'] if isinstance(x, dict) else None)
df['Creator'] = df['Creator'].apply(lambda x: x['accountId'] if isinstance(x, dict) else None)
df['Resolution'] = df['Resolution'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df['Reporter'] = df['Reporter'].apply(lambda x: x['accountId'] if isinstance(x, dict) else None)
df['Issue Type'] = df['Issue Type'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df['Watchers'] = df['Watchers'].apply(lambda x: x['watchCount'] if isinstance(x, dict) else None)
df['Time tracking (time spent)'] = df['Time tracking'].apply(lambda x: x.get('timeSpent') if isinstance(x, dict) else None)
df['Client Name_20'] = df['Client Name_20'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
df['First Time Right'] = df['First Time Right'].apply(lambda x: x.get('value') if isinstance(x, dict) else None)
df["Components"] = df["Components"].apply(lambda x: [item.get("description", None) for item in x])
df["Fix versions"] = df["Fix versions"].apply(lambda x: [item.get("releaseDate", None) for item in x])

df['Time tracking (remaining estimate)'] = df['Time tracking'].apply(lambda x: x.get('remainingEstimate') if isinstance(x, dict) else None)
df['Time tracking (remaining estimate)'] = df['Time tracking (remaining estimate)'].replace('0h', None)
df = df.drop(columns=['Time tracking']) # Was broken down to 2 columns, no longer useful

# Keep only Closed issues
df = df[df['Status'] == 'Closed']

# Reoder columns
cols_start = ["id", "key", "Summary", "Description", "Status", "Priority", "Created", "Resolved"]
cols_start = [col for col in cols_start if col in df.columns]
others = [col for col in df.columns if col not in cols_start]
df = df[cols_start + others]

# Assign types
df['Created'] = pd.to_datetime(df['Created'], utc=True)
df['Created'] = df['Created'].dt.tz_convert('America/Chicago')
df['Resolved'] = pd.to_datetime(df['Resolved'], utc=True)
df['Resolved'] = df['Resolved'].dt.tz_convert('America/Chicago')
df['Updated'] = pd.to_datetime(df['Updated'], utc=True)
df['Updated'] = df['Updated'].dt.tz_convert('America/Chicago')
df['[CHART] Date of First Response'] = pd.to_datetime(df['[CHART] Date of First Response'], utc=True)
df['[CHART] Date of First Response'] = df['[CHART] Date of First Response'].dt.tz_convert('America/Chicago')
df['Requested Target Date'] = pd.to_datetime(df['Requested Target Date'])



## Support and development dataframes
df_sprt = df[df["key"].str.startswith("CNSD")]
df_dev = df[df["key"].str.startswith("CNXT")]

# Drop unused Jira fields
df_sprt = df_sprt.drop(columns = df_sprt.columns[df_sprt.isna().all()])
df_dev = df_dev.drop(columns = df_dev.columns[df_dev.isna().all()])

# Support
df_sprt = df_sprt.drop(columns=['Fix versions','Components'])
df_sprt = df_sprt.rename(columns={'Client Name_20': 'Client Name'})
df_sprt['Reopened'] = df_sprt['Reopened'].fillna(0)
df_sprt['Client Name'] = df_sprt.apply(
    lambda row: row['Client Name_21'] if pd.isna(row['Client Name']) or row['Client Name'] == 'Other' else row['Client Name'],
    axis=1
)
df_sprt = df_sprt.drop(columns=['Client Name_21'])

# Development
df_dev = df_dev.drop(columns=['Client Name_20','Client Name_21'])

#Rename project names
df_sprt['key'] = df_sprt['key'].str.replace('CNSD', 'SPRT')
df_dev['key'] = df_dev['key'].str.replace('CNXT', 'DEV')

# Save dataframes for later stages
with open("data/processed/df_sprt.pkl", "wb") as f_out:
    pickle.dump(df_sprt, f_out)

with open("data/processed/df_dev.pkl", "wb") as f_out:
    pickle.dump(df_dev, f_out)


# Status changelog
status_changelog = pd.read_excel("data/raw/status_changelog.xlsx")
# Drop CRE issues
status_changelog = status_changelog[~status_changelog['Key'].str.startswith('CRE')]
# Only keeping columns we need
status_changelog= status_changelog[['Key','Change Start','Time In This State [m]','Status']]
# Only keep issues that have been closed
status_changelog = status_changelog.groupby('Key').filter(lambda group: 'Closed' in group['Status'].values)
# Sorting
status_changelog = status_changelog.sort_values(by=['Key', 'Change Start'], ascending=[True, True])
# Fixing data types
status_changelog['Change Start'] = pd.to_datetime(status_changelog['Change Start'])
status_changelog['Time In This State [m]'] = status_changelog['Time In This State [m]'].astype(str).str.replace('m', '', regex=False)
status_changelog['Time In This State [m]'] = status_changelog['Time In This State [m]'].astype(int)

# Save Dataframe
with open("data/processed/status_changelog.pkl", "wb") as f_out:
    pickle.dump(status_changelog, f_out)