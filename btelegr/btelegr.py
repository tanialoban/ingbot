import time 
import requests 
import datetime
import random
from pymongo import MongoClient
import os

class Portal:
    def __init__(self, id, level, owner, mods, resors):
        self.id = id
        self.level = level
        self.owner = owner
        self.mods = mods
        self.resors = resors

    def __eq__(self, other):
        if self.id == other.id and self.level == other.level and self.owner == other.owner:                 
            for i, j in zip(self.mods, other.mods):
                if i != j:
                    return False
            for i, j in zip(self.resors, other.resors):
                if i != j:
                    return False   
            return True     
        return False

class BotHandler: 
    def __init__(self, token, name_bot):
        self.token = token
        self.name_bot = name_bot
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

    def portal_info_L8(self, name, value, portals, chat_id): #list L8 portals
        port8 = portals.find({name: value})
        msg = value + ':'
        i = 1
        for port in port8:
            msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
            i =  i + 1
        if i > 1:    
            self.send_mess(chat_id, msg)     
        else:
            self.send_mess(chat_id, "нет " + value)    

    def get_portal_ferms(self, name, key1, key2, portals, chat_id): #list L7-L8 portals with farm modes
        port7 = portals.find({name: key1})
        port8 = portals.find({name: key2})
        i = 1
        msg = key2 +':\n'                   
        for port in port8:
            moddb = modes.find({"_id": port['_id']})
            for mods in moddb:   
                if 'Heat Sink' in mods['mod1'] or 'Multi-hack' in mods['mod1']  or 'Transmuter' in mods['mod1'] or 'Heat Sink' in mods['mod2'] or 'Multi-hack' in mods['mod2']  or 'Transmuter' in mods['mod2'] or 'Heat Sink' in mods['mod3'] or 'Multi-hack' in mods['mod3']  or 'Transmuter' in mods['mod3'] or 'Heat Sink' in mods['mod4'] or 'Multi-hack' in mods['mod4']  or 'Transmuter' in mods['mod4'] :    
                    msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
                    i = i + 1
        if i == 1:    
            msg = ''
        msg = msg + '\n' + key1 + ':'
        for port in port7:
            moddb = modes.find({"_id": port['_id']})
            for mods in moddb:   
                if 'Heat Sink' in mods['mod1'] or 'Multi-hack' in mods['mod1']  or 'Transmuter' in mods['mod1'] or 'Heat Sink' in mods['mod2'] or 'Multi-hack' in mods['mod2']  or 'Transmuter' in mods['mod2'] or 'Heat Sink' in mods['mod3'] or 'Multi-hack' in mods['mod3']  or 'Transmuter' in mods['mod3'] or 'Heat Sink' in mods['mod4'] or 'Multi-hack' in mods['mod4']  or 'Transmuter' in mods['mod4'] :   
                    msg = msg + '\n' + str(i) + ". "+ port['name']  + " " + port['level'] + ' '  
                    i = i + 1
        if i > 1:    
            self.send_mess(chat_id, msg) 
        else:
            self.send_mess(chat_id, "нет ферм")    

    def portal_info_L78(self, name, key1, key2, portals, chat_id): #list L7-L8 portals
        port8 = portals.find({name: key1})
        port7 = portals.find({name: key2})
        msg = key1 + ':'
        i = 1
        for port in port8:
            msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
            i = i + 1
        if i == 1:    
            msg = ''
        msg = msg + '\n'+ key2 + ':'
        for port in port7:
            msg = msg + '\n' + str(i) + ". "+ port['name'] + " " + port['level'] + ' '
            i = i + 1
        if i > 1:    
            self.send_mess(chat_id, msg) 
        else:
            self.send_mess(chat_id, "нет " + key1 + "-" + key2)  

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
        try:
            firstname = last['message']['chat']['first_name']
        except KeyError:
            firstname = ''
            username = last['message']['from']['first_name'] 
        if self.name_bot in in_msg:  #chat for some people contains end word command '@namebot'          
            in_msg = in_msg[:-12]
    # command to bot
        if in_msg == '/enl8':            
            self.portal_info_L8("level", "E8", portals, chat_id)            
        if in_msg == '/enl78': 
            self.portal_info_L78("level", "E7", "E8", portals, chat_id)     
        if in_msg == '/res78':  
            self.portal_info_L78("level", "R7", "R8", portals, chat_id)    
        if in_msg == '/res8': 
            self.portal_info_L8("level", "R8", portals, chat_id) 
        if in_msg == '/eferm':
            self.get_portal_ferms("level", "E8", "E7", portals, chat_id)    
        if in_msg == '/rferm':
            self.get_portal_ferms("level", "R8", "R7", portals, chat_id) 

    # text message to bot
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
                    msg =  "OOPS, " + in_msg[11:] + " no found"
                self.send_mess(chat_id, msg)
            elif "где" in in_msg:
                objc = players.find({"nameing": in_msg[8:]})    
                f = True
                for plr in objc:            
                    f = False       
                    msg = in_msg[8:] + " последний раз был на "+ plr['portal'] + " в " + plr['time'] 
                if f:    
                    msg = "OOPS, " + in_msg[8:] + " еще не добавил в базу, но я работаю над этим :)"
                self.send_mess(chat_id, msg)
        elif in_msg.lower() in welcome:
            self.send_mess(chat_id, random.SystemRandom().choice(welcome) + ', ' + firstname)
        elif in_msg.lower() in cool:            
            self.send_mess(chat_id, random.SystemRandom().choice(thanks)) 
        print(msg)
                 
def main():            
    TOKEN = os.environ['TELEGRAM_TOKEN']
    print("TELEGRAM_TOKEN " + TOKEN)
    MONGO_URI = os.environ['MONGO_URI']
    print("MONGO_URI " + MONGO_URI)
    NAME_BOT = os.environ['NAME_BOT']
    print("NAME_BOT " + NAME_BOT)
    greet_bot = BotHandler(TOKEN, NAME_BOT) 
    new_offset = None
    update_id = greet_bot.get_last_update()['update_id']   
    client = MongoClient(MONGO_URI)
    db = client.ingressdb 
    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        if update_id == last_update['update_id']: #while don't come new message
            message = last_update['message']['text']
            print(message)
            greet_bot.switch(message, last_update, db)
            update_id += 1       
     
if __name__ == '__main__':  
    main()