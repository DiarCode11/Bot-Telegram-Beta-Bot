import os
from datetime import datetime
import pandas as pd

def validate_date(date_text):
    try:
        input_date = datetime.strptime(date_text, '%d-%m-%Y')
        today = datetime.today()
        return input_date > today
    except ValueError:
        return False

def validate_time(time_text):
    try:
        datetime.strptime(time_text, '%H:%M')
        return True
    except ValueError:
        return False
    
def save_task(task, date, time, chat_id):
    # Membuat DataFrame baru dari data input
    df_new = pd.DataFrame({'Task': [task], 'Date': [date], 'Time': [time]})
    
    # Membuat nama file CSV berdasarkan chat_id
    csv_filename = f"{chat_id}.csv"
    
    # Path lengkap ke file CSV
    csv_file_path = os.path.join('csv_files', csv_filename)
    
    # Jika file CSV sudah ada, baca DataFrame dari file CSV
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        # Menggabungkan DataFrame baru dengan DataFrame yang sudah ada
        df = pd.concat([df, df_new], ignore_index=True)
    else:
        df = df_new  # Gunakan DataFrame baru jika file CSV belum ada
    
    # Menyimpan DataFrame ke dalam file CSV
    df.to_csv(csv_file_path, index=False)