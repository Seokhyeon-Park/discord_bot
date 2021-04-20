# ref[1] -  https://softvanilla.github.io/discordbot/discord_%EC%8B%9C%EC%9E%91/
#           (*Set discord bot, Korean document[blog])

import discord
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import random

# TOKEN : Discord token
# Your discord token, Refer to *ref[1]
TOKEN = ""

client = discord.Client()

# based on fow.kr
# league of legends(Kor server) rank, point, win rate searching
def searching(name):
    try:
        name = name
        # 
        # driver = webdriver.Chrome("")
        # driver.get("http://fow.kr/find/"+name)
        # refresh_button = driver.find_element_by_link_text("갱신가능")
        # refresh_button.click()
        # driver.quit()
        #
        req = requests.get("http://fow.kr/find/"+name)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        #
        div_text = soup.find_all('div', {'class' : 'table_summary'})
        #
        point_len = len("</font></b><br/>")
        rank = str(div_text[0])[str(div_text[0]).find('228822">')+8:str(div_text[0]).find('</font></b><br/>')]
        point = str(div_text[0])[str(div_text[0]).find('</font></b><br/>')+point_len+10:str(div_text[0]).find('</font></b><br/>')+point_len+15]
        point = re.findall("\d+", point)
        rate = str(div_text[0]).index('%)')
        #
        lol = "===================\nUser : " + name + "\nRank : " + rank + "\nPoint : " + point[0] + "p" + "\nWin rate : " + str(div_text[0])[rate-5:rate] + " %"
        error = "배치 or Error"
        return lol
    except:
        error = "배치 or Error"
        return error

@client.event
async def on_ready():
    print(f'{client.user} online!')

@client.event
async def on_message(message):
    #
    if message.author == client.user:
        return
    # league of legends search.
    if message.content.startswith("!lol"):
        name = message.content[5:len(message.content)]
        if len(message.content) < 30:
            result = searching(name)
            await message.channel.send(result)
        else:
            game_member = message.content[5:len(message.content)]
            game_member = game_member.replace("님이 로비에 참가하셨습니다.","")
            member_list = game_member.split("\n")
            for name in member_list:
                result = searching(name)
                await message.channel.send(result)
    # Channel text bot
    if message.content == "command":
        await message.channel.send("TEXT")
    # Emoji(img, gif things)
    if message.content == command_list[4]:
        await message.channel.send(file=discord.File('text.gif'))

# running bot
client.run(TOKEN)
