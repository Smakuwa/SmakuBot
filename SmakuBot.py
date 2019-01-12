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
korsan = "100001699215604"
swider = "100007813848151"
zeus = "100001699215604"

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
        if author_id == mojeid or author_id == zeus:
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

            if (author_id == mojeid) or (author_id == zeus) or self.ryz_commands is True:
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
                elif message_object.text.lower() == "!random":
                    response = requests.get("https://picsum.photos/200/300/?random")
                    random = json.loads(response.text)
                    self.sentRemoteImage(random["message"], None, thread_id, thread_type)
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
            elif message_object.text == "papież pedał":
                self.reactToMessage(mid, MessageReaction.ANGRY)
                self.send(Message("dzieci jebał"), thread_id, thread_type)
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

            if author_id == mojeid:
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
                elif message_object.text == "!rigcz":
                    self.send(Message(
                        "no i ja się pytam człowieku dumny ty jesteś z siebie zdajesz sobie sprawę z tego co robisz?masz ty wogóle rozum i godnośc człowieka?ja nie wiem ale żałosny typek z ciebie ,chyba nie pomyślałes nawet co robisz i kogo obrażasz ,możesz sobie obrażac tych co na to zasłużyli sobie ale nie naszego papieża polaka naszego rodaka wielką osobę ,i tak wyjątkowa i ważną bo to nie jest ktoś tam taki sobie że możesz go sobie wyśmiać bo tak ci się podoba nie wiem w jakiej ty się wychowałes rodzinie ale chyba ty nie wiem nie rozumiesz co to jest wiara .jeśli myslisz że jestes wspaniały to jestes zwykłym czubkiem którego ktoś nie odizolował jeszcze od społeczeństwa ,nie wiem co w tym jest takie śmieszne ale czepcie się stalina albo hitlera albo innych zwyrodnialców a nie czepiacie się takiej świętej osoby jak papież jan paweł 2 .jak można wogóle publicznie zamieszczac takie zdięcia na forach internetowych?ja się pytam kto powinien za to odpowiedziec bo chyba widac że do koscioła nie chodzi jak jestes nie wiem ateistą albo wierzysz w jakies sekty czy wogóle jestes może ty sługą szatana a nie będziesz z papieża robił takiego ,to ty chyba jestes jakis nie wiem co sie jarasz pomiotami szatana .wez pomyśl sobie ile papież zrobił ,on był kimś a ty kim jestes żeby z niego sobie robić kpiny co? kto dał ci prawo obrażac wogóle papieża naszego ?pomyślałes wogóle nad tym że to nie jest osoba taka sobie że ją wyśmieje i mnie będa wszyscy chwalic? wez dziecko naprawdę jestes jakis psycholek bo w przeciwieństwie do ciebie to papież jest autorytetem dla mnie a ty to nie wiem czyim możesz być autorytetem chyba takich samych jakiś głupków jak ty którzy nie wiedza co to kosciół i religia ,widac że się nie modlisz i nie chodzisz na religie do szkoły ,widac nie szanujesz religii to nie wiem jak chcesz to sobie wez swoje zdięcie wstaw ciekawe czy byś sie odważył .naprawdę wezta się dzieci zastanówcie co wy roicie bo nie macie widac pojęcia o tym kim był papież jan paweł2 jak nie jestescie w pełni rozwinięte umysłowo to się nie zabierajcie za taką osobę jak ojciec swięty bo to świadczy o tym że nie macie chyba w domu krzyża ani jednego obraza świętego nie chodzi tutaj o kosciół mnie ale wogóle ogólnie o zasady wiary żeby mieć jakąs godnosc bo papież nikogo nie obrażał a ty za co go obrażasz co? no powiedz za co obrażasz taką osobę jak ojciec święty ?brak mnie słów ale jakbyś miał pojęcie chociaz i sięgnął po pismo święte i poczytał sobie to może byś się odmienił .nie wiem idz do kościoła bo widac już dawno szatan jest w tobie człowieku ,nie lubisz kościoła to chociaż siedz cicho i nie obrażaj innych ludzi"),
                              thread_id, thread_type)
                elif message_object.text == "!fanatyk":
                    self.send(Message(
                        "Mój stary to fanatyk wędkarstwa. Pół mieszkania zajebane wędkami najgorsze. Średnio raz w miesiącu ktoś wdepnie w leżący na ziemi haczyk czy kotwicę i trzeba wyciągać w szpitalu bo mają zadziory na końcu. W swoim 22 letnim życiu już z 10 razy byłem na takim zabiegu. Tydzień temu poszedłem na jakieś losowe badania to baba z recepcji jak mnie tylko zobaczyła to kazała buta ściągać xD bo myślała, że znowu hak w nodze. Druga połowa mieszkania zajebana Wędkarzem Polskim, Światem Wędkarza, Super Karpiem xD itp. Co tydzień ojciec robi objazd po wszystkich kioskach w mieście, żeby skompletować wszystkie wędkarskie tygodniki. Byłem na tyle głupi, że nauczyłem go into internety bo myślałem, że trochę pieniędzy zaoszczędzimy na tych gazetkach ale teraz nie dosyć, że je kupuje to jeszcze siedzi na jakichś forach dla wędkarzy i kręci gównoburze z innymi wędkarzami o najlepsze zanęty itp. Potrafi drzeć mordę do monitora albo wypierdolić klawiaturę za okno. Kiedyś ojciec mnie wkurwił to założyłem tam konto i go trolowałem pisząc w jego tematach jakieś losowe głupoty typu karasie jedzo guwno. Matka nie nadążała z gotowaniem bigosu na uspokojenie. Aha, ma już na forum rangę SUM, za najebanie 10k postów. Jak jest ciepło to co weekend zapierdala na ryby. Od jakichś 5 lat w każdą niedzielę jem rybę na obiad a ojciec pierdoli o zaletach jedzenia tego wodnego gówna. Jak się dostałem na studia to stary przez tydzień pie**olił że to dzięki temu, że jem dużo ryb bo zawierają fosfor i mózg mi lepiej pracuje. Co sobotę budzi ze swoim znajomym mirkiem całą rodzinę o 4 w nocy bo hałasują pakując wędki, robiąc kanapki itd. Przy jedzeniu zawsze pierdoli o rybach i za każdym razem temat schodzi w końcu na Polski Związek Wędkarski, ojciec sam się nakręca i dostaje strasznego bólu dupy durr niedostatecznie zarybiajo tylko kradno hurr, robi się przy tym cały czerwony i odchodzi od stołu klnąc i idzie czytać Wielką Encyklopedię Ryb Rzecznych żeby się uspokoić. W tym roku sam sobie kupił na święta ponton. Oczywiście do wigilii nie wytrzymał tylko już wczoraj go rozpakował i nadmuchał w dużym pokoju. Ubrał się w ten swój cały strój wędkarski i siedział cały dzień w tym pontonie na środku mieszkania. Obiad (karp) też w nim zjadł [cool][cześć] Gdybym mnie na długość ręki dopuścili do wszystkich ryb w polsce to bym wziął i zapierdolił. Jak któregoś razu, jeszcze w podbazie czy gimbazie, miałem urodziny to stary jako prezent wziął mnie ze sobą na ryby w drodze wyjątku. Super prezent kurwo. Pojechaliśmy gdzieś wpizdu za miasto, dochodzimy nad jezioro a ojcu już się oczy świecą i oblizuje wargi podniecony. Rozłożył cały sprzęt i siedzimy nad woda i patrzymy na spławiki. Po pięciu minutach mi się znudziło więc włączyłem discmana to mnie ojciec pierdolnął wędką po głowie, że ryby słyszą muzykę z moich słuchawek i się płoszą. Jak się chciałem podrapać po dupie to zaraz krzyczał szeptem, żebym się nie wiercił bo szeleszczę i ryby z wody widzą jak się ruszam i uciekają. 6 godzin musiałem siedzieć w bezruchu i patrzeć na wodę jak w jakimś jebanym Guantanamo. Urodziny mam w listopadzie więc jeszcze do tego było zimno jak sam skurwysyn. W pewnym momencie ojciec odszedł kilkanaście metrów w las i się spierdział. Wytłumaczył mi, że trzeba w lesie pierdzieć bo inaczej ryby słyszą i czują. Wspomniałem, że ojciec ma kolegę mirka, z którym jeździ na ryby. Kiedyś towarzyszem wypraw rybnych był hehe Zbyszek. Człowiek o kształcie piłki z wąsem i 365 dni w roku w kamizelce BOMBER. Byli z moim ojcem prawie jak bracia, przychodził z żoną Bożeną na wigilie do nas itd. Raz ojciec miał imieniny zbysio przyszedł na hehe kielicha. Najebali się i oczywiście cały czas gadali o wędkowaniu i rybach. Ja siedziałem u siebie w pokoju. W pewnym momencie zaczeli drzeć na siebie mordę, czy generalnie lepsze są szczupaki czy sumy. WEŹ MNIE NIE WKURWIAJ ZBYCHU, WIDZIAŁEŚ TY KIEDYŚ JAKIE SZCZUPAK MA ZĘBY? CHAPS I RĘKA UJEBANA! KURWA TADEK SUMY W POLSCE PO 80 KILO WAŻĄ, TWÓJ SZCZUPAK TO IM MOŻE NASKOCZYĆ CO TY MI O SUMACH PIERDOLISZ JAK LEDWO UKLEJĘ POTRAFISZ Z WODY WYCIĄGNĄĆ. SZCZUPAK TO JEST KRÓL WODY JAK LEW JEST KRÓL DŻUNGLI. No i aż się zaczeli nakurwiać zapasy na dywanie w dużym pokoju a ja z matką musieliśmy ich rodzielać. Od tego czasu zupełnie zerwali kontakt. W zeszłym roku zadzwoniła żona zbysia, że zbysio spadł z rowerka i zaprasza na pogrzeb. Odebrała akurat matka, złożyła kondolencje, odkłada słuchawkę i mówi o tym ojcu, a ojciec I bardzo kurwa dobrze. Tak go za tego suma znienawidził. Wspominałem też o arcywrogu mojego starego czyli Polskim Związku Wędkarskim. Stał się on kompletną obsesją ojca i jak np. w telewizji mówią, że gdzieś był trzęsienie ziemi to stary zawsze mamrocze pod nosem, że powinni w końcu coś o tych skurwysynach z PZW powiedzieć. Gazety niewędkarskie też przestał czytać bo miał ból dupy, że o wędkarstwie polskim ani aferach w PZW nic się nie pisze. Szefem koła PZW w mojej okolicy jest niejaki pan Adam. Jest on dla starego uosobieniem całego zła wyrządzonego polskim akwenom przez Związek i ojciec przez wiele lat toczył z nim wojnę. Raz poszedł na jakieś zebranie wędkarskie gdzie występował Adam i stary wrócił do domu z podartą koszulą bo siłą go usuwali z sali takie tam inby odpierdalał. Po klęsce w starciu fizycznym ze zbrojnym ramieniem PZW ojciec rozpoczął partyzantkę internetową polegającą na szkalowaniu PZW i Adama na forach lokalnych gazet. Napierdalał na niego jakieś głupoty typu, że Adam był tajnym współpracownikiem UB albo, że go widział na ulicy jak komuś gwoździem samochód rysował itd. Nie nauczyłem ojca into TOR więc skończyło się bagietami za szkalowanie i stary musiał zapłacić Adamowi 2000zł. Jak płacił to przez tydzień w domu się nie dało żyć, ojciec kurwił na przekupne sądy, PZW, Adama i w ogóle cały świat. Z jego pierdolenia wynikało, że PZW jak jacyś masoni rządzi całym krajem, pociąga za szurki i ma wszędzie układy. Przeliczał też te 2000 na wędki, haczyki czy łódki i dostawał strasznego bólu dupy, ile on by mógł np. zanęty waniliowej za te 2k kupić (kilkaset kilo). Stary jakoś w zeszłym roku stwierdził, że koniecznie musi mieć łódkę do połowów bo niby wypożyczanie za drogo wychodzi i wszyscy go chcą oszukać synek na wodzie to się prawdziwe okazy łapie! tam jest żywioł! ale nie było go stać ani nie miał jej gdzie trzymać a hehe frajerem to on nie jest żeby komuś płacić za przechowywanie więc zgadał się z jakimiś wędkarzami okolicy, że kupią łódkę na spółkę, ona będzie stała u jakiegoś janusza, który ma dom a nie mieszkanie w bloku jak my, na podjeździe na przyczepie, którą ten janusz ma i się będą tą łódką dzielili albo będą jeździć łowić razem. Na początku ta kooperatywa szła nawet nieźle ale w któryś weekend ojciec się rozchorował i nie mógł z nimi jechać i miał o to olbrzymi ból dupy. Jeszcze ci jego koledzy dzwonili, że ryby biorą jak pojebane więc mój ojciec tylko leżał czerwony ze złości na kanapie i sapał z wkurwienia. Sytuację jeszcze pogarszało to, że nie miał na kogo zwalić winy co zawsze robi. W końcu doszedł do wniosku, że to niesprawiedliwe, że oni łowią bez niego bo przecież po równo się zrzucali na łódkę i w niedzielę wieczorem, jak te janusze już wróciły z wyprawy, wyszedł nagle z domu. Po godzinie wraca i mówi do mnie, że muszę mu pomóc z czymś przed domem. Wychodzę na zewnątrz a tam nasz samochód z przyczepą i łódką xD Pytam skąd on ją wziął a on mówi, że januszowi zajebał z podjazdu przed domem bo oni go oszukali i żeby łapał z nim łódkę i wnosimy do mieszkania XD Na nic się zdało tłumaczenie, że zajmie cały duży pokój. Na szczęście łódka nie zmieściła się w drzwiach do klatki więc stary stwierdził, że on ją przed domem zostawi. Za pomocą jakichś łańcuchów co były na łódce i mojej kłódki od roweru przypiął ją do latarni i zadowolony chce iść wracać do mieszkania a tu nagle przyjeżdżają 2 samochody z januszami współwłaścicielami, którzy domyślili się gdzie ich własność może się znajdować xD Zaczęła się nieziemska inba bo janusze drą mordy dlaczego łódkę ukradł i że ma oddawać a ojciec się drze, że oni go oszukali i on 500zł się składał a nie pływał w ten weekend. Ja starałem się załagodzić sytuację żeby ojciec od nich nie dostał wpierdolu bo było blisko. Po kilkunastu minutach sytuacja wyglądała tak: -Mój ojciec leży na ziemi, kurczowo trzyma się przyczepy i krzyczy, że nie odda -Janusze krzyczą, że ma oddawać -Jeden janusz ma rozjebany nos bo próbował leżącego ojca odciągnąć od łódki za nogę i dostał drugą nogą z kopa -Dwóch policjantów ciągnie ojca za nogi i mówi, że jedzie z nimi na komisariat bo pobił człowieka -We wszystkich oknach dookoła stoją sąsiedzi -Moja stara płacze i błaga ojca żeby zostawił łódkę a policjantów żeby go nie aresztowali -Ja smutnazaba.psd W końcu policjanci oderwali starego od łodzi. Ja podałem januszom kod do kłódki rowerowej i zabrali łódkę, rzucając wcześniej staremu 500zł i mówiąc, że nie ma już do łódki żadnego prawa i lepiej dla niego, żeby się nigdy na rybach nie spotkali. Matka ubłagała policjantów, żeby nie aresztowali ojca. Janusz co dostał w mordę butem powiedział, że on się nie będzie pie**olił z łażeniem po komisariatach i ma to w dupie tylko ojca nie chce więcej widzieć. Stary do tej pory robi z januszami gównoburzę na forach dla wędkarzy bo założyli tam specjalny temat, gdzie przestrzegali przed robieniem jakichkolwiek interesów z moim ojcem. Obserwowałem ten temat i widziałem jak mój ojciec nieudolnie porobił trollkonta Szczepan54 Liczba postów: 1 Ten temat założyli jacyś idioci! Znam użytkownika stary_anona od dawna i to bardzo porządny człowiek i wspaniały wędkarz! Chcą go oczernić bo zazdroszczą złowionych okazów! Potem jeszcze używał tych trollkont do prześladowania niedawnych kolegów od łódki. Jak któryś z nich zakładał jakiś temat to ojciec się tam wpie**alał na trollkoncie i np. pisał, ze ch*jowe ryby łapie i widać, że nie umie łowić xD Z tych samych trollkont udzielał się w swoich tematach i jak na przykład wrzucał zdjęcia złapanych przez siebie ryb to sam sobie pisał Noooo gratuluję okazu! Widać, że doświadczony łowca! a potem się z tego cieszył i kazał oglądać mi i starej jak go chwalą na forum."),
                              thread_id, thread_type)
                elif message_object.text == "Jak to jest byc skryba?":
                    self.send(Message(
                        "Moim zdaniem to nie ma tak, że dobrze albo że nie dobrze. Gdybym miał powiedzieć, co cenię w życiu najbardziej, powiedziałbym, że ludzi. Ekhm... Ludzi, którzy podali mi pomocną dłoń, kiedy sobie nie radziłem, kiedy byłem sam. I co ciekawe, to właśnie przypadkowe spotkania wpływają na nasze życie. Chodzi o to, że kiedy wyznaje się pewne wartości, nawet pozornie uniwersalne, bywa, że nie znajduje się zrozumienia, które by tak rzec, które pomaga się nam rozwijać. Ja miałem szczęście, by tak rzec, ponieważ je znalazłem. I dziękuję życiu. Dziękuję mu, życie to śpiew, życie to taniec, życie to miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to robisz?, skąd czerpiesz tę radość? A ja odpowiadam, że to proste, to umiłowanie życia, to właśnie ono sprawia, że dzisiaj na przykład buduję maszyny, a jutro... kto wie, dlaczego by nie, oddam się pracy społecznej i będę ot, choćby sadzić... znaczy... marchew."),
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