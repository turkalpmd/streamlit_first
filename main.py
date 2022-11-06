
from PIL import Image
import streamlit as st
from utils import *
import pandas as pd
import numpy as np


st.title("This is My Z-score Calculator")

img = Image.open("zscore.png")
st.image(img)

# Introduction

st.subheader("Introduction")

st.text("""
Burada Z-score'ları hesaplıyacağız inş.
	""")


weight = st.number_input("KG cinsinden ağırlık;", step = 0.1)
height = st.number_input("Santimetre cinsinden boyu;")
age = st.number_input("Ay olarak yaşı;",step=1)
gender =st.text_input("Erkek için M Kız için F yazınız;")


if st.button("Z skorunu Analiz Et"):


    wfa, lhfa = calc(weight,height,age,gender)#result = process_csv(dataframe)
    df["wfa"] = wfa
    df["lhfa"] = lhfa
    
    st.success(f"Your wfa is {wfa} anf lhfa is {lhfa}") #st.success(f"Sonuç: {result}")
    
    #result = [weight,height,age,gender,wfa,lhfa]
    #save_results(result)
    #save_files()
    