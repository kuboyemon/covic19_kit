#ライブラリのインポート
import pandas as pd
import openpyxl
import requests as req
from bs4 import BeautifulSoup

#スクレイピングの実行、ベースとなるdfの作成
url="https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000082537_00001.html"
res=req.get(url)
soup=BeautifulSoup(res.text,'html.parser')

result = soup.select("a[href]")

link_list =[]
for link in result:
    href = link.get("href")
    link_list.append(href)

xlsx_list = [temp for temp in link_list if temp.endswith('xlsx')]
url_covic_xlsx='https://www.mhlw.go.jp'+f'{xlsx_list[0]}'

df=pd.read_excel(url_covic_xlsx)

df_tochigi=df[df['都道府県名']=='栃木県']
df_tochigi.reset_index(drop=True,inplace=True)

#アプリ部分の作成のためのライブラリインポート
import streamlit as st
import streamlit.components.v1 as stc

st.title('医療用検査キット取り扱い薬局検索システム')
st.write('元データ掲載元')
st.write(url)
city=st.selectbox(
  '検索したい市町を選択',
  ('すべて','宇都宮市','足利市','栃木市','佐野市','鹿沼市',
    '日光市','小山市','真岡市','大田原市','矢板市','那須塩原市',
    'さくら市','那須烏山市','下野市',
    '上三川町','益子町','茂木町','市貝町',
    '芳賀町','壬生町','野木町','塩谷町','高根沢町','那須町','那珂川町')
)
if city=='すべて':
  df=df_tochigi
else:
  df=df_tochigi[df_tochigi['所在地'].str.contains(city)]
  df.reset_index(drop=True,inplace=True)

st.dataframe(df[['薬局名称','所在地']])
st.write('拠点数:'+str(len(df)))

df_index=df.index.values

num=st.selectbox('番号を選択して詳細を表示',
(i for i in df_index)
)
num=int(num)
st.error('市町に取り扱い薬局が存在しません')

if num==None:
    st.write('番号を入力してください。')
else:
    st.write('###### 薬局名称')
    st.write(df.loc[num,'薬局名称'])
    st.write('###### 所在地')
    link='[{}](https://www.google.co.jp/maps/place/{})'.format(df.loc[num,'所在地'],df.loc[num,'所在地'])
    st.markdown(link, unsafe_allow_html=True)
    st.write('###### 電話番号')
    tel_num=df.loc[num,'電話番号']
    st.write('※長押しで電話発信可能')
    stc.html("<a href='tel:{}'>{}</a>".format(tel_num,tel_num)) 
st.write('無料検査拠点検索システムに戻る')
st.write('https://kuboyemon-covic19-pdf-covic19pdf-63n9sa.streamlitapp.com/')

st.write('Ver.1.0     2022.8.5 公開開始')
st.write('Copyright © kuboyemon at Yaita PS from Tochigi PD')
