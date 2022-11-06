
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


# Input

weight = st.number_input("Enter your Weight in KG", step = 0.1)

height = st.number_input("Enter your Height in Centimeters")

age = st.number_input("Enter your Age with month format",step=1)

gender  =st.text_input("Enter your gender with F or M")


df = pd.DataFrame()
df["weight"] = weight
df["height"] = height
df["age"] = age
df["gender"] = gender


uploaded_files = df

if st.button("Dosyayı Yükle ve Analiz Et"):
    
    try:
        wfa, lhfa = calc(weight,height,age,gender)
        df["wfa"] = wfa
        df["lhfa"] = lhfa
        save_to_log('INFO', 'Dosya işleme işlemi başarılı.')
        st.success(f"Your wfa is {wfa} anf lhfa is {lhfa}") 
        
        try:
            result = [weight,height,age,gender,wfa,lhfa]
            save_results(result)
            save_to_log('INFO', 'Sonuç dosyası oluşturuldu.')
            save_files()
            save_to_log('INFO', 'Dosyalar Google Drive\'a yüklendi.')

        except Exception as e:
            save_to_log('ERROR', 'Sonuç dosyası oluşturulamadı.')
            save_to_log('ERROR', e)
    
    except Exception as e:
        save_to_log('ERROR', 'Dosya işleme işlemi başarısız.')
        save_to_log('ERROR', e)
        st.write("Dosya işleme işlemi başarısız.")
        
