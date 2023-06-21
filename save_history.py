from telethon import TelegramClient, events
from pymongo import MongoClient
from datetime import datetime, timedelta

# Telegram API credentials
api_id = 20679681
api_hash = '189869dae68e7509de73279efe8c6f81'
session_name = 'anon'

app = TelegramClient(session_name, api_id, api_hash)

# MongoDB credentials
mongodb_uri = 'mongodb+srv://muhyo:yoqub080@muhyo.yo2m9vm.mongodb.net/?retryWrites=true&w=majority'
database_name = 'telegram_archive_messages'
collection_name = 'chat_messages'

# Create a MongoDB client and connect to the database
client = MongoClient(mongodb_uri)
db = client[database_name]
collection = db[collection_name]


@app.on(events.NewMessage)
async def handle_new_message(event):
    message = event.message
    sender = await app.get_entity(message.from_id)

    chat_id = message.chat_id
    user_first_name = sender.first_name
    user_username = sender.username
    text = message.text

    # Adjust the time to UTC+5
    time = message.date + timedelta(hours=5)
    formatted_date = time.strftime("%m oy %d kuni")
    formatted_time = time.strftime("Vaqt %H:%M:%S")

    # Handle the case when the user has no username
    if user_username is None:
        user_username = "Yo'q"
    else:
        user_username = "@" + user_username

    # Save the message to MongoDB
    message_data = {
        'chat_id': chat_id,
        'sender_name': user_first_name,
        'sender_username': user_username,
        'time': f"{formatted_date}. {formatted_time}",
        'text': text
    }
    collection.insert_one(message_data)

    # Retrieve the channel entity
    # channel = await app.get_entity('@muhyohistory')

    # Send the message to the channel
    # await app.send_message(channel, f"ID: **`{chat_id}`**\n"
    #                                   f"Ism: **[{user_first_name}](tg://user?id={chat_id})**\n"
    #                                   f"Username: **{user_username}**\n"
    #                                   f"Sana: **{formatted_date}**\n"
    #                                   f"Vaqt: **{formatted_time}**\n"
    #                                   f"Xabar: **{text}**")

# Start the Telethon client
with app:
    # Run the client event loop
    app.run_until_disconnected()
