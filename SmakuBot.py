from fbchat import Client
from fbchat.models import *
from bs4 import BeautifulSoup
from requests import get
import random, time, datetime, json, requests, os, sys
import numpy as np


email = "smakubot@gmail.com"
password = "koloporter1"

ryz = "2304717856220410"
meine = "1536442066412320"
mojeid = "100012448476506"
korsan = "100024773796503"
swider = "100007813848151"

barka = "\nPan kiedyś stanął nad brzegiem\nSzukał ludzi gotowych pójść za Nim\nBy łowić serca\nSłów Bożych prawdą.\n\nRef.:\nO Panie, to Ty na mnie spojrzałeś,\nTwoje usta dziś wyrzekły me imię.\nSwoją barkę pozostawiam na brzegu,\nRazem z Tobą nowy zacznę dziś łów.\n\n2.\nJestem ubogim człowiekiem,\nMoim skarbem są ręce gotowe\nDo pracy z Tobą\nI czyste serce.\n\n3.\nTy, potrzebujesz mych dłoni,\nMego serca młodego zapałem\nMych kropli potu\nI samotności.\n\n4.\nDziś wypłyniemy już razem\nŁowić serca na morzach dusz ludzkich\nTwej prawdy siecią\nI słowem życia.\n\n\nBy Papież - https://www.youtube.com/watch?v=fimrULqiExA\nZ tekstem - https://www.youtube.com/watch?v=_o9mZ_DVTKA"

kolorki = [ThreadColor.BILOBA_FLOWER, ThreadColor.BRILLIANT_ROSE, ThreadColor.CAMEO, ThreadColor.DEEP_SKY_BLUE, ThreadColor.FERN, ThreadColor.FREE_SPEECH_GREEN, ThreadColor.GOLDEN_POPPY, ThreadColor.LIGHT_CORAL, ThreadColor.MEDIUM_SLATE_BLUE, ThreadColor.MESSENGER_BLUE]

memy = ["memy", "demotywatory", "jeja"]

headers = {
    'Content-Type': "application/json",
    'x-api-key': "bffd8b8b-cfa0-4d1a-8f6b-ba9207dc6c79"
}


def urban_dictionary(word):
    word = word.replace(" ", "+")
    response = requests.get("https://www.miejski.pl/slowo-" + word)
    if response.status_code == 404:
        response = None
        return "Nie znaleziono takiego słowa"
    else:
        parsed = BeautifulSoup(response.text, "html.parser")
        title = parsed.body.find("h1").get_text()
        definition = parsed.find("div", "definition summary").get_text()
        example = parsed.find("div", "example").get_text()
        message = title + "\nDefinicja:" + definition + "\n\nPrzyklad/y:" + example
        parsed = None
        response = None
        return message


class SmakuBot(Client):
    ryz_commands = False
    weather_key = ""

    def mentions(self, thread_id):
        thread = list(self.fetchThreadInfo(thread_id)[thread_id].participants)
        mention = []
        for i in range(len(thread)):
            mention.append(Mention(thread[i], 0, 9))
        return mention

    def onNicknameChange(self, mid=None, author_id=None, changed_for=None, new_nickname=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        if author_id != self.uid:
            if changed_for == self.uid:
                if new_nickname != np.load("nazwa.npy"):
                    abcdef = np.load("nazwa.npy")
                    self.changeNickname(str(abcdef), str(self.uid), str(thread_id), thread_type)

    def onListenError(self, exception=None):
        print(exception)
        if self.isLoggedIn():
            pass
        else:
            self.login(email, password)

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                  thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):
        # self.markAsDelivered(thread_id, message_object.uid)
        # self.markAsRead(thread_id)
        print(message_object)
        print(message_object.text)
        if author_id == mojeid:
            if message_object.text[0:7] == "!nazwa ":
                a = message_object.text.replace("!nazwa ", "")
                np.save("nazwa", a)
                b = self.fetchThreadList()
                for c in b:
                    self.changeNickname(a, self.uid, c.uid, c.type)
            elif message_object.text[0:4] == "!bc ":
                a = message_object.text.replace("!bc ", "")
                b = self.fetchThreadList()
                for c in b:
                    self.send(Message(a), c.uid, c.type)
            elif message_object.text[0:3].lower() == "!r ":
                react = message_object.text.lower().replace("!r ", "")
                react = react.split(" ")
                s = self.fetchThreadMessages(thread_id, int(react[0])+int(react[1]))
                if react[2] == "angry":
                    react[2] = MessageReaction.ANGRY
                elif react[2] == "smile":
                    react[2] = MessageReaction.SMILE
                elif react[2] == "sad":
                    react[2] = MessageReaction.SAD
                elif react[2] == "wow":
                    react[2] = MessageReaction.WOW
                elif react[2] == "love":
                    react[2] = MessageReaction.LOVE
                elif react[2] == "yes":
                    react[2] = MessageReaction.YES
                elif react[2] == "no":
                    react[2] = MessageReaction.NO

                for a in range(int(react[1])):
                    self.reactToMessage(s[int(react[0])+a].uid, react[2])
            elif message_object.text == "!ip":
                if thread_type == ThreadType.USER:
                    ip = get("https://api.ipify.org").text
                    self.send(Message("Moje IP: "+ip), thread_id, thread_type)
                    ip = None
                else:
                    self.send(Message("Moje IP to 127.0.0.1"), thread_id, thread_type)
            elif message_object.text[0:6].lower() == "!bomb ":
                a = message_object.text.split(" ")
                parameters = {"inputUserMobile": a[1]}
                self.send(Message("Zaczynam wysyłać"), thread_id, thread_type)
                for i in range(int(a[2])):
                    adres = "http://gry.wapster.pl/ma/send.aspx?src=wap2&fid="+str(random.choice(self.gamelist))+"&r=LPH"
                    r = requests.post(adres, data=parameters)
                self.send(Message("Wysłano "+a[2]+" wiadomosci na numer "+a[1]), thread_id, thread_type)
                
                pass

            if (author_id == mojeid) or (thread_id != ryz) or self.ryz_commands is True:
                if message_object.text.lower() == "!doggo":
                    response = requests.get("https://dog.ceo/api/breeds/image/random")
                    dog = json.loads(response.text)
                    self.sendRemoteImage(dog["message"], None, thread_id, thread_type)
                elif message_object.text.lower() == "!catto":
                    response = requests.get("https://api.thecatapi.com/v1/images/search", headers)
                    cat = json.loads(response.text)
                    self.sendRemoteImage(cat[0]["url"], None, thread_id, thread_type)
                elif message_object.text.lower() == "!birb":
                    response = requests.get("http://random.birb.pw/tweet.json")
                    bird = json.loads(response.text)
                    self.sendRemoteImage("https://random.birb.pw/img/" + bird["file"], None, thread_id, thread_type)

            if message_object.text[0:15].lower() == "poprosze tencze":
                if author_id == mojeid:
                    for i in range(10):
                        self.changeThreadColor(random.choice(kolorki), thread_id)
                    self.changeThreadColor(ThreadColor.BRILLIANT_ROSE, thread_id)
                    self.changeThreadColor(ThreadColor.BRILLIANT_ROSE, thread_id)
                else:
                    self.send(Message("Sam sobie zrób tęczę."), thread_id, thread_type)
                    
            elif message_object.text.lower() == "czas":
                now = datetime.datetime.now()
                tera = now.strftime("%A %d %B %H:%M")
                tera = tera.replace("September", "Września")
                tera = tera.replace("August", "Sierpnia")
                tera = tera.replace("October", "Października")
                tera = tera.replace("November", "Listopada")
                tera = tera.replace("Saturday", "Sobota")
                tera = tera.replace("Sunday", "Niedziela")
                tera = tera.replace("Monday", "Poniedziałek")
                tera = tera.replace("Tuesday", "Wtorek")
                tera = tera.replace("Wednesday", "Środa")
                tera = tera.replace("Thursday", "Czwartek")
                tera = tera.replace("Friday", "Piątek")
                czas = round(time.time())-3600
                czasdoswiat = 1545429600 - czas
                czasdowakacji = 1561068000 - czas
                wiadomosc = "Jest: " + tera + "\nPoczątek przerwy świątecznej (22 grudnia) za: " + str(int((czasdoswiat - czasdoswiat % 86400) / 86400)) + "dni " + time.strftime("%Hh %Mmin %Ssek", time.gmtime(int(round(czasdoswiat))))\
                            + "\nKoniec roku szkolnego za: " + str(int((czasdowakacji - czasdowakacji % 86400) / 86400)) + "dni " + time.strftime("%Hh %Mmin %Ssek", time.gmtime(int(round(czasdowakacji))))
                self.send(Message(wiadomosc), thread_id, thread_type)
            elif message_object.text.lower() == "grek":
                if message_object.text == "Grek":
                    self.send(Message("grek*"), thread_id, thread_type)
                self.send(Message("to pedał"), thread_id, thread_type)
            elif message_object.text.lower() == "!shiba":
                response = requests.get("https://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true")
                shiba = json.loads(response.text)
                self.sendRemoteImage(shiba[0], None, thread_id, thread_type)
            elif message_object.text.lower() == "pedał":
                self.send(Message("sam jesteś grek"), thread_id, thread_type)
            elif message_object.text.lower() == "pedał to":
                self.send(Message("grek"), thread_id, thread_type)
            elif message_object.text.lower() == "!panda":
                self.sendLocalImage("pandy/" + random.choice(os.listdir("pandy")), None, thread_id, thread_type)
            elif message_object.text.lower() == "!ile":
                self.send(Message("Odkąd mnie dodano napisano "+str(self.fetchThreadInfo(thread_id)[thread_id].message_count)+" wiadomości"), thread_id, thread_type)
            elif message_object.text.lower() == "ping":
                self.send(Message("Pong!"), thread_id, thread_type)
            elif message_object.text.lower() == "pong":
                self.send(Message("Ping!"), thread_id, thread_type)
            elif message_object.text == "🤔":
                self.send(Message("🤔"), thread_id, thread_type)
            elif message_object.text.lower() == "!kod":
                self.send(Message("https://github.com/kugo12/WiertarBot"), thread_id, thread_type)
              
            if author_id == mojeid or author_id == korsan or author_id == swider:
                if "@everyone" in message_object.text.lower():
                    self.send(Message("@everyone", self.mentions(thread_id)), thread_id, thread_type)

            if "1337" in message_object.text:
                if author_id == mojeid:
                    self.send(Message("Jesteś Elitą"), thread_id, thread_type)
                else:
                    self.send(Message("Nie jesteś Elitą"), thread_id, thread_type)

            if "2137" in message_object.text:
                self.send(Message("haha toż to papieżowa liczba"), thread_id, thread_type)
              
            if message_object.text.lower() == "barka":
                self.send(Message(barka), thread_id, thread_type)

            if "xd" in message_object.text.lower():
                if "Xd" in message_object.text:
                    self.reactToMessage(mid, MessageReaction.ANGRY)
                elif (thread_id != ryz) or self.ryz_commands is True:
                    self.reactToMessage(mid, MessageReaction.SMILE)
                    
            if thread_id != meine:
                if "wiertarbot" in message_object.text.lower():
                    self.send(Message("Spierdalaj"), thread_id, thread_type)
                    self.reactToMessage(mid, MessageReaction.ANGRY)
                elif "wiertarski" in message_object.text.lower():
                    self.send(Message("Spierdalaj"), thread_id, thread_type)
                    self.reactToMessage(mid, MessageReaction.ANGRY)
                
            if "spierdalaj" == message_object.text.lower():
                self.send(Message("sam spierdalaj"), thread_id, thread_type)
                self.reactToMessage(mid, MessageReaction.ANGRY)
            elif message_object.text.lower()[0:3] == "sam" and message_object.text.lower().endswith("spierdalaj"):
                t = message_object.text.lower().replace("sam", "")
                t = t.replace(" ", "")
                t = t.replace("spierdalaj", "")
                if t == "" and message_object.text.lower().count("spierdalaj") == 1:
                    message = "sam "
                    for i in range(message_object.text.lower().count("sam")):
                        message += "sam "
                    message += "spierdalaj"
                    self.send(Message(message), thread_id, thread_type)
                    self.reactToMessage(mid, MessageReaction.ANGRY)

            if thread_id == ryz:
                if author_id == mojeid or author_id == korsan:
                    if message_object.text[0:9] == "!komendy ":
                        text = message_object.text.replace("!komendy ", "")
                        if text == "tak" and self.ryz_commands is not True:
                            self.ryz_commands = True
                            self.send(Message("Komendy zostały włączone"), ryz, thread_type)
                        elif text == "nie" and self.ryz_commands is True:
                            self.ryz_commands = False
                            self.send(Message("Komendy zostały wyłączone"), ryz, thread_type)
                if message_object.text.lower() == "!komendy":
                    if self.ryz_commands is True:
                        self.send(Message("Komendy są włączone"), ryz, thread_type)
                    else:
                        self.send(Message("Komendy są wyłączone"), ryz, thread_type)

            if thread_id != ryz or author_id == mojeid:
                if message_object.text.lower()[0:8] == "!pogoda ":
                    city = message_object.text.lower().replace("!pogoda ", "")
                    if thread_id == meine or author_id == mojeid:
                        response = requests.get("http://dataservice.accuweather.com/locations/v1/cities/search?apikey="+self.weather_key+"&q="+city+"&language=pl-PL&details=false")
                        city_id = json.loads(response.text)
                        if city_id == []:
                            self.send(Message("Taka miejscowość nie istnieje, lub dzienny limit został wyczerpany\ngoogle.com/search?q=pogoda+"+city), thread_id, thread_type)
                        else:
                            city_id = city_id[0]["Key"]
                            response = requests.get("http://dataservice.accuweather.com/currentconditions/v1/"+city_id+"?apikey=EBvzyH6oZrG2g6AvNTEnIXORieRaNIAR&language=pl-PL&details=true")
                            pogoda = json.loads(response.text)[0]
                            message = "Pogoda w mieście: "+city+"\n"+str(pogoda["WeatherText"])
                            message += "\nTemperatura teraz: "+str(pogoda["Temperature"]["Metric"]["Value"])+"°C\nOdczuwalna: "+str(pogoda["RealFeelTemperature"]["Metric"]["Value"])+"°C\n"
                            message += "Wilgotność: "+str(pogoda["RelativeHumidity"])
                            message += "%\nCiśnienie: "+str(pogoda["Pressure"]["Metric"]["Value"])+"hPa\nZachmurzenie: "+str(pogoda["CloudCover"])+"%"
                            self.send(Message(message), thread_id, thread_type)
                    else:
                        self.send(Message("google.com/search?q=pogoda+"+city), thread_id, thread_type)
                elif message_object.text.lower() == "!suchar":
                    response = requests.get("http://sucharyy.pl/losuj")
                    if response.status_code == 404:
                        self.send(Message("Nie ma takiej strony"), thread_id, thread_type)
                    else:
                        parsed = BeautifulSoup(response.text, "html.parser")
                        suchar = parsed.body.find("article", "natresc").get_text()
                        self.send(Message(suchar), thread_id, thread_type)
                    response, parsed, suchar = None, None, None
                elif message_object.text.lower()[0:9] == "!miejski ":
                    word = message_object.text.replace("!miejski ", "")
                    self.send(Message(urban_dictionary(word)), thread_id, thread_type)
                    word = None
                elif message_object.text == "!Xd":
                    self.send(Message(
                        "Serio, mało rzeczy mnie triggeruje tak jak to chore \"Xd\". Kombinacji x i d można używać na wiele wspaniałych sposobów. Coś cię śmieszy? Stawiasz \"xD\". Coś się bardzo śmieszy? Śmiało: \"XD\"! Coś doprowadza Cię do płaczu ze śmiechu? \"XDDD\" i załatwione. Uśmiechniesz się pod nosem? \"xd\". Po kłopocie. A co ma do tego ten bękart klawiaturowej ewolucji, potwór i zakała ludzkiej estetyki - \"Xd\"? Co to w ogóle ma wyrażać? Martwego człowieka z wywalonym jęzorem? Powiem Ci, co to znaczy. To znaczy, że masz w telefonie włączone zaczynanie zdań dużą literą, ale szkoda Ci klikać capsa na jedno \"d\" później. Korona z głowy spadnie? Nie sondze. \"Xd\" to symptom tego, że masz mnie, jako rozmówcę, gdzieś, bo Ci się nawet kliknąć nie chce, żeby mi wysłać poprawny emotikon. Szanujesz mnie? Używaj \"xd\", \"xD\", \"XD\", do wyboru. Nie szanujesz mnie? Okaż to. Wystarczy, że wstawisz to zjebane \"Xd\" w choć jednej wiadomości. Nie pozdrawiam"),
                              thread_id, thread_type)
                elif message_object.text.lower() == "!mem":
                    rand = random.choice(memy)
                    if rand == "memy":
                        response = requests.get("http://memy.pl/losuj")
                        if response.status_code == 404:
                            self.send(Message("Nie ma takiej strony"), thread_id, thread_type)
                        else:
                            parsed = BeautifulSoup(response.text, "html.parser")
                            img = parsed.body.find("a", "img-responsive").find("img")["src"]
                            self.sendRemoteImage(img, None, thread_id, thread_type)
                    elif rand == "demotywatory":
                        response = requests.get("https://demotywatory.pl/losuj")
                        if response.status_code == 404:
                            self.send(Message("Nie ma takiej strony"), thread_id, thread_type)
                        else:
                            parsed = BeautifulSoup(response.text, "html.parser")
                            img = parsed.body.find("img", "demot")
                            self.sendRemoteImage(img["src"], None, thread_id, thread_type)
                    elif rand == "jeja":
                        response = requests.get("https://memy.jeja.pl/losowe")
                        if response.status_code == 404:
                            self.send(Message("Nie ma takiej strony"), thread_id, thread_type)
                        else:
                            parsed = BeautifulSoup(response.text, "html.parser")
                            img = parsed.body.find("img", ["ob-left-image", "ob-image-j"])["src"]
                            self.sendRemoteImage(img, None, thread_id, thread_type)
                    img, parsed, response = None, None, None


bot = SmakuBot(email, password)
bot.listen()