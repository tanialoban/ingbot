import requests 
import time 
import datetime
import random
from pymongo import MongoClient

TOKEN = '411787988:AAFJ7JdB6gXfeoNNksru_cN-Eh9Ei8_1_PY'
url = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_updates_json(request):  
    response = requests.get(request + 'getUpdates')
    return response.json()
 
def last_update(data):  
    results = data['result']
    total_updates = len(results) - 1
    return results[total_updates]

def get_chat_id(update):  
    chat_id = update['message']['chat']['id']
    return chat_id
 
def send_mess(chat, text):  
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

def get_updates_json(request):  
    params = {'timeout': 100, 'offset': None}
    response = requests.get(request + 'getUpdates', data=params)
    return response.json()

def switch(in_msg, last, db):
    welcome = ('здравствуйте', 'привет', 'ку', 'здарова', 'добрый день','hi', 'hello')
    cool = ('молодец', 'так держать','спасибо','круто')  
    thanks = ('всегда пожалуйста', 'я старался', 'не проблема', 'обращайтесь')  
    out_msg = ''
    msg = ""    
    portals = db['portals']
    modes = db['portals.mods']  
    players = db['players']
    chat_id = get_chat_id(last)   
    firstname = last['message']['chat']['first_name']
    username = last['message']['chat']['username']           
    if 'бот' in in_msg or 'Бот' in in_msg:
        if "статус" in in_msg:
            cursor = portals.find({"name": in_msg[11:]})   
            if cursor != "":     
                for port in cursor:
                    mods = modes.find({"_id": port['_id']}) 
                    for mod in mods:   
                        msg = port['name'] + ":\n" +  mod["mod1"]+" | " + mod["mod2"]+" | " + mod["mod3"]+" | " + mod["mod4"]
                        send_mess(chat_id, msg)
            else:
                send_mess(chat_id, "Упс, такого портала " + in_msg[11:] + " нет в моей базе")
        elif "где" in in_msg:
            objc = players.find({"nameing": in_msg[8:]})  
            for plr in objc:
                if plr != "":     
                    msg = in_msg[8:] + " последний раз был на "+ plr['portal'] + " в " + plr['time'] 
                else:
                    msg = "Прости друг, " + in_msg[8:] + " еще не добавил в базу, но я работаю над этим :)"
                send_mess(chat_id, msg)
    elif in_msg in welcome:
        send_mess(chat_id, random.SystemRandom().choice(welcome) + ', ' + firstname)
    elif in_msg in cool:            
        send_mess(chat_id, random.SystemRandom().choice(thanks))   
    time.sleep(3)   

def get_status(db):
    portals = db['portals']
    modes = db['portals.mods']  
    cursor = portals.find({"mod": 'X'})        
    for port in cursor:
        mods = modes.find({"_id": port['_id']}) 
        for mod in mods:   
            msg = port['name'] + ":\n" +  mod["mod1"]+" | " + mod["mod2"]+" | " + mod["mod3"]+" | " + mod["mod4"]
            print(msg)
            send_mess(chat_id, msg)
        db.portals.update({ 'name': port['name'] }, { 'name': port['name'], 'mod': "" } )
    time.sleep(3)  

def main():     
    update_id = last_update(get_updates_json(url))['update_id']   
    client = MongoClient("mongodb://user:user@ds149865.mlab.com:49865/ingressdb")
    db = client.ingressdb 
    while True:
        last = last_update(get_updates_json(url))
        if update_id == last['update_id']:
            message = last['message']['text']
            switch(message, last, db)
            update_id += 1        
        get_status(db)  
        time.sleep(5)     
    
 
if __name__ == '__main__':  
    main()