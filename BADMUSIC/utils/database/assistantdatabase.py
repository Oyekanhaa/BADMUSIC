import random

from BADMUSIC import userbot
from BADMUSIC.core.mongo import mongodb

assistantdict = {}


# ✅ Lazy DB getter (MOST IMPORTANT)
def get_db():
    if mongodb is None:
        return None
    return mongodb.assistants


async def get_client(assistant: int):
    assistant = int(assistant)
    if assistant == 1:
        return userbot.one
    elif assistant == 2:
        return userbot.two
    elif assistant == 3:
        return userbot.three
    elif assistant == 4:
        return userbot.four
    elif assistant == 5:
        return userbot.five


async def save_assistant(chat_id, number):
    db = get_db()
    number = int(number)

    if db is None:
        assistantdict[chat_id] = number
        return

    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": number}},
        upsert=True,
    )


async def set_assistant(chat_id):
    from BADMUSIC.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant

    db = get_db()
    if db:
        await db.update_one(
            {"chat_id": chat_id},
            {"$set": {"assistant": ran_assistant}},
            upsert=True,
        )

    return await get_client(ran_assistant)


async def get_assistant(chat_id: int):
    from BADMUSIC.core.userbot import assistants

    assistant = assistantdict.get(chat_id)

    if assistant and assistant in assistants:
        return await get_client(assistant)

    db = get_db()
    if db:
        data = await db.find_one({"chat_id": chat_id})
        if data:
            got = data.get("assistant")
            if got in assistants:
                assistantdict[chat_id] = got
                return await get_client(got)

    return await set_assistant(chat_id)


async def set_calls_assistant(chat_id):
    from BADMUSIC.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant

    db = get_db()
    if db:
        await db.update_one(
            {"chat_id": chat_id},
            {"$set": {"assistant": ran_assistant}},
            upsert=True,
        )

    return ran_assistant


async def group_assistant(self, chat_id: int):
    from BADMUSIC.core.userbot import assistants

    assistant = assistantdict.get(chat_id)

    if not assistant or assistant not in assistants:
        db = get_db()
        if db:
            data = await db.find_one({"chat_id": chat_id})
            if data and data.get("assistant") in assistants:
                assistant = data["assistant"]
                assistantdict[chat_id] = assistant
            else:
                assistant = await set_calls_assistant(chat_id)
        else:
            assistant = await set_calls_assistant(chat_id)

    assistant = int(assistant)
    return getattr(self, ["one", "two", "three", "four", "five"][assistant - 1])
