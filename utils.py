

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import pandas as pd
import streamlit as st

from pygrowup import Calculator
#from pygrowup import helpers



# Kullanıcıları, girdikleri tarih ile adlandıracağız.
current_user = datetime.now().strftime('%H.%M.%S.%f %d-%m-%Y')

created_files = []


# Kullanıcı için log dosyası oluşturuluyor.
def create_user_log_file():
    # Kullanıcı için log dosyası oluşturma,
    with open(f"log_{current_user}.txt", "w", encoding="utf-8") as f:

        created_files.append(f"log_{current_user}.txt")
        # İlk mesaj
        log_message = str(current_user + " için log dosyasının başlangıcı.\n\n")
        
        f.write(log_message)
        f.close()


# Log dosyasına mesaj eklemek için kullanılır.
# Log type, mesajın tipini belirtir.
# Log type değerleri: INFO ve ERROR
def save_to_log(log_type, log_message):
    # Log dosyası açılır.
    with open(f"log_{current_user}.txt", "a", encoding="utf-8") as f:
        # Olayın gerçekleştiği saat alınır.
        event_date = datetime.now().strftime('%H.%M.%S %d-%m-%Y')
        # Log mesajı oluşturulur.
        log_message = str(event_date + " " + log_type + " " + log_message + '\n')
        f.write(log_message)
        f.close()


def create_drive_auth():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile('mycreds.txt')
    if gauth.credentials is None:
        # Eğer mycreds.txt dosyası yoksa, kullanıcıdan kimlik doğrulaması yapılması istenir.
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Kimlik doğrulaması süresi dolmuşsa yeniden kimlik doğrulaması yapılır.
        gauth.Refresh()
    else:
        # Kimlik doğrulaması geçerliyse kimlik doğrulaması yapılması istenmez.
        gauth.Authorize()
    # Kimlik doğrulaması sonucunda elde edilen bilgiler mycreds.txt dosyasına kaydedilir.
    gauth.SaveCredentialsFile('mycreds.txt')


def calc(weight,height,age,gender):

    if age <= 24:
        calculator = Calculator(adjust_height_data=False, 
                                adjust_weight_scores=False,
                                include_cdc=False, 
                                logger_name='pygrowup',
                                log_level='INFO')

        wfa = calculator.wfa(weight,age,gender)
        lhfa = calculator.lhfa(height,age,gender)

    if age > 24:
        calculator = Calculator(adjust_height_data=False, 
                                adjust_weight_scores=False,
                                include_cdc=True, 
                                logger_name='pygrowup',
                                log_level='INFO')

        wfa = calculator.wfa(weight,age,gender)
        lhfa = calculator.lhfa(height,age,gender)

    return wfa,lhfa


def process_csv(dataframe):
    dataframe.to_csv(f"csv_{current_user}.csv", index=False)
    created_files.append(f"csv_{current_user}.csv")
    return dataframe.sum().values[0]


def save_results(result):
    with open(f"result_{current_user}.txt", "a", encoding="utf-8") as f:
        created_files.append(f"result_{current_user}.txt")
        f.write(str(result))
        f.close()


def save_files():
    gauth = GoogleAuth()
    create_cred_file()
    gauth.LoadCredentialsFile('mycreds_test.txt')
    drive = GoogleDrive(gauth)
    folder_name = 'test'  # Please set the folder name.
    folders = drive.ListFile(
        {
            'q': "title='" + folder_name + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folders:
        if folder['title'] == folder_name:
            for created_file in created_files:
                file2 = drive.CreateFile({'parents': [{'id': folder['id']}]})
                file2.SetContentFile(created_file)
                file2.Upload()


def create_cred_file():
    cred_str = '{"access_token": "' + st.secrets["access_token"] +\
               '", "client_id": "' + st.secrets["client_id"] +\
               '", "client_secret": "' + st.secrets["client_secret"] + \
               '", "refresh_token": "' + st.secrets["refresh_token"] + \
               '", "token_expiry": "' + st.secrets["token_expiry"] + \
               '", "token_uri": "' + st.secrets["token_uri"] + \
               '", "user_agent": null' + \
               ', "revoke_uri": "' + st.secrets["revoke_uri"] + \
               '", "id_token": null' + \
               ', "id_token_jwt": null' + \
               ', "token_response": {"access_token": "' + st.secrets["token_response"]["access_token"] + \
               '", "expires_in": ' + str(st.secrets["token_response"]["expires_in"]) + \
               ', "refresh_token": "' + st.secrets["token_response"]["refresh_token"] + \
               '", "scope": "' + st.secrets["token_response"]["scope"] + \
               '", "token_type": "' + st.secrets["token_response"]["token_type"] + \
               '"}, "scopes": ["https://www.googleapis.com/auth/drive"]' + \
               ', "token_info_uri": "' + st.secrets["token_info_uri"] + \
               '", "invalid": false' + \
               ', "_class": "' + st.secrets["_class"] + \
               '", "_module": "' + st.secrets["_module"] + '"}'
    text_file = open("mycreds_test.txt", "w")
    n = text_file.write(cred_str)
    text_file.close()