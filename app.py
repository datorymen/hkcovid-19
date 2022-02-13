import streamlit as st
import pandas as pd
import datetime
import pytz
import pdfplumber
import numpy as np

st.set_page_config(layout='wide')


now_time = (datetime.datetime.now(pytz.timezone('Asia/Hong_Kong')))
now_str = now_time.strftime("%Y-%m-%d %H:%M")

today_time = datetime.datetime.date(now_time)
today = today_time.strftime('%Y-%m-%d')
today_str = today_time.strftime("%Y-%m-%d %H:%M")

yesterday_time = (today_time - datetime.timedelta(days=1))
yesterday = yesterday_time.strftime('%Y-%m-%d')
yesterday_str = yesterday_time.strftime("%m" + "月" + "%d" + "日")

days_14_ago_time = today_time - datetime.timedelta(days=15)
days_14_ago_str = days_14_ago_time.strftime("%m" + "月" + "%d" + "日")
days_14_ago = str(days_14_ago_time)


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.header('香港COVID-19小工具')
st.write('作者：datory.men')
st.write('祝福香港早日清零！')
# st.write(today)

# try:
# selection = st.radio('請選擇功能：', ['各區流動採樣站', '個案曾經到訪過的大廈', '個案曾居住的住宅大廈', '排名'])
selection = st.radio('請選擇功能：', ['各區流動採樣站', '個案曾經到訪過的大廈'])

df = pd.read_csv('http://www.chp.gov.hk/files/misc/building_list_chi.csv')
df['個案最後到訪日期'] = pd.to_datetime(df['個案最後到訪日期'], format="%d/%m/%Y")
# df = df[df['個案最後到訪日期'] >= days_14_ago]
# df['曾到訪個案數量'] = df['相關個案編號'].str.split().str.len()
df = df[df['個案最後到訪日期'].notnull()]

df1 = df.groupby('地區').agg('count').reset_index()
df1 = df1[['地區', '大廈名單']]
df1.columns = ['地區', '14天内個案曾經到訪過的大廈总數量']
df1 = df1.sort_values('14天内個案曾經到訪過的大廈总數量', ascending=False).reset_index(drop=True)
df1['排名'] = df1.index + 1
df1 = df1[['排名', '地區', '14天内個案曾經到訪過的大廈总數量']]

df_living = pd.read_csv('http://www.chp.gov.hk/files/misc/building_list_chi.csv')
df_living = df_living[df_living['個案最後到訪日期'].notnull()]
df_living = df_living[['地區', '大廈名單', '相關個案編號']]
df_living.columns = ['地區', '大廈名單', '個案編號']
# df_living['個案編號'] = df_living['個案編號'].astype('int')

df_all = pd.read_csv('http://www.chp.gov.hk/files/misc/enhanced_sur_covid_19_chi.csv')
df_all = df_all[['個案編號', '報告日期', '性別', '年齡', '個案狀況*']]
df_all['報告日期'] = pd.to_datetime(df_all['報告日期'], format="%d/%m/%Y").dt.strftime('%Y-%m-%d')

df_cases = pd.merge(df_living, df_all, how='left', on='個案編號')

df4 = df_cases.groupby('地區').agg('count').reset_index()
df4 = df4[['地區', '大廈名單']]
df4.columns = ['地區', '14天内的個案居住的大廈总數量']
df4 = df4.sort_values('14天内的個案居住的大廈总數量', ascending=False).reset_index(drop=True)
df4['排名'] = df4.index + 1
df4 = df4[['排名', '地區', '14天内的個案居住的大廈总數量']]


if selection == '各區流動採樣站':

     pdf = pdfplumber.open(today + '-a-mscs.pdf')
     # pdf = pdfplumber.open('2022-02-09-b-mscs.pdf')
     st.write('信息更新日期：' + today)

     # try:
     #      pdf = pdfplumber.open(today + '-a-mscs.pdf')
     #      st.write('信息更新日期：' + today)
     # except:
     #      pdf = pdfplumber.open(yesterday + '-b-mscs.pdf')
     #      st.write('信息更新日期：' + today)
     # else:
     #      pdf = pdfplumber.open(yesterday + '-a-mscs.pdf')
     #      st.write('信息更新日期：' + yesterday)

     pages = len(pdf.pages)

     df_pdf = pd.DataFrame()
     for i in range(1, pages):
          first_page = pdf.pages[i]
          table = first_page.extract_table()
          table_df = pd.DataFrame(table)
          table_df.columns = ['地區名稱', '流動採樣站',
                              '開放日期', '服務時間',
                              '服務對象']
          df_pdf = df_pdf.append(table_df, ignore_index=True)

     df_pdf['地區名稱'] = df_pdf['地區名稱'].str.replace(r'[a-zA-Z0-9  ()\n&,-/]+', '', regex=True)
     df_pdf = df_pdf[~df_pdf['地區名稱'].isin(['地區', '港島', '九龍', '新界'])]
     df_pdf = df_pdf.replace(r'', np.nan, regex=True)
     df_pdf = df_pdf.fillna(method='ffill')
     df_pdf = df_pdf[['地區名稱', '流動採樣站',
                      '開放日期', '服務時間']]

     df_pdf['地區名稱'] = df_pdf['地區名稱'].str.replace(r'[a-zA-Z0-9  ()\n&,-/]+', '', regex=True)
     df_pdf['流動採樣站'] = df_pdf['流動採樣站'].str.replace(r'[a-zA-Z\n(),&]', '', regex=True).str.replace(r'(\d+)\D*$', '',
                                                                                                   regex=True)
     df_pdf['開放日期'] = df_pdf['開放日期'].str.replace(r'[a-zA-Z()&,/\n]', '', regex=True)
     df_pdf['服務時間'] = df_pdf['服務時間'].str.replace(r'[\n]', '', regex=True).str.replace('Monday and Friday', '')

     df_pdf = df_pdf.replace(r'', np.nan, regex=True)
     df_pdf = df_pdf.fillna(method='ffill')
     df_pdf = df_pdf.reset_index(drop=True)

     # st.markdown(""" <style> .font {
     # font-size:500px;}
     # </style> """, unsafe_allow_html=True)
     #
     # area_list = (df_pdf['地區名稱'].unique())
     # option = st.selectbox(
     #      '選擇地區', area_list)
     #
     # df_area = df_pdf[df_pdf['地區名稱'] == option]
     st.table(df_pdf)

     st.caption('數據來自衛生署。每日更新。')


if selection == '個案曾經到訪過的大廈':

     st.write('信息更新時間：' + now_str)

     area_list = (df1['地區'].values)
     option = st.selectbox(
          '選擇地區以查看大廈詳細名稱（按照最新的到訪日期排列）', area_list)


     df2 = df[df['地區'] == option]
     # df2 = df2[['地區', '大廈名單', '個案最後到訪日期', '曾到訪個案數量']]
     df2 = df2[['地區', '大廈名單', '個案最後到訪日期']]
     df2 = df2.sort_values('個案最後到訪日期', ascending=False)
     df2 = df2.reset_index(drop=True)
     df2['排名'] = df2.index + 1
     df2 = df2[['排名', '地區', '大廈名單', '個案最後到訪日期']]
     df2['個案最後到訪日期'] = df2['個案最後到訪日期'].astype('str')
     df2['地區名稱'] = df2['地區']
     df2 = df2.drop('地區', axis=1)
     df2 = df2[['排名', '地區名稱', '大廈名單', '個案最後到訪日期']]
     df2.columns = ['排序', '地區名稱', '大廈名單', '個案最後到訪日期']


     st.table(df2)



# if selection == '個案曾居住的住宅大廈':
#
#      st.write('信息更新時間：' + now_str)
#
#
#      area_list = (df4['地區'].values)
#      option = st.selectbox(
#           '選擇地區以查看大廈詳細名稱（按照最新的報告日期排列）', area_list)
#
#
#      df3 = df_cases[df_cases['地區'] == option]
#      df3 = df3.sort_values('個案編號', ascending=False)
#      df3 = df3.reset_index(drop=True)
#
#      st.table(df3)
#
#      st.caption('數據來自衛生署。刷新頁面即可更新。')
#
# if selection == '排名':
#      st.header('18區到訪大廈數量排名：')
#      st.table(df1)
#
#      st.header('18區居住大廈數量排名：')
#      st.table(df4)
#
#
#      st.caption('數據來自衛生署。刷新頁面即可更新。')
# # except:
# #      st.write(today + ' 數據文件出現問題。官網更新後會自動顯示。')

st.caption('''
如果發現問題或者有任何建議，請發郵件到: \n
number1datascientist(at)gmail點com \n
\n
''')


