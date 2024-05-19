import os
from datetime import datetime,  timedelta
import pandas as pd
from handlers import SendNotifHandler

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

def combine_tasks():
    # Buat daftar untuk menyimpan dataframe
    dataframes = []
    folder_path = 'csv_files'
    # Iterasi melalui setiap file di folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv') and not filename.startswith('combined'):
            # Buat path penuh ke file csv
            file_path = os.path.join(folder_path, filename)
            
            # Baca file csv ke dataframe
            df = pd.read_csv(file_path)
            
            # Tambahkan kolom 'id' dengan nama folder
            df['Chat ID'] = filename.split('.')[0]
            
            # Tambahkan dataframe ke daftar
            dataframes.append(df)

    # Gabungkan semua dataframe dalam daftar menjadi satu dataframe
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Simpan dataframe gabungan ke file csv baru
    output_path = os.path.join(folder_path, 'combined.csv')
    combined_df.to_csv(output_path, index=False)

    print(f'All files combined and saved as {output_path}')
    
def reminder(bot): 
    current_time = datetime.now().time()

    # Path ke file CSV
    file_path = 'csv_files/combined.csv'

    # Membaca file CSV ke dalam DataFrame
    df = pd.read_csv(file_path)

    # Asumsikan kolom 'deadline' berisi tanggal dalam format 'YYYY-MM-DD'
    # Konversi kolom 'deadline' ke datetime
    df['Deadline'] = pd.to_datetime(df['Date'])

    # Dapatkan tanggal saat ini
    current_date = datetime.now()

    # Hitung selisih hari antara deadline dan tanggal saat ini
    df['days_until_deadline'] = (df['Deadline'] - current_date).dt.days

    # Filter tugas dengan deadline kurang dari 7 hari
    tasks_due_soon = df[df['days_until_deadline'] < 7]

    # Tampilkan tugas yang deadline kurang dari 7 hari
    for index, row in tasks_due_soon.iterrows():
        taskname = row['Taskname']
        deadline = row['Deadline']
        time = row['Time']
        chat_id = row['Chat ID']
        days_until_deadline = row['days_until_deadline']

        # Cek apakah jam 6.00
        if current_time.hour == 6 and current_time.minute == 0:
            # Kirim notifikasi  
            SendNotifHandler(bot, chat_id, taskname, deadline, time, days_until_deadline)

        
def Download_csv(bot, chat_id):
    folder_name = 'csv_files'
    csv_file_path = f'{folder_name}/{chat_id}.csv'
 
    # Periksa apakah file CSV ada
    if os.path.exists(csv_file_path):
        # Kirim file CSV ke pengguna
        bot.sendDocument(chat_id, open(csv_file_path, 'rb'))