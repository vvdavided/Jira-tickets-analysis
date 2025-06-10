import pickle


with open("data\raw\issues_development.pkl", "rb") as f1:
    issues1 = pickle.load(f1)


with open("data\raw\issues_support.pkl", "rb") as f2:
    issues2 = pickle.load(f2)

# Combine both lists
combined_issues = issues1 + issues2

# Save combined lists to new pickle file
with open("data\raw\combined_issues.pkl", "wb") as f_out:
    pickle.dump(combined_issues, f_out)

print(f"Combined {len(issues1)} + {len(issues2)} issues into 'combined_issues.pkl'")
