#%% Import data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_dev = pd.read_pickle("../data/processed/df_dev.pkl")
df_dev['summary_tags'] = df_dev['Summary'].str.findall(r'\[([^\]]+)\]')

# Categorize dev tickets
from collections import Counter
counter = Counter(df_dev['summary_tags'].sum())


#%% Created dev tickets per Year by Work Category
dev_year = df_dev[['Created','Priority']].copy()
dev_year['Year'] = dev_year['Created'].dt.year
dev_year_grouped = dev_year.groupby(['Year','Priority']).size().unstack(fill_value=0)

ax = dev_year_grouped.plot(
    kind='bar',
    stacked=True
)

plt.title("Created development tickets per Year by Priority")
plt.xlabel("Year")
plt.ylabel("Number of Tickets")
plt.legend(title="Priority")
plt.tight_layout()
plt.show()

#%% CNSD Created tickets per Year-Month by Work Category

df_sprt['Year-Month'] = df_sprt['Created'].dt.to_period('M').astype(str)


ticket_counts = df_sprt.groupby(['Year-Month', 'Work category']).size().unstack(fill_value=0)


ticket_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='crest')

plt.title('Created support tickets per Year-Month by Work Category')
plt.xlabel('Year-Month')
plt.ylabel('Number of Tickets')
plt.xticks(rotation=45)
plt.legend(title='Work Category')
#plt.tight_layout()
plt.show()

#%% 

df_dev['Weekday'] = df_dev['Created'].dt.day_name()


order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


grouped = df_dev.groupby(['Weekday']).size().unstack(fill_value=0)
grouped = grouped.reindex(order)

grouped.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='crest')

plt.title("Support tickets created by Day of the Week and Work Category", fontsize=14)
plt.xlabel("Day of the Week")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)
plt.legend(title="Work Category")
plt.tight_layout()
plt.show()

#%% Hour of the day
df_dev['Created Hour'] = df_dev['Created'].dt.hour

# group by hour and Work category
count = df_dev['Created Hour'].value_counts().sort_index()



hour_labels = [f"{h%12 or 12} {'AM' if h < 12 else 'PM'}" for h in grouped.index]


count.plot(x='Created Hour',y='count', kind='bar', stacked=True, colormap='crest')

plt.title("Created support tickets by Hour of the Day and Work Category")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Tickets")
plt.xticks(rotation=45)
plt.legend(title="Work Category")
plt.tight_layout()
plt.show()


#%%


