import telepot
import os
import time
from telepot.loop import MessageLoop
from dotenv import load_dotenv
from handlers import StartHandler, NewTaskHandler, TaskSubmittedHandler, ShowTasksHandler, BackHandler
from task_utils import validate_date, validate_time, save_task, Download_csv

class BetaBot:
    def __init__(self, token):
        self.bot = telepot.Bot(token)
        self.sessions = {}  # Dictionary untuk menyimpan data sesi pengguna
        
        self._setup_handlers()
    
    def _setup_handlers(self):
        MessageLoop(self.bot, {
            'chat': self.handle_message,
            'callback_query': self.handle_callback_query
        }).run_as_thread()

    def handle_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        # Inisialisasi sesi jika belum ada
        if chat_id not in self.sessions: 
            self.sessions[chat_id] = {
                'lastBotMsgID': None,
                'isCreateTask': False, 
                'isCreateDate': False,
                'isCreateTime': False, 
                'taskname': None,
                'date': None,
                'time': None
            }
        
        if content_type == 'text':
            if msg['text'] == '/start':
                StartHandler(self.bot, chat_id)
        
            elif not msg['text'].startswith('/') and self.sessions[chat_id]['isCreateTask']: 
                self.sessions[chat_id]['taskname'] = msg['text']
                NewTaskHandler(self.bot, chat_id, self.sessions[chat_id]['lastBotMsgID'], mode='create_task', sessions=self.sessions[chat_id])
                self.sessions[chat_id]['isCreateTask'] = False  # Matikan sesi Create task
                self.sessions[chat_id]['isCreateDate'] = True  # Lanjut ke sesi Create Date
                
                time.sleep(1) 
                self.bot.deleteMessage((chat_id, msg['message_id']))  # Hapus pesan setelah 1 detik
                
            elif not msg['text'].startswith('/') and self.sessions[chat_id]['isCreateDate']: 
                if validate_date(msg['text']):
                    self.sessions[chat_id]['date'] = msg['text']
                    NewTaskHandler(self.bot, chat_id, self.sessions[chat_id]['lastBotMsgID'], mode='create_date', sessions=self.sessions[chat_id])
                    self.sessions[chat_id]['isCreateDate'] = False
                    self.sessions[chat_id]['isCreateTime'] = True
                    
                    time.sleep(1) 
                    self.bot.deleteMessage((chat_id, msg['message_id']))
                else : 
                    msg = 'Masukkan format dengan benar!'
                    self.bot.sendMessage(chat_id, msg)
                
            elif not msg['text'].startswith('/') and self.sessions[chat_id]['isCreateTime']: 
                if validate_time(msg['text']):
                    self.sessions[chat_id]['time'] = msg['text']
                    NewTaskHandler(self.bot, chat_id, self.sessions[chat_id]['lastBotMsgID'], mode='create_time', sessions=self.sessions[chat_id])
                    self.sessions[chat_id]['isCreateTime'] = False
                    
                    time.sleep(1) 
                    self.bot.deleteMessage((chat_id, msg['message_id']))
                else : 
                    msg = 'Masukkan format dengan benar!'
                    elf.bot.sendMessage(chat_id, msg)

    def handle_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        chat_id = msg['message']['chat']['id']
        message_id = msg['message']['message_id']
        
        if query_data == 'new_task':
            self.sessions[chat_id]['isCreateTask'] = True
            self.sessions[chat_id]['lastBotMsgID'] = message_id
            NewTaskHandler(self.bot, chat_id, self.sessions[chat_id]['lastBotMsgID'], mode='blank_task', sessions=self.sessions[chat_id])
            
        elif query_data == 'show_tasks':
            ShowTasksHandler(self.bot, chat_id, message_id)
        
        elif query_data == 'save_task':
            save_task(self.sessions[chat_id]['taskname'], self.sessions[chat_id]['date'], self.sessions[chat_id]['time'], chat_id)
            TaskSubmittedHandler(self.bot, chat_id, message_id)
        
        elif query_data == 'back':
            BackHandler(self.bot, chat_id, message_id)
            
        elif query_data == 'download_csv': 
            Download_csv(self.bot, chat_id)

    def start(self):
        print('Bot is listening ...')
        # Keep the program running
        while True:
            time.sleep(5)

if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.getenv('TOKEN')

    if TOKEN is None:
        raise ValueError("No TOKEN found in environment variables")

    bot = BetaBot(TOKEN)
    bot.start()
