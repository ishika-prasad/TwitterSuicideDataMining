import pandas as pd

dfs = pd.read_excel('sentiment212.xlsx')
new_df = dfs.dropna()

text_list = new_df['sentiment'].tolist()

indices_neutral = [i for i, x in enumerate(text_list) if x == 0]
indices_positive = [i for i, x in enumerate(text_list) if x == 1]
indices_negative = [i for i, x in enumerate(text_list) if x == -1]


percent_neutral = (len(indices_neutral) / len(text_list)) * 100
print("Neutral Tweets: ", round(percent_neutral, 2), "%")
percent_positive = (len(indices_positive) / len(text_list)) * 100
print("Positive Tweets: ", round(percent_positive, 2), "%")
percent_negative = (len(indices_negative) / len(text_list)) * 100
print("Negative Tweets: ", round(percent_negative, 2), "%")


