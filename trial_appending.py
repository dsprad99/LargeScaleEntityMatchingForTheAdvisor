import pandas as pd

'''
@breif: Script that append two CSV files together. Used specifically when wanting to append together two trials where the first one
filters out all of the papers that have already been matched in the second trial so that all the new files in the second trial will never 
have matched before. Therefore with a smaller hashmap of k-mers to query we can run it at higher accuracy thresholds without sacraficing as much
runtime.
'''

# Read the existing files
matched_unmatched_df = pd.read_csv("total_dblp_to_mag_rerun_trial3.csv")
mag_to_dblp_query_total_df = pd.read_csv("mag_to_dblp_query_total_trial2.csv")

# Check if mag_id in matched_unmatched_papers_trial1.csv is not in mag_to_dblp_query_total_trial1.csv
new_rows = matched_unmatched_df[~matched_unmatched_df['candidate_mag_id'].isin(mag_to_dblp_query_total_df['mag_id'])]

# Filter and select only the required columns
new_rows = new_rows[['candidate_mag_id', 'candidate_dblp_id','candidate_paper_title']]

# Rename columns for consistency
new_rows.columns = ['mag_id', 'best_candidate_dblp_id','candidate_title']

# Append the new rows to mag_to_dblp_query_total_trial1.csv
if not new_rows.empty:
    mag_to_dblp_query_total_df = pd.concat([mag_to_dblp_query_total_df, new_rows])

    # Write the updated dataframe back to mag_to_dblp_query_total_trial1.csv
    mag_to_dblp_query_total_df.to_csv("mag_to_dblp_query_total_trial3.csv", index=False)
    print("New rows appended successfully.")
else:
    print("No new rows to append.")



