import streamlit as st
import pandas as pd
import datetime


today = datetime.date.today()
yesterday = (today - datetime.timedelta(days=1) + datetime.timedelta(hours=8)).strftime("%m-%d")
now = (datetime.datetime.today() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
days_14_ago = str(today - datetime.timedelta(days=14))




df = pd.read_csv('http://www.chp.gov.hk/files/misc/building_list_chi.csv')
df['個案最後到訪日期'] = pd.to_datetime(df['個案最後到訪日期'], format="%d/%m/%Y")
df = df[df['個案最後到訪日期'] >= days_14_ago]
df['曾到訪個案數量'] = df['相關個案編號'].str.split().str.len()
df = df[df['個案最後到訪日期'].notnull()]

st.title('你附近有個案到訪過的大廈嗎？')
st.write('數據更新時間：' + now)
st.write('過去14日：' + (today - datetime. timedelta(days=14) + datetime.timedelta(hours=8)).strftime("%m-%d") + ' 到 ' + yesterday)

df1 = df.groupby('地區').agg('count').reset_index()
df1 = df1[['地區', '大廈名單']]
df1.columns = ['地區', '14天内的大廈总數量']
df1 = df1.sort_values('14天内的大廈总數量', ascending=False).reset_index(drop=True)
df1['排名'] = df1.index + 1
df1 = df1[['排名', '地區', '14天内的大廈总數量']]


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# Display a static table

st.header('18區個案到訪過的大廈數量如下：')

st.table(df1)




area_list = (df1['地區'].values)
option = st.selectbox(
     '選擇地區以查看大廈詳細名稱', area_list)


df2 = df[df['地區'] == option]
df2 = df2[['地區', '大廈名單', '個案最後到訪日期', '曾到訪個案數量']]
df2 = df2.sort_values('曾到訪個案數量', ascending=False)
df2 = df2.reset_index(drop=True)
df2['排名'] = df2.index + 1
df2 = df2[['排名', '地區', '大廈名單', '個案最後到訪日期', '曾到訪個案數量']]
df2['個案最後到訪日期'] = df2['個案最後到訪日期'].astype('str')
df2['地區名稱'] = df2['地區']
df2 = df2.drop('地區', axis=1)
df2 = df2[['排名', '地區名稱', '大廈名單', '個案最後到訪日期', '曾到訪個案數量']]


st.table(df2)

st.caption('''
數據來自衛生署。刷新頁面即可更新。\n
\n
如果發現問題或者有任何建議，請發郵件到: \n
number1datascientist(at)gmail點com
''')

st.write('datory.men')
