import os
import logging
import asyncio
from flask import Flask, render_template, request, redirect, url_for
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# Setup logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

# Telegram Bot Token and MongoDB URI from environment variables
API_TOKEN = os.getenv("7582332724:AAGv_voD95gioLsyQnVyFP0tUsDt4T31VQQ")
MONGO_URI = os.getenv("mongodb+srv://chaiflix69:chaiflix69@chaiflix.nt5c9.mongodb.net/?retryWrites=true&w=majority&appName=chaiflix")

# Create bot client
bot = Client("movie_bot", bot_token=API_TOKEN)

# MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client["chaiflix69"]
collection = db["Telegram_files"]

# Command to start bot
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to the Movie Bot! Send a movie link to save it.")

# Command to add a movie link
@bot.on_message(filters.command("add_movie"))
async def add_movie(client, message):
    if message.reply_to_message and message.reply_to_message.text:
        movie_link = message.reply_to_message.text.strip()

        # Prepare data for MongoDB
        movie_data = {
            "movie_link": movie_link,
            "file_name": message.reply_to_message.text.split('/')[-1],  # Use the file name or any identifier
            "caption": "Movie Description",  # Placeholder for the movie description
            "file_type": "video"
        }
        
        # Insert into MongoDB
        await collection.insert_one(movie_data)
        await message.reply(f"Movie link {movie_link} added successfully!")

    else:
        await message.reply("Please reply to a message containing a movie link!")

# Flask route to show admin page
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle the movie link submission from the admin page
@app.route('/add_movie_link', methods=['POST'])
def add_movie_link():
    movie_link = request.form['movie_link']

    # Prepare movie data for MongoDB
    movie_data = {
        "movie_link": movie_link,
        "file_name": movie_link.split('/')[-1],  # Use file name from URL
        "caption": "Movie Description",  # Placeholder for the description
        "file_type": "video"
    }

    # Insert into MongoDB
    collection.insert_one(movie_data)
    return redirect(url_for('index'))

# Run the bot
if __name__ == "__main__":
    bot.run()  # Run Telegram bot in the background
    app.run(host='0.0.0.0', port=5000)  # Run the Flask app
