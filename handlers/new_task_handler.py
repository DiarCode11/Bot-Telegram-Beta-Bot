from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def NewTaskHandler(bot, chat_id, message_id, mode, sessions):
    taskname = sessions.get('taskname')
    date = sessions.get('date')
    time = sessions.get('time')
    
    title = 'Detail Tugas: '
    
    if mode == 'blank_task': 
        msg = f'*{title}*\n\n📖: 🚫\n🗓️: 🚫\n⏰: 🚫\n\nMasukkan Nama Tugas!'
        bot.editMessageText((chat_id, message_id), msg, parse_mode='Markdown')
    
    elif mode == 'create_task':
        msg = f'*{title}*\n\n📖: {taskname} ✅\n🗓️: 🚫\n⏰: 🚫\n\nMasukkan Tanggal Tenggat dari Tugas anda (format:DD-MM-YYYY)'
        bot.editMessageText((chat_id, message_id), msg, parse_mode='Markdown')
        
    elif mode == 'create_date': 
        msg = f'*{title}*\n\n📖: {taskname} ✅\n🗓️: {date} ✅\n⏰: 🚫\n\nMasukkan Waktu Tenggatnya (format:HH:MM)'
        bot.editMessageText((chat_id, message_id), msg, parse_mode='Markdown')
        
    elif mode == 'create_time': 
        msg = f'*{title}*\n\n📖: {taskname} ✅\n🗓️: {date} ✅\n⏰: {time} ✅\n\nSimpan perubahan?'
        
        button = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='👌 Simpan Tugas', callback_data='save_task'),
                 InlineKeyboardButton(text='🚫 Reset Task', callback_data='new_task')],
                [InlineKeyboardButton(text='⏮️ Home', callback_data='back')]
        ])
        
        bot.editMessageText((chat_id, message_id), msg, parse_mode='Markdown', reply_markup=button)
        
        
        
 