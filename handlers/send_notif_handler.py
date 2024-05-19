from datetime import datetime

def SendNotifHandler(bot, chat_id, taskname, date, time, day):
    msg = f'*[🤖 BETABOT REMINDER 🤖]*\n\nHai, sepertinya ada tugas yang deadlinenya sudekat. Jangan lupa membuat tugasnya ya! 😊\n\nDetail Tugasmu:\n📖: {taskname} \n🗓️: {date} \n⏰: {time}'
    
    bot.sendMessage(chat_id, msg, parse_mode='Markdown')
    
