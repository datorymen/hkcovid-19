import streamlit as st
import pandas as pd

df = pd.read_csv('building_list_chi.csv')
# df['個案最後到訪日期'] = pd.to_datetime(df['個案最後到訪日期'])
df['曾到訪個案數量'] = df['相關個案編號'].str.split().str.len()
df = df[df['個案最後到訪日期'].notnull()]

st.title('你附近有個案到訪過的大廈嗎？')

# st.header('過去14日大廈數量最多的3個區：')

df1 = df.groupby('地區').agg('count').reset_index()
df1 = df1[['地區', '大廈名單']]
df1.columns = ['地區', '14天内的大廈总數量']
df1 = df1.sort_values('14天内的大廈总數量', ascending=False).reset_index(drop=True)
df1['排名'] = df1.index + 1
df1 = df1[['排名', '地區', '14天内的大廈总數量']]

# top_area_1 = df1.iloc[0, 1]
# top_area_1_number = df1.iloc[0, 2]
# top_area_2 = df1.iloc[1, 1]
# top_area_2_number = df1.iloc[1, 2]
# top_area_3 = df1.iloc[2, 1]
# top_area_3_number = df1.iloc[2, 2]
#
# col1, col2, col3 = st.columns(3)
# col1.metric(top_area_1, top_area_1_number)
# col2.metric(top_area_2, top_area_2_number)
# col3.metric(top_area_3, top_area_3_number)

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

# col4, col5, col6 = st.columns([1, 2, 3])
# with col4:
#     st.write('排名')
#     for i in range(0, 18):
#         # st.markdown("""
#         # <style>
#         # .big-font {
#         #     font-size:100px !important;
#         # }
#         # </style>
#         # """, unsafe_allow_html=True)
#         st.write(df1.iloc[i, 0])
#

#
# with col5:
#     st.write('地區')
#     for i in range(0, 18):
#         # link = district
#         area = df1.iloc[i, 1]
#         st.write(area)
#
#         # st.markdown([str(area)](link)', unsafe_allow_html=True)
#
#
# with col6:
#     st.write('14天内個案到訪過的大廈數量')
#     for i in range(0, 18):
#         st.write(df1.iloc[i, 2])



area_list = (df1['地區'].values)
option = st.selectbox(
     '選擇地區以查看大廈詳細名稱', area_list)

# st.write('You selected:', option)

df2 = df[df['地區']== option]
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
數據來自衛生署。每天清晨6點前更新。\n
希望這個網站可以幫到大家。\n
希望香港的疫情早日結束！\n 
如果發現問題或者有任何建議，請發郵件到: \n
number1datascientist(at)gmail點com
''')