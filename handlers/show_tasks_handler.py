import os
import pandas as pd
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def ShowTasksHandler(bot, chat_id, message_id):
    file_path = f'csv_files/{chat_id}.csv'
    
    if os.path.exists(file_path):
        # Membaca isi CSV
        df = pd.read_csv(file_path)
        
        # Membuat pesan teks dari isi CSV
        if not df.empty:
            msg = "*Berikut adalah tugas-tugas Anda:*\n\n"
            for index, row in df.iterrows():
                msg += f"📖: {row['Task']} \n🗓️: {row['Date']} \n⏰: {row['Time']} \n\n"
            
            button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='📝 Tugas baru', callback_data='new_task')],
                [InlineKeyboardButton(text='⬇ Download CSV', callback_data='download_csv')],
                [InlineKeyboardButton(text='🔙 Kembali', callback_data='back')]
            ])
        else:
            msg = "Horee, tidak ada tugas ditemukan. Ingin menambahkan tugas baru?"
            button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='📝 Tugas baru', callback_data='new_task')],
                [InlineKeyboardButton(text='🔙 Kembali', callback_data='back')]
            ])
    else:
        msg = "Hmmmm🤔, sepertinya kamu baru pertama kali menggunakan layanan pengingat tugas ini. Coba buat tugas baru 👇👇👇👇"
        button = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='📝 Tugas baru', callback_data='new_task')],
            [InlineKeyboardButton(text='🔙 Kembali', callback_data='back')]
        ])
    
    bot.editMessageText((chat_id, message_id), msg, parse_mode='Markdown', reply_markup=button)
