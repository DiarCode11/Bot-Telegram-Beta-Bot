from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

msg = '*Hai saya Beta Bot, senang bertemu denganmu* 😊. \n\nSaya bisa mengingatkan tugasmu saat deadline sudah mulai dekat, cukup dengan mengklik tombol Tambahkan Tugas dibawah. Selain itu kamu juga bisa melihat tugas-tugas yang sudah dicatat dan mendapatkan nya dalam format .xlsx. \n\nAyo coba!  👇👇👇👇'
    
button = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='📝 Tugas baru', callback_data='new_task')],
            [InlineKeyboardButton(text='📒 Lihat Tugas', callback_data='show_tasks')]
        ])

def StartHandler(bot, chat_id):
    bot.sendMessage(chat_id, msg, parse_mode='Markdown', reply_markup=button)

def BackHandler(bot, chat_id, message_id):
    bot.editMessageText((chat_id, message_id), msg, parse_mode='Markdown', reply_markup=button)