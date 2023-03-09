import atexit, logging, random, json, requests, traceback

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.info("Программа Стартует")

with open("settings.json", "r", encoding='utf-8') as read_file:
    settings = json.load(read_file)

token = settings["token"]  # access_token
usertoken = settings["usertoken"]
repostCheckSet = settings["repostCheck"]
postId = settings["postId"]
apiVersion = 5.131
groupId = settings["groupId"]
subscribeGroups = settings["subscribe"]
pictures_ = settings["pictures"]
pictures = []
picNames = settings["names"]


def checkLink(text):
    if "https://steamcommunity.com/tradeoffer/new/?partner=" in text and "&token=" in text:
        return True
    return False

def checkRepost(userID):
    a = requests.get(f"https://api.vk.com/method/wall.getReposts?owner_id=-{groupId}&post_id={postId}&access_token={usertoken}&v={apiVersion}").json()["response"]
    ids = []
    for i in a["profiles"]:
        ids.append(str(i["id"]))
    if userID in ids:
        return True
    return False

@atexit.register
def saving():
    global users
    with open("users.json", "w", encoding='utf-8') as write_file:
        json.dump(users, write_file)
    logging.info("Программа завершила работу")


def sendMessage(peerId, randomId, text, attachment="", keyboard = ""):
    return requests.get(f"https://api.vk.com/method/messages.send?message={text}&attachment={attachment}&keyboard={keyboard}&peer_id={peerId}&access_token={token}&v={apiVersion}&random_id={randomId}").json()

def isMember(group_id, user_id):
    return requests.get(f"https://api.vk.com/method/groups.isMember?group_id={group_id}&user_id={user_id}&access_token={token}&v={apiVersion}").json()["response"]

def uploadPic(peer_id, picName):
    a = requests.get("https://api.vk.com/method/photos.getMessagesUploadServer?peer_id={}&access_token={}&v=5.131".format(peer_id,token)).json()
    b = requests.post(a['response']['upload_url'], files={'photo': open(picName, 'rb')}).json()
    c = requests.get( "https://api.vk.com/method/photos.saveMessagesPhoto?photo={}&server={}&hash={}&access_token={}&v=5.131".format(b['photo'],b['server'],b['hash'], token) ).json()
    d = "photo{}_{}".format(c["response"][0]["owner_id"], c["response"][0]["id"])
    return d

def textOrderisation(text):
    textN = ""
    for i in text:
        if i != " ":
            textN+= i
    return textN.lower()

def reborn(userId):
    users[userId] = 0
    return True

def zeroCondition(update, userId,text):
    if text != "забрать":
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["0"], keyboard=keyboard0)
    users[userId] = 1
    nickname = requests.get(f"https://api.vk.com/method/users.get?user_ids={userId}&fields=screen_name&access_token={token}&v={apiVersion}").json()["response"][0]["first_name"]
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["1"].format(nickname), keyboard=keyboard1)

def firstCondition(update, userId,text):
    if text != "посмотреть":
        nickname = requests.get(f"https://api.vk.com/method/users.get?user_ids={userId}&fields=screen_name&access_token={token}&v={apiVersion}").json()["response"][0]["first_name"]
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["1"].format(nickname), keyboard=keyboard1)
    users[userId] = 2
    rand = random.randint(0,len(pictures)-1)
    att = pictures[rand]
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["2"].format(picNames[rand]), attachment=att, keyboard=keyboard2)

def secondCondition(update, userId,text):
    if text != "хочу":
        return 0
    users[userId] = 3
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["3"], keyboard=keyboard3)

def thirdCondition(update, userId,text):
    if text != "выполнил":
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["3"], keyboard=keyboard3)
    if repostCheckSet == 1:
        if checkRepost(userId) == False:
            return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["no_repost"], keyboard=keyboard3)
    users[userId] = 4
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["4"], keyboard=keyboard4)

def fourthCondition(update, userId,text):
    if text != "переход":
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["4"], keyboard=keyboard4)
    for i in subscribeGroups:
        if isMember(i,userId) == False:
            return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["no_subscribe"], keyboard=keyboard4)
    users[userId] = 5
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["5"], keyboard=keyboard5)

def fifthCondition(update, userId, text):
    if text != "сделано":
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["5"], keyboard=keyboard5)
    users[userId] = 6
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["6"], keyboard=keyboard6)

def sixthCondition(update, userId, text):
    if text != "перепроверка":
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["6"], keyboard=keyboard6)
    users[userId] = 7
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["7"], keyboard=keyboard6)

def seventhCondition(update, userId, text):
    if text != "перепроверка":
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["7"], keyboard=keyboard6)
    users[userId] = 8
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["8"], keyboard=keyboard7)

def eitghtyCondition(update, userId, text):
    if not checkLink(text):
        return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["invalid_link"], keyboard=keyboard7)
    users[userId] = 9
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["9"], keyboard=keyboard7)

def nineCondition(update, userId, text):
    return sendMessage(update["object"]["message"]["peer_id"], update["object"]["message"]["random_id"], localisation["10"], keyboard=keyboard7)


with open("localisation.json", "r", encoding='utf-8') as read_file:
    localisation = json.load(read_file)

users = {}
with open("users.json", "r", encoding='utf-8') as read_file:
    users = json.load(read_file)

for i in pictures_:
    pictures.append(uploadPic(0, i))

keyboard0= json.dumps({"one_time":False, "buttons":[ [{"action":{"type":"text","label":"Забрать"},  "color":"primary"}] ]})
keyboard1= json.dumps({"one_time":False, "buttons":[ [{"action":{"type":"text","label":"Посмотреть"},  "color":"primary"}] ]})
keyboard2= json.dumps({"one_time":False, "buttons":[ [{"action":{"type":"text","label":"Хочу"},  "color":"primary"}] ]})
keyboard3= json.dumps({"one_time":False, "buttons":[ [{"action":{"type":"text","label":"Выполнил"},  "color":"primary"}] ]})
keyboard4= json.dumps({"one_time":False, "buttons":[ [{"action":{"type":"text","label":"Переход"},  "color":"primary"}] ]})
keyboard5= json.dumps({"one_time":False, "buttons":[ [{"action":{"type":"text","label":"Сделано"},  "color":"primary"}] ]})
keyboard6= json.dumps({"one_time":False, "buttons":[ [{"action":{"type":"text","label":"Перепроверка"},  "color":"primary"}] ]})
keyboard7= json.dumps({"one_time":True, "buttons":[]})

conditions = {
    0:lambda:zeroCondition(update, userId,text),
    1:lambda:firstCondition(update, userId,text),
    2:lambda:secondCondition(update, userId,text),
    3:lambda:thirdCondition(update, userId, text),
    4:lambda:fourthCondition(update, userId, text),
    5:lambda:fifthCondition(update, userId, text),
    6:lambda:sixthCondition(update, userId, text),
    7:lambda:seventhCondition(update, userId, text),
    8:lambda:eitghtyCondition(update, userId, text),
    9:lambda:nineCondition(update, userId, text)
}

def mainBot():
    global ts, update, userId, text # without ts - problems; update,user.text - можно определить перечень commands в самой функции как альтернатива
    
    response = requests.get('https://api.vk.com/method/groups.getLongPollServer',
                   params={'access_token': token, "v":apiVersion, "group_id":groupId}).json()["response"] # getting an longPoll server ( google if you are interested )
    keyLongPoll = response["key"]
    ts = response["ts"]
    serverLongPoll = response["server"] 
    
    while (True):
        try:
            response = requests.get(f"{serverLongPoll}?act=a_check&key={keyLongPoll}&ts={ts}&wait=25&mode=2&version={apiVersion}").json()
            logging.info(response)
            if response.get("updates",0): 
                for update in response["updates"]:
                    if update["type"] == "message_new":
                        text = textOrderisation(update["object"]["message"]["text"])
                        userId = str(update["object"]["message"]["from_id"])
                        if text == "привет1234привет":
                            reborn(userId)
                        conditions[users.get(userId, 0)]()
            ts = response["ts"]
        except Exception as e:
            try:
                logging.error(e)
                logging.error(traceback.format_exc())
                logging.error(e.message)
                logging.error(e.args)
                return
            except Exception as e:
                return

while True:
    mainBot()