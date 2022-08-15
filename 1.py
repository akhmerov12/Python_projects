from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.config import Config
from config import host, user, password, db_name



from bs4 import BeautifulSoup
import requests, fake_useragent
import vk_api
import psycopg2

class Kernel:

    def mechanism(self, connection=False):
        self.textResult.text = ""
        self.textInfo.text = ""
        if self.userAgentC.active:
            ua = fake_useragent.UserAgent()
            header = {'User-Agent': str(ua.random)}
            self.textInfo.text += header['User-Agent']
        ipSite = 'http://icanhazip.com'
        if self.userAgentC.active:
            adress = requests.get(ipSite, headers=header)
        else:
            adress = requests.get(ipSite)
        self.textInfo.text += "\n:: IP your network: %s" % adress.text
        if self.torProxieC.active:
            self.textInfo.text += ":: Connecting to the Tor network\n"
            proxie = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
        try:
            if self.userAgentC.active and self.torProxieC.active:
                adress = requests.get(ipSite, proxies=proxie, headers=header)
                connection = True
            elif self.torProxieC.active:
                adress = requests.get(ipSite, proxies=proxie)
                connection = True
        except:
            self.textInfo.text += ":: Stopping connect to the Tor network\n"
            if self.userAgentC.active:
                adress = requests.get(ipSite, headers=header)
            else:
                adress = requests.get(ipSite)
        if connection:
            self.textInfo.text += ":: Connected to the Tor network\n"
            self.textInfo.text += ":: IP Tor network: %s" % adress.text
        try:
            url = self.textSite.text
            if connection:
                if self.userAgentC.active and self.torProxieC.active:
                    page = requests.get(url, proxies=proxie, headers=header)
                elif self.torProxieC.active:
                    page = requests.get(url, proxies=proxie)
            else:
                if self.userAgentC.active:
                    page = requests.get(url, headers=header)
                else:
                    page = requests.get(url)
            self.soup = BeautifulSoup(page.text, "html.parser")
        except:
            return False
        else:
            return True




class Parse:

    def runParse(self, args):
        if ParserApp.mechanism(self):
            if self.textTag.text:
                for tag in self.soup.findAll(self.textTag.text):
                    if self.textAttribute.text:
                        if self.textAttribute.text == "wall_reply_text":
                            data = self.soup.find_all("div", {"class": "wall_reply_text"})
                            self.textResult.text += "%s\n" % data
                            break
                        else:
                            try:
                                self.textResult.text += "%s\n" % tag[self.textAttribute.text].text
                            except KeyError:
                                pass
                    else:
                        self.textResult.text += "%s\n" % str(tag)
            else:
                for tag in self.soup.findAll('html'):
                    self.textResult.text += "%s\n" % str(tag)
            self.textInfo.text += ":: Parse successfully runned."
        else:
            self.textInfo.text += ":: Invalid URL: '%s'.\n" % self.textSite.text

    def get_token(self):
        return ''

    def saveParse(self, args):
        if ParserApp.mechanism(self):

            vk_session = vk_api.VkApi(token=self.get_token())

            vk = vk_session.get_api()
            comments = []

            def take_Id(user_id, post_id, count):
                ids = vk_session.method('wall.getComments', {"owner_id": user_id, "post_id": post_id, "count": 99})
                return (ids)

            def take_comments(user_id, post_id):
                comment = (
                    vk_session.method('wall.getComments', {"owner_id": user_id, "post_id": post_id, "count": 99}))
                allIds = take_Id(self.textTag.text, post_id, 99)
                commentId = []
                for i in range(allIds['current_level_count']):
                    commentId.append(allIds['items'][i]['id'])
                if comment['count'] != 0:
                    for i in range(len(commentId)):
                        comments.append(comment['items'][i]['text'])
                        nestedComments = (vk_session.method('wall.getComments',
                                                            {"owner_id": user_id, "post_id": post_id, "count": 99,
                                                             "comment_id": commentId[i]}))
                        if nestedComments['count'] != 0:
                            for j in range(nestedComments['count']):
                                comments.append(nestedComments['items'][j]['text'])
                return (comments)

            posts = vk_session.method('wall.get', {'owner_id': self.textTag.text, 'count': 50})
            t = []
            for d in range(len(posts['items'])):
                postId = (posts['items'][d]['id'])
                postComments = take_comments(self.textTag.text, postId)
            if self.nameFile.text:
                with open(self.nameFile.text, "w", encoding="utf-8") as file:
                    t = 0
                    for j in range(len(postComments)):
                        if postComments[j] != "":
                            try:
                                connection = psycopg2.connect(
                                    host=host,
                                    user=user,
                                    password=password,
                                    database=db_name,
                                )
                                connection.autocommit = True
                                with connection.cursor() as cursor:
                                    postgres_insert_query = """INSERT INTO МАДИ(number, comments) VALUES (%s, %s);"""
                                    record_to_insert = (j - t + 1, postComments[j])
                                    cursor.execute(postgres_insert_query, record_to_insert)
                                    print(f"[INFO] Table created successfully")
                            except Exception as _ex:
                                print("[INFO] Error while working with PostgreSQL", _ex)
                            finally:
                                if connection:
                                    connection.close()
                                    print("[INFO] PostgreSQL connection closed")
                        else:
                            t += 1

    def clear(self, args):
        self.textResult.text = ""
        self.textInfo.text = ""

    def send_comment(self, args):
        vk_session = vk_api.VkApi(token=self.get_token())

        vk = vk_session.get_api()
        if(self.commentId.text != ""):
            vk_session.method('wall.createComment', {'owner_id': self.textTag.text, "post_id": self.postId.text,
                                                     "reply_to_comment": self.commentId.text, "message": self.comments.text})
        else:
            vk_session.method('wall.createComment', {'owner_id': self.textTag.text, "post_id": self.postId.text,
                                                     "message": self.comments.text})



class ParserApp(App, Kernel, Parse):

    def build(self):
        self.title = "Vk Parser"
        root = BoxLayout(orientation="horizontal", padding=5)

        left = BoxLayout(orientation="vertical")

        buttonRun = Button(text="Run in the terminal", size_hint=[1, .07], on_press=self.runParse)
        left.add_widget(buttonRun)

        self.textSite = TextInput(
            text="https://vk.com",
            multiline=False,
            font_size=17, size_hint=[1, .07],
            background_color=[1, 1, 1, .7])
        left.add_widget(self.textSite)

        gridLeft = GridLayout(size_hint=[1, .07], cols=2)

        self.nameFile = TextInput(text="result.txt", multiline=False, font_size=17)
        gridLeft.add_widget(self.nameFile)

        buttonSave = Button(text="Save in the BD", on_press=self.saveParse)
        gridLeft.add_widget(buttonSave)

        left.add_widget(gridLeft)

        self.textResult = TextInput(readonly=True)
        left.add_widget(self.textResult)

        right = BoxLayout(orientation="vertical", size_hint=[.6, 1])

        userAgentL = Label(text=": : User-agent : :", font_size=16)
        torProxieL = Label(text=": : Tor-proxies : :", font_size=16)

        self.userAgentC = Switch(size_hint=[1, .33], active=True)
        self.torProxieC = Switch(size_hint=[1, .33], active=True)

        gridRight = GridLayout(size_hint=[1, .27], cols=2)

        gridRight.add_widget(userAgentL)
        gridRight.add_widget(self.userAgentC)

        gridRight.add_widget(torProxieL)
        gridRight.add_widget(self.torProxieC)

        self.textTag = TextInput(text='', multiline=False, hint_text="id", font_size=17)

        self.commentId = TextInput(text='', multiline=False, hint_text="comment_id", font_size=17)

        self.comments = TextInput(text="", multiline=True, hint_text="comment", font_size=17)

        self.postId = TextInput(text='', multiline=False, hint_text="post_id", font_size=17)

        gridRight.add_widget(self.textTag)
        gridRight.add_widget(self.commentId)
        gridRight.add_widget(self.postId)
        gridRight.add_widget(self.comments)


        right.add_widget(gridRight)


        self.textInfo = TextInput(readonly=True, background_color=[1, 1, 1, .7])
        right.add_widget(self.textInfo)

        right.add_widget(Button(text="Отправить", size_hint=[1, .055], on_press=self.send_comment))
        right.add_widget(Button(text="Clear", size_hint=[1, .055], on_press=self.clear))

        root.add_widget(left)
        root.add_widget(right)

        return root



if __name__ == "__main__":
    ParserApp().run()