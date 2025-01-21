import pandas as pd

p_df = pd.read_csv("performers.csv").drop(["Unnamed: 0"], axis=1)
p_df.columns = ["Performer", "IAFD Link", "Career scene #"]
print(p_df.head())

p_df["IAFD Link"] = p_df["IAFD Link"].apply(
    lambda link: f'<a href="{link}" target="_blank">{link}</a>'
)

print(p_df.head())

p_df.to_csv("performers_html.csv")