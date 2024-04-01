import re
from telethon.tl import types

## Helper function for get_message
    
async def get_entity(event, entity):
    """Get chat entity from entity parameter"""
    if entity.isdigit() or entity.startswith("-"):
        chat = types.PeerChannel(int(entity))
    else:
        try:
            chat = await event.client.get_entity(entity)
        except Exception as e:
            chat = await event.client.get_entity(types.PeerChat(int(entity)))

    return chat


async def loop_message(event, chat, ids: int, next=True):
    """Loop channel posts to get message"""
    skip = 20
    tries = 0
    while True:
        if ids > 0 and tries <= skip:
            message = await event.client.get_messages(chat, ids=ids)
            tries += 1
            if not message:
                if next:
                    ids += 1
                    continue
                else:
                    ids -= 1
                    continue
            else:
                if hasattr(message, 'message'):
                    if message.media and not (message.sticker or message.voice or message.web_preview):
                        return message
                ids = ids + 1 if next else ids - 1
        else:
            return


## Helper function for turn into telegraph
        
# async def hentaifox_to_telegraph(kode):
#     from test_tele.features.extractors.ehentai import get_img_list_gellerydl
#     lists = await get_img_list_gellerydl(kode)


## Helper to check if user is in a group
        
async def is_bot_in_group(event):
    """
    Check if the bot is running in a group.

    Args:
        client (TelegramClient): The Telegram client.
        event (Message): The message event.

    Returns:
        bool: True if the bot is running in a group, False otherwise.
    """

    chat = await event.client.get_entity(event.chat_id)
    return chat.megagroup


async def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return youtube_regex_match

    return youtube_regex_match


async def instagram_url_validation(url):
    instagram_regex = (
        r'(https?://)?(www\.)?'
        r'(instagram.com)/'
        r'(p/[^&=%\?]{1,}|[^&=%\?]{1,}highlights/[^&=%\?]{1,17})')

    instagram_regex_match = re.match(instagram_regex, url)
    if instagram_regex_match:
        return instagram_regex_match

    return instagram_regex_match