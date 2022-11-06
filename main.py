
from PIL import Image
import streamlit as st
from utils import *
import pandas as pd
import numpy as np


st.title("Z-score Hesaplama Uygulaması")

img = Image.open("hacettepe.jpg")
st.image(img)

# Introduction

st.subheader("Büyüme Takibi")


st.text("""
Bu uygulamada Z score'lar 2 yaş ve altında WHO üstünde ise \n
CDC referans aralıkları kullanılarak hesaplanır.
	""")


weight = st.number_input("KG cinsinden ağırlık;", step = 0.1)
height = st.number_input("Santimetre cinsinden boyu;")
age = st.number_input("Ay olarak yaşı;",step=1)
gender =st.radio("Cinsiyeti seçiniz", options=["Erkek","Kız"])
    #text_input("Erkek için E Kız için K yazınız;")

if gender == "Erkek":
    gender = "M"
if gender == "Kız":
    gender = "F"

df = pd.DataFrame()
df["weight"] = weight
df["height"] = height
df["age"] = age
df["gender"] = gender

uploaded_files = df
if st.button("Z skorunu Analiz Et"):



    wfa, lhfa = calc(weight,height,age,gender)#result = process_csv(dataframe)
    df["wfa"] = wfa
    df["lhfa"] = lhfa
    
    st.success(f"Yaşa göre ağırlık; {wfa} \n 
                 Yaşa göre boy; {lhfa}'dur ") #st.success(f"Sonuç: {result}")
    
    #result = [weight,height,age,gender,wfa,lhfa]
    #save_results(result)
    #save_files()
    