# Telegram Bots on Python

## Table of Contents
- [What is a Telegram Bot](#what-is-telegram-bot)
- [Demo bots](#demo-bots)
- [Word Meaning Bot](#word-meaning-bot)
- [Host bots](#host-bots)

## What is a Telegram Bot
Bots are small applications that run entirely within the Telegram app. Users interact with bots through flexible interfaces that can support any kind of task or service. 

_You can read more about bots in the official documentation:_   
[Bots](https://core.telegram.org/bots)   
[Telegram Bot API](https://core.telegram.org/bots/api)

## [Demo Bots](https://github.com/dkoleev/telegram-bots/tree/main/demo)
Demo bots from python-telegram-bot [Examples](https://docs.python-telegram-bot.org/en/stable/examples.html)

## [Word Meaning Bot](https://github.com/dkoleev/telegram-bots/blob/main/word_meaning_bot.py)
This bot shows phonetic, meaning, and pronunciations for entered words.

### How to use:
1. Find this bot in Telegram by the name `@WordExplainBot`.
2. Enter the word you need the explanation in the chat with the bot.
![](https://gyazo.com/063fe2ec8ecf8278e78c3dc045f69f24)

### How it works:
This bot uses [Free Dictionary API](https://dictionaryapi.dev/).

After getting a message from a user, the bot sends the request to `Free Dictionary API`

```python3

def get_meaning(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return format_respone(data)
    else:
        return f"Sorryy, I couldn't find the meaning of '{word}'."
```

Parse the result and send it back to the user.

## Host bots
You can host your bots on a `third-party host` or `your own`.

### Third-party hosts
There are many choices for hosts. For example:
* Heroku
* [PythonAnywhere](https://www.pythonanywhere.com/)
* AWS (Amazon Web Services)
* Google Cloud Platform

I'd recommend you start with `PythonAnywhere` because of its simplicity and free plan. 

### Own host
I use [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) for hosting my bots.
