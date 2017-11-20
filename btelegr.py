import time 
import requests 
import datetime
import random
from pymongo import MongoClient

TOKEN = '411787988:AAFJ7JdB6gXfeoNNksru_cN-Eh9Ei8_1_PY'

class BotHandler: 
    def __init__(self, token):
        self.token = token
        self.url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.url + method, params)
        result_json = resp.json()['result']
        return result_json

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
        return last_update

    def send_mess(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.url + method, params)
        return resp

    def switch(self, in_msg, last, db):
        welcome = ('здравствуйте', 'привет', 'ку', 'здарова', 'добрый день','hi', 'hello')
        cool = ('молодец', 'так держать','спасибо','круто','норм')  
        thanks = ('всегда пожалуйста', 'я старался', 'не проблема', 'обращайтесь')  
        out_msg = ''
        msg = ""    
        portals = db['portals']
        modes = db['portals.mods']  
        players = db['players']
        chat_id = last['message']['chat']['id']
        firstname = last['message']['chat']['first_name']
        username = last['message']['chat']['username']           
        if 'бот' in in_msg or 'Бот' in in_msg:
            if "статус" in in_msg:
                cursor = portals.find({"name": in_msg[11:]}) 
                f = True  
                for port in cursor:
                    f = False
                    mods = modes.find({"_id": port['_id']}) 
                    for mod in mods:   
                        msg = port['name'] + ":\n" +  mod["mod1"]+" | " + mod["mod2"]+" | " + mod["mod3"]+" | " + mod["mod4"]
                if f:
                    msg =  "Упс, " + in_msg[11:] + " нет в моей базе"
                self.send_mess(chat_id, msg)
            elif "где" in in_msg:
                objc = players.find({"nameing": in_msg[8:]})    
                f = True
                for plr in objc:            
                    f = False       
                    msg = in_msg[8:] + " последний раз был на "+ plr['portal'] + " в " + plr['time'] 
                if f:    
                    msg = "Прости друг, " + in_msg[8:] + " еще не добавил в базу, но я работаю над этим :)"
                self.send_mess(chat_id, msg)
        elif in_msg in welcome:
            self.send_mess(chat_id, random.SystemRandom().choice(welcome) + ', ' + firstname)
        elif in_msg in cool:            
            self.send_mess(chat_id, random.SystemRandom().choice(thanks))   

    def get_status(self, db):
        portals = db['portals']
        modes = db['portals.mods']  
        cursor = portals.find({"mod": 'X'})        
        for port in cursor:
            mods = modes.find({"_id": port['_id']}) 
            for mod in mods:   
                msg = port['name'] + ":\n" +  mod["mod1"]+" | " + mod["mod2"]+" | " + mod["mod3"]+" | " + mod["mod4"]
            self.send_mess(chat_id, msg)
            db.portals.update({ 'name': port['name'] }, { 'name': port['name'], 'mod': "" } )

def main():     
    greet_bot = BotHandler(TOKEN) 
    new_offset = None
    update_id = greet_bot.get_last_update()['update_id']   
    client = MongoClient("mongodb://user:user@ds149865.mlab.com:49865/ingressdb")
    db = client.ingressdb 
    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        if update_id == last_update['update_id']:
            message = last_update['message']['text']
            greet_bot.switch(message, last_update, db)
            update_id += 1        
        greet_bot.get_status(db)  
        time.sleep(1)     
     
if __name__ == '__main__':  
    main()