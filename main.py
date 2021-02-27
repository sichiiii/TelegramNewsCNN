import requests, telebot, re 
from bs4 import BeautifulSoup
from random import randint

bot = telebot.TeleBot('<TOKEN>')

@bot.message_handler(commands=['start'])
def getNewArticle(message):
    url = 'http://lite.cnn.com/en'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features="lxml")
    rand = randint(1, 100)
    selector = str(soup.select_one(f'#mount > div > div.afe4286c > ul > li:nth-child({rand})'))
    articleHref = str(re.findall("href=[\"\'](.*?)[\"\']", selector))
    articleHref = articleHref.replace("'", '')
    articleHref = articleHref.replace("[", '')
    articleHref = articleHref.replace("]", '')
    articleUrl = "http://lite.cnn.com" + articleHref
    getTextArticle(message, articleUrl)

def getTextArticle(message, articleUrl):
    getArticle = requests.get(articleUrl)
    finalSoup = BeautifulSoup(getArticle.content, features="lxml")
    final = str(finalSoup.select_one('#mount > div > div.afe4286c').get_text())
    checkLength(message, final)

def checkLength(message, final):
    if len(final) > 4096:
        for x in range(0, len(final), 4096):
            bot.send_message(message.chat.id, final[x:x+4096])
    else:
        bot.send_message(message.chat.id, final)

bot.polling(none_stop=True)
