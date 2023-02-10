
pip install requests
import requests 
import json
import pandas as pd

new_df = pd.DataFrame()
for i in range(1,29999,1000):
    url = requests.get('http://openapi.seoul.go.kr:8088/654a41474d6b7975313230526e73534d/json/BukChonInOutPeopleInfo/{}/{}/'.format(i, i+999))
    data = (url.text)
    dict_data = json.loads(data)
    df = pd.DataFrame(dict_data['BukChonInOutPeopleInfo']['row'])
    new_df = pd.concat([new_df, df])




new_df['ENDTIME'] = pd.to_datetime(new_df['ENDTIME'])
new_df['MONTH'] = new_df['ENDTIME'].dt.month
new_df.head()


new_df["PASS"] = new_df['INCOUNT'] + new_df['OUTCOUNT']
new_df.groupby("MONTH")["PASS"].mean()


import seaborn as sns
sns.barplot(data=new_df, x='MONTH', y='PASS')


new_df['Day'] = [num_to_day[k] for k in new_df['ENDTIME'].dt.dayofweek] ## 요일 칼럼
new_df1 = new_df.groupby('Day')['PASS'].aggregate(['max','min','mean'])
new_df1 = new_df1.reset_index()

sns.barplot(data = new_df1, x= 'Day', y = 'mean')

filter = new_df["ENDTIME"].dt.hour < 4
filter2 = (new_df["ENDTIME"].dt.hour <= 8) & (new_df["ENDTIME"].dt.hour > 4)
filter3 = (new_df["ENDTIME"].dt.hour <= 12) & (new_df["ENDTIME"].dt.hour > 8)
filter4 = (new_df["ENDTIME"].dt.hour <= 16) & (new_df["ENDTIME"].dt.hour > 12)
filter5 = (new_df["ENDTIME"].dt.hour <= 20) & (new_df["ENDTIME"].dt.hour > 16)
filter6 = (new_df["ENDTIME"].dt.hour <= 24) & (new_df["ENDTIME"].dt.hour > 20)

print(new_df.loc[filter, "PASS"].mean())
print(new_df.loc[filter2, "PASS"].mean())
print(new_df.loc[filter3, "PASS"].mean())
print(new_df.loc[filter4, "PASS"].mean())
print(new_df.loc[filter5, "PASS"].mean())
print(new_df.loc[filter6, "PASS"].mean())

new_df['DEVICENAME'].value_counts()

df_sorted = new_df.sort_values(by='PASS' ,ascending=False)
df_sorted = df_sorted.head(100)


new_df['INPASS'] = new_df['INCOUNT'] - new_df['OUTCOUNT']
new_df['OUTPASS'] = new_df['OUTCOUNT'] - new_df['INCOUNT']






