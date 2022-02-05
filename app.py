import streamlit as st
import pandas as pd
import datetime
import pytz
import pdfplumber




today = datetime.datetime.today().strftime('%Y-%m-%d')
today_time = datetime.datetime.today()
today_str = today_time.strftime("%Y-%m-%d %H:%M")
yesterday_time = (today_time - datetime.timedelta(days=1))
yesterday_str = yesterday_time.strftime("%m" + "月" + "%d" + "日")
# now = (datetime.datetime.today() + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")
now_time = (datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')))
now_str = now_time.strftime("%Y-%m-%d %H:%M")
days_14_ago_time = today_time - datetime.timedelta(days=14)
days_14_ago_str = days_14_ago_time.strftime("%m" + "月" + "%d" + "日")

days_14_ago = str(today_time - datetime.timedelta(days=14))


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

st.header('香港COVID-19小工具')
st.write('作者：datory.men')

selection = st.radio(
          '請選擇功能：', ['個案曾經到訪過的大廈', '各區流動採樣站'])

if selection == '個案曾經到訪過的大廈':

     df = pd.read_csv('http://www.chp.gov.hk/files/misc/building_list_chi.csv')
     df['個案最後到訪日期'] = pd.to_datetime(df['個案最後到訪日期'], format="%d/%m/%Y")
     df = df[df['個案最後到訪日期'] >= days_14_ago]
     df['曾到訪個案數量'] = df['相關個案編號'].str.split().str.len()
     df = df[df['個案最後到訪日期'].notnull()]

     # st.write('個案曾經到訪過的大廈')
     st.write('信息更新時間：' + now_str)
     st.write('過去14日範圍是指' + days_14_ago_str + ' 到 ' + yesterday_str)

     df1 = df.groupby('地區').agg('count').reset_index()
     df1 = df1[['地區', '大廈名單']]
     df1.columns = ['地區', '14天内個案曾經到訪過的大廈总數量']
     df1 = df1.sort_values('14天内個案曾經到訪過的大廈总數量', ascending=False).reset_index(drop=True)
     df1['排名'] = df1.index + 1
     df1 = df1[['排名', '地區', '14天内個案曾經到訪過的大廈总數量']]


     area_list = (df1['地區'].values)
     option = st.selectbox(
          '選擇地區以查看大廈詳細名稱（按照最新的到訪日期排列）(頁面底部有18區大廈數量排名)', area_list)


     df2 = df[df['地區'] == option]
     df2 = df2[['地區', '大廈名單', '個案最後到訪日期', '曾到訪個案數量']]
     df2 = df2.sort_values('個案最後到訪日期', ascending=False)
     df2 = df2.reset_index(drop=True)
     df2['排名'] = df2.index + 1
     df2 = df2[['排名', '地區', '大廈名單', '個案最後到訪日期', '曾到訪個案數量']]
     df2['個案最後到訪日期'] = df2['個案最後到訪日期'].astype('str')
     df2['地區名稱'] = df2['地區']
     df2 = df2.drop('地區', axis=1)
     df2 = df2[['排名', '地區名稱', '大廈名單', '個案最後到訪日期', '曾到訪個案數量']]


     st.table(df2)

     st.header('18區大廈數量排名：')

     st.table(df1)

     st.caption('數據來自衛生署。刷新頁面即可更新。')



if selection == '各區流動採樣站':


     # st.write('各區流動採樣站')
     st.write('信息更新日期：' + today)
     # st.write('正在開發中。。。')
     pdf = pdfplumber.open(today + '-a-mscs.pdf')
     pages = len(pdf.pages)

     df_pdf = pd.DataFrame()
     for i in range(1, pages):
          first_page = pdf.pages[i]
          table = first_page.extract_table()
          table_df = pd.DataFrame(table)
          df_pdf = df_pdf.append(table_df)

     df_pdf.rename(columns=df_pdf.iloc[0], inplace=True)
     df_pdf.drop(df_pdf.index[0], inplace=True)
     df_pdf.columns = ['地區', '流動採樣站',
                       '開放日期', '服務時間',
                       '服務對象']
     df_pdf = df_pdf[['地區', '流動採樣站',
                      '開放日期', '服務時間']]
     df_pdf = df_pdf[df_pdf['開放日期'].notnull()]
     df_pdf = df_pdf.fillna(method='ffill')

     st.markdown(""" <style> .font {
     font-size:500px;} 
     </style> """, unsafe_allow_html=True)

     # st.write('test')
     st.table(df_pdf)
     st.caption('數據來自衛生署。每日更新。')

st.caption('''
如果發現問題或者有任何建議，請發郵件到: \n
number1datascientist(at)gmail點com \n
\n
''')

st.write('祝福香港早日清零！')

