import time 
import requests 
import datetime
import random
from pymongo import MongoClient
import os

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
        print('start send')
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.url + method, params)
        print('end send')
        print(chat_id)
        print(text)
        return resp

    def switch(self, in_msg, last, db):
        welcome = ('здравствуйте', 'привет', 'ку', 'здарова', 'добрый день','hi', 'hello')
        cool = ('молодец', 'так держать','спасибо','круто','норм')  
        thanks = ('всегда пожалуйста', 'я старался', 'не проблема', 'обращайтесь')  
        out_msg = ''
        msg = ""    
        modes = db['portals.mods']  
        players = db['players']
        portals = db['portals']
        chat_id = last['message']['chat']['id']
        
        print("swich start")
        try:
            firstname = last['message']['chat']['first_name']
        except KeyError:
            firstname = ''
            username = last['message']['from']['first_name'] 
        if '@bjornKingBot' in in_msg:              
            in_msg = in_msg[:-13]
        if in_msg == '/enl8':            
            portE8 = portals.find({"level": "E8"})
            msg = 'E8:'
            i = 1
            for port in portE8:
                msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
                i =  i + 1
            if i > 1:    
                self.send_mess(chat_id, msg)     
            else:
                self.send_mess(chat_id, "нет E8")    
        if in_msg == '/enl78': 
            portE8 = portals.find({"level": "E8"})
            portE7 = portals.find({"level": "E7"})
            msg = 'E8:'
            i = 1
            for port in portE8:
                msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
                i = i + 1
            if i == 1:    
                msg = ''
            msg = msg + '\nE7:'
            for port in portE7:
                msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
                i = i + 1
            if i > 1:    
                self.send_mess(chat_id, msg) 
            else:
                self.send_mess(chat_id, "нет E7-E8")    
        if in_msg == '/res78':  
            portR8 = portals.find({"level": "R8"})
            portR7 = portals.find({"level": "R7"})
            msg = 'R8:'
            i = 1
            for port in portR8:
                msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
                i = i + 1
            if i == 1:    
                msg = ''
            msg = msg + '\nR7:'
            for port in portR7:
                msg = msg + '\n' + str(i) + ". "+ port['name']  + " " + port['level'] + ' '  
                i = i + 1
            if i > 1:    
                self.send_mess(chat_id, msg) 
            else:
                self.send_mess(chat_id, "нет R7-R8")    
        if in_msg == '/res8': 
            
            print("command res8")  
            portR8 = portals.find({"level": "R8"})            
            print("find res8")
            i = 1
            msg = 'R8:'
            for port in portR8:
                msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '   
                i = i + 1
            
            print("before send message")    
            if i > 1:    
                self.send_mess(chat_id, msg) 
            else:
                self.send_mess(chat_id, "нет R8")        
        if in_msg == '/eferm':
            portE7 = portals.find({"level": "E7"})
            portE8 = portals.find({"level": "E8"})
            i = 1
            msg = 'E8:\n'                   
            for port in portE8:
                moddb = modes.find({"_id": port['_id']})
                for mods in moddb:   
                    if 'Heat Sink' in mods['mod1'] or 'Multi-hack' in mods['mod1']  or 'Transmuter' in mods['mod1'] or 'Heat Sink' in mods['mod2'] or 'Multi-hack' in mods['mod2']  or 'Transmuter' in mods['mod2'] or 'Heat Sink' in mods['mod3'] or 'Multi-hack' in mods['mod3']  or 'Transmuter' in mods['mod3'] or 'Heat Sink' in mods['mod4'] or 'Multi-hack' in mods['mod4']  or 'Transmuter' in mods['mod4'] :    
                        msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
                        i = i + 1

            if i == 1:    
                msg = ''
            msg = msg + '\nE7:'
            for port in portE7:
                moddb = modes.find({"_id": port['_id']})
                for mods in moddb:   
                    if 'Heat Sink' in mods['mod1'] or 'Multi-hack' in mods['mod1']  or 'Transmuter' in mods['mod1'] or 'Heat Sink' in mods['mod2'] or 'Multi-hack' in mods['mod2']  or 'Transmuter' in mods['mod2'] or 'Heat Sink' in mods['mod3'] or 'Multi-hack' in mods['mod3']  or 'Transmuter' in mods['mod3'] or 'Heat Sink' in mods['mod4'] or 'Multi-hack' in mods['mod4']  or 'Transmuter' in mods['mod4'] :   
                        msg = msg + '\n' + str(i) + ". "+ port['name']  + " " + port['level'] + ' '  
                        i = i + 1
            if i > 1:    
                self.send_mess(chat_id, msg) 
            else:
                self.send_mess(chat_id, "нет ферм")    
        if in_msg == '/rferm':
            portR7 = portals.find({"level": "R7"})
            portR8 = portals.find({"level": "R8"})
            msg = 'R8:'
            i = 1
            for port in portR8:
                moddb = modes.find({"_id": port['_id']})
                for mods in moddb:   
                    if 'Heat Sink' in mods['mod1'] or 'Multi-hack' in mods['mod1']  or 'Transmuter' in mods['mod1'] or 'Heat Sink' in mods['mod2'] or 'Multi-hack' in mods['mod2']  or 'Transmuter' in mods['mod2'] or 'Heat Sink' in mods['mod3'] or 'Multi-hack' in mods['mod3']  or 'Transmuter' in mods['mod3'] or 'Heat Sink' in mods['mod4'] or 'Multi-hack' in mods['mod4']  or 'Transmuter' in mods['mod4'] :   
                        msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
                        i = i + 1
            if i == 1:    
                msg = ''
            msg = msg + '\nR7:'
            for port in portR7:
                moddb = modes.find({"_id": port['_id']})
                for mods in moddb: 
                    if 'Heat Sink' in mods['mod1'] or 'Multi-hack' in mods['mod1']  or 'Transmuter' in mods['mod1'] or 'Heat Sink' in mods['mod2'] or 'Multi-hack' in mods['mod2']  or 'Transmuter' in mods['mod2'] or 'Heat Sink' in mods['mod3'] or 'Multi-hack' in mods['mod3']  or 'Transmuter' in mods['mod3'] or 'Heat Sink' in mods['mod4'] or 'Multi-hack' in mods['mod4']  or 'Transmuter' in mods['mod4'] :   
                        msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '  
                        i = i + 1
            if i > 1:    
                self.send_mess(chat_id, msg) 
            else:
                self.send_mess(chat_id, "нет ферм")     

        if 'бот' in in_msg or 'Бот' in in_msg:
            if "статус" in in_msg:
                cursor = portals.find({"name": in_msg[11:]}) 
                f = True  
                for port in cursor:
                    f = False
                    mods = modes.find({"_id": port['_id']}) 
                    for mod in mods:   
                        msg = port['name'] + ":\n" +  mod["mod1"]+" = " + mod["own1"]  + "\n"+ mod["mod2"]+" = "+ mod["own2"]  + "\n" + mod["mod3"]+" = " + mod["own3"]  + "\n" + mod["mod4"] + " = "+ mod["own4"]
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
        elif in_msg.lower() in welcome:
            self.send_mess(chat_id, random.SystemRandom().choice(welcome) + ', ' + firstname)
        elif in_msg.lower() in cool:            
            self.send_mess(chat_id, random.SystemRandom().choice(thanks)) 
        print("end swich")      
        print(msg)

    def get_status(self, db,chat_id):
        portals = db['portals']
        modes = db['portals.mods']  
        cursor = portals.find()        
        for port in cursor:
            mods = modes.find({"_id": port['_id']}) 
            msg = ''
            for mod in mods:   
                msg = port['name'] + ":\n" +  mod["mod1"]+" = " + mod["own1"]  + "\n"+ mod["mod2"]+" = "+ mod["own2"]  + "\n" + mod["mod3"]+" = " + mod["own3"]  + "\n" + mod["mod4"] + " = "+ mod["own4"]
            # self.send_mess(chat_id, msg)
            try: 
                db.portals.update({"_id": port['_id']}, 
                {"_id": port['_id'], "level": port['level'], "owner":  port['owner'], "name": port['name'], "lat": port['lat'], 'lng':port['lng'], 'mod': port['mod'] })
            except KeyError:
                db.portals.update({"_id": port['_id']}, 
                {"_id": port['_id'], "level": port['level'], "owner":  '', "name": port['name'], "lat": port['lat'], 'lng':port['lng'], 'mod': port['mod'] })
               

def main():
    TOKEN = os.environ['TELEGRAM_TOKEN']
    print("TELEGRAM_TOKEN" + TOKEN)
    MONGO_URI = os.environ['MONGO_URI']
    print("MONGO_URI" + MONGO_URI)


    greet_bot = BotHandler(TOKEN) 
    new_offset = None
    update_id = greet_bot.get_last_update()['update_id']   
    client = MongoClient(MONGO_URI)
    db = client.ingressdb 
    while True:
        print("wait new updates")
        greet_bot.get_updates(new_offset)
        print("wait last update test 3")
        last_update = greet_bot.get_last_update()
        print(update_id,last_update['update_id'])
        if update_id == last_update['update_id']:
            message = last_update['message']['text']
            print(message)
            greet_bot.switch(message, last_update, db)
            # greet_bot.get_status(db, last_update['message']['chat']['id'])  
            update_id += 1       
     
if __name__ == '__main__':  
    main()