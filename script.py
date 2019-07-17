from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
main_token = '790952230:AAGHRP82mjWukDs88BnLWjakKUk9gHIPm78'
updater = Updater(token=main_token, use_context=True)
dispatcher = updater.dispatcher
import logging
import requests
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
from instagram import Account, Media, WebAgent
inst_url = 'https://instagram.com/p/' 
acc_list = []
checker = []
rep = updater.job_queue
added_acc = ''
q = open("acc_base.txt", "r")
for line in q :
       acc_list.append(line.strip())
q.close() 
def repeater(context: CallbackContext) :
        agent = WebAgent()
        checker = []    
        check_base = open("check_base.txt", "r")
        for line in check_base :
                checker.append(line.strip())
        check_base.close()
        print(checker)
        while len(checker) != len(acc_list) :
                checker.append('')
        for i in range(len(acc_list)) :
                agent = WebAgent()
                account = Account(acc_list[i])
                agent.update(account)
                last_post = agent.get_media(account, count = 1)
                media = Media(str(last_post[0][0]))
                media1 = str(Media(str(last_post[0][0])))
                if media.is_album == True and media1 != checker[i]  :
                        context.bot.send_message(chat_id='@omankoig' , text = inst_url + media.code)
                        checker[i] = media.code
                        continue 
                elif media1 == checker[i] :
                        continue
                elif media1 != checker[i] : 
                        upload_img = media.display_url
                        upload_caption = media.caption
                        print(upload_caption)
                        p = requests.get(upload_img)
                        out = open("1.jpg", "wb")
                        out.write(p.content)
                        out.close()
                        context.bot.send_photo(chat_id='@omankoig', photo=open('1.jpg', 'rb'))
                        context.bot.send_message(chat_id='@omankoig', text = upload_caption)
                        checker[i] = media.code
        check_base = open("check_base.txt", "w")
        for line in checker :
                check_base.write(line + '\n')
        check_base.close()
repeater_work = rep.run_repeating(repeater, interval = 80, first= 0)

def adder(update, context) :
        added_account = ''
        added_acc = str(update.message.text)
        if added_acc[0:4] == 'http'  :
                for i in range(2, len(added_acc) - 25 ):   
                        added_account += added_acc[-i]
                for i in range(len(acc_list)) :
                        if added_account == acc_list[i] :
                                break
                        else :
                                acc_list.append(added_account[::-1])
                                break
        else : 
                for i in range(len(acc_list)): 
                        if added_acc == acc_list[i]:
                                break
                        else:
                                acc_list.append(added_acc)
                                break
        q = open("acc_base.txt", "w")
        for line in acc_list :
                q.write(line+'\n')
        q.close()
        context.bot.send_message(chat_id = update.message.chat_id, text = 'Акааунт ' + update.message.text + ' добавлен')
        repeater_work = rep.run_repeating(repeater, interval = 80, first= 0)
adder_handler = MessageHandler(Filters.text , adder)
dispatcher.add_handler(adder_handler)

updater.start_polling()
