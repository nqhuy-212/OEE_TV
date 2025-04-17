import streamlit as st 
from load_data import get_data

st.set_page_config(layout= 'wide',page_title="OEE",page_icon="logo.png",)
st.logo("logo.png",size= 'large')
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        margin-top: 200 px;
        color: 'rgb(255,255,255)';
        font-size : 68px;
    }
    div.block-container{padding-top:1.5rem};
    </style>
    """,
    unsafe_allow_html=True
)

#---PAGE SETUP---
cutter_2u05 = st.Page(
    page="views/cutter_2u05.py",
    title= "Auto cutter 2U05"
)
cutter_2u06 = st.Page(
    page="views/cutter_2u06.py",
    title= "Auto cutter 2U06"
)
cutter_2u07 = st.Page(
    page="views/cutter_2u07.py",
    title= "Auto cutter 2U07"
)
cutter_2u08 = st.Page(
    page="views/cutter_2u08.py",
    title= "Auto cutter 2U08"
)
cutter_2u09 = st.Page(
    page="views/cutter_2u09.py",
    title= "Auto cutter 2U09"
)
cutter_2u10 = st.Page(
    page="views/cutter_2u10.py",
    title= "Auto cutter 2U10"
)
cutter_2u11 = st.Page(
    page="views/cutter_2u11.py",
    title= "Auto cutter 2U11"
)
cutter_2u55 = st.Page(
    page="views/cutter_2u55.py",
    title= "Auto cutter 2U55"
)
cutter_2u56 = st.Page(
    page="views/cutter_2u56.py",
    title= "Auto cutter 2U56"
)
cutter_2u57 = st.Page(
    page="views/cutter_2u57.py",
    title= "Auto cutter 2U57"
)
cutter_2u58 = st.Page(
    page="views/cutter_2u58.py",
    title= "Auto cutter 2U58"
)
cutter_2u81 = st.Page(
    page="views/cutter_2u81.py",
    title= "Auto cutter 2U81"
)
cutter_2u82 = st.Page(
    page="views/cutter_2u82.py",
    title= "Auto cutter 2U82"
)

pg = st.navigation(pages=[cutter_2u05,cutter_2u06,cutter_2u07,cutter_2u08,cutter_2u09,cutter_2u10,cutter_2u11,cutter_2u55,cutter_2u56,cutter_2u57,cutter_2u58,cutter_2u81,cutter_2u82])   
pg.run()




