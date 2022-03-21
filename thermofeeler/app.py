import streamlit as st
import numpy as np
import pandas as pd
import time

from thermofeeler.predict import predict_query

st.set_page_config(page_title="ThermoFeeler", page_icon="🌡",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed

# st.markdown(
#         """
#         <style>
# @font-face {
#   font-family: 'Tangerine';
#   font-style: normal;
#   src: url(https://fonts.gstatic.com/s/tangerine/v12/IurY6Y5j_oScZZow4VOxCZZM.woff2) format('woff2');
#   unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;}html, body, [class*="css"] {
#     font-family: 'Tangerine'}
#     </style>
#     """,unsafe_allow_html=True,)

title = """<p style="font-family:'Tangerine'; color:Red; font-size:42px;">ThermoFeeler</p>"""
st.markdown(title, unsafe_allow_html=True)


st.markdown("""Enter a twitter query""")

query= st.text_input('Example : Apple')


# Progress bar
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)

response = predict_query(query)
st.write(response)

# if response != 200 :
#     st.error('You entered an inexistent query')
