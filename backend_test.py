import pandas as pd
import numpy as np 

df = pd.read_excel('Placement Sheet 2025-26(On Campus + Off Campus).xlsx')
print(df.head())
print(df.columns)
print(f"Total number of students placed = {len(df)}")
print(f"Total Number of companies visited the campus = {df['Company'].nunique()}")
print(f"Highest Package = {df['Package(LPA)'].max()}")
print(f"Average Package = {df['Package(LPA)'].mean()}")
percentplaced = (len(df)/420) *100
print(f"Percent of total students = {percentplaced}")
branch_group = df.groupby("Branch")
branch_stats = branch_group["Package(LPA)"].agg(["count","max","mean"])
print(branch_stats)
branch_stats["Placement %"] = (branch_stats["count"]/60)*100
print('\n')
print(branch_stats)
