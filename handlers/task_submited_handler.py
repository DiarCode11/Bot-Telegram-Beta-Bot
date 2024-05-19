from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def TaskSubmittedHandler(bot, chat_id, message_id): 
    msg = '*Tugas Berhasil Ditambahkan*\n\nTugas yang anda inputkan sudah tersimpan 😊. Kamu bisa menambahkan tugas baru lagi atau melihat tugas yang sudah diinputkan\n\nAyo coba👇👇👇👇'
    button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📝 Tugas baru', callback_data='new_task')],
        [InlineKeyboardButton(text='📒 Lihat Tugas', callback_data='show_tasks')]
    ])
    bot.editMessageText((chat_id, message_id), msg, parse_mode='Markdown', reply_markup=button)
        