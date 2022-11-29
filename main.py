import streamlit as st
import io
from PIL import Image, ImageDraw, ImageFont
from pymongo import *

usn = st.secrets["USN"]
pwd = st.secrets["PWD"]

connection_str = f"mongodb+srv://{usn}:{pwd}@cluster0.h3wbmip.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(connection_str)
db = cluster["consortium-2022"]
st.set_page_config(page_title="Consortium Certification", page_icon=None,
                   layout="centered", initial_sidebar_state="collapsed", menu_items=None)


background = Image.open("./new_banner.png")
col1, col2, col3 = st.columns([0.2, 5, 0.2])
col2.image(background, use_column_width=True)

PATH = "./cert.png"

font = ImageFont.truetype("Poppins-Medium.ttf", 80)

collection = db["Events"]
# print(collection)
events = []
participants = []
for i in collection.find({}):
  events.append(i["event_name"])
event = st.selectbox("Select Event name", events)
for i in collection.find({"event_name" : event}):
  participants = i["Participants"]
name = st.selectbox("Select your name for generating certificate", participants)


im = Image.open(PATH)
d = ImageDraw.Draw(im)

W, H = im.size
w, h = d.textsize(name, font=font)
e_w, e_h = d.textsize(event, font=font)
print(w, h)
d.text(((((W-w)/2) + 105, ((H - h)/2) + 300)),
       name, fill=(56, 56, 56), font=font)
d.text(((((W-e_w)/2) - 700, ((H - e_h)/2) + 500)),
       event, fill=(56, 56, 56), font=font)
if st.button("Get Certificate"):
    ioData = io.BytesIO()
    im.save(ioData, format='PNG', quality='keep')
    finalImage = ioData.getvalue()
    st.image(finalImage)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
