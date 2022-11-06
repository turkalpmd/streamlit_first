

import streamlit as st
from utils import *


st.title("CSV İşleme Uygulaması")
uploaded_files = st.file_uploader("CSV Dosyasını Seçiniz", type="csv")
if st.button("Dosyayı Yükle ve Analiz Et"):
    create_user_log_file()
    if uploaded_files:
        save_to_log('INFO', 'Dosya yükleme işlemi başlatıldı.')
        try:
            dataframe = pd.read_csv(uploaded_files, header=0)
            save_to_log('INFO', 'Dosya yükleme işlemi başarılı.')

            try:
                result = process_csv(dataframe)
                save_to_log('INFO', 'Dosya işleme işlemi başarılı.')
                st.success(f"Sonuç: {result}")

                try:
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

        except Exception as e:
            save_to_log('ERROR', 'Dosya yükleme işlemi başarısız.')
            save_to_log('ERROR', e)
            st.write("Dosya yüklenirken bir hata oluştu.")