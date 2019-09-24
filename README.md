# Shino
### What is Shino?
Shino, is an open source discord modmail bot written in python, with this code you can make your moderation life easier!

### How to use it?
To use Shino you need to follow this steps.
1. Download python : [Python](https://www.python.org/downloads/) 
  -![#FF0000](https://placehold.it/15/f03c15/000000?text=+) `Version : 3.xx` <br />
  -![#FF0000](https://placehold.it/15/f03c15/000000?text=+) `Make sure to check add to path when installing!`
2. Open command prompt and type this:
  -`pip install -r requirements.txt` or  `pip3 install -r requirements.txt`
3. Go to Discord Developer Portal : [Discord Developer Portal](https://discordapp.com/developers/applications/) 
  - Click `New Application`.<br />
    ![NewApp](https://i.imgur.com/J3y4cSf.png)
  - Choose a name and a photo...
  - Go to `Bot` <br />
    ![NewApp](https://i.imgur.com/xodpdZM.png)
  - Add Bot. <br /> 
  - Go to *Token* and click `Copy` <br />
    ![NewApp](https://i.imgur.com/GyvGg8S.png)
4. Now go to Shino folder and open `token.txt`, and past the token.
5. Open command prompt, move to Shino directory then type : `python main.py`
6. The bot should run, if you need any help please contact me on discord: Drake.#1112
7. Invite the bot to your server.
  - Go to Discord Developer Portal : [Discord Developer Portal](https://discordapp.com/developers/applications/)
  - Switch yo your app, general information then copy client id.
  - Replace `[client_id]` with your client id : https://discordapp.com/oauth2/authorize?client_id=*[client_id]*&permissions=8&scope=bot 
** Notice **: you need to make sure that the bot is running before inviting it to your server, if you invited it first, kick it, run it then invite it back.  

### Shino's System

#### System explained : 
After joining the server, the bot needs to make some configuration, necessary roles, categories... and in order to do that after joining the server you need to do : `?config`. After that the bot should run without problems.
##### Commands:
1. **?config** : Makes necessary configuration for the bot.
2. **?md** : Open a modmail request.
3. **?help [optional: md, config]** Asks for help in DMS.
##### Prefix:
To change the bot's prefix you need to go to Shino's directory then to main.py, open it with a text editor and change:
```python
prefix = '?'
```
with your wanted prefix, and make sure you don't remove the "".






