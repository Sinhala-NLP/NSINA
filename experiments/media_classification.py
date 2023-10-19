import pandas as pd

full = pd.read_json("/content/drive/MyDrive/NSINa.json")

# Number of samples to take from each category
sample_size = 10000


# Define a function to sub-sample from each category
def sub_sample(group):
    return group.sample(min(len(group), sample_size))


# Group the DataFrame by 'Category' and apply the sub-sampling function
subsampled_df = full.groupby('Source', group_keys=False).apply(sub_sample)

# Reset the index of the resulting DataFrame
subsampled_df = subsampled_df.reset_index(drop=True)

