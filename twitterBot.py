import os
import tweepy
import openai
import time
import requests
from datetime import datetime

# Function to load environment variables from a .env file
def load_env_file(file_path=".env"):
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key] = value
        print("Environment variables loaded successfully.")
    else:
        print(f"{file_path} not found.")

# Load environment variables
load_env_file()

# Twitter and OpenAI API Keys (Make sure these are securely stored in your .env file)
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Debugging: Ensure the keys are loaded properly
def debug_keys():
    print(f"API_KEY: {API_KEY}")
    print(f"API_SECRET_KEY: {API_SECRET_KEY}")
    print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
    print(f"ACCESS_TOKEN_SECRET: {ACCESS_TOKEN_SECRET}")
    print(f"BEARER_TOKEN: {BEARER_TOKEN}")
    print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

debug_keys()

if not all([API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, OPENAI_API_KEY]):
    print("One or more API keys are missing.")
else:
    print("API keys loaded successfully.")

# Twitter API Authentication
# Initialize Tweepy Client for API v2
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    bearer_token=BEARER_TOKEN
)

# Initialize Tweepy API for v1.1 (for media upload)
auth = tweepy.OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)
api_v1 = tweepy.API(auth)

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Function to generate tweet using OpenAI
def generate_tweet():
    try:
        messages = [{"role": "user", "content": "Write a tweet about latest crypto news or about meme coins using 20-50 words."}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50,
            temperature=0.7
        )
        tweet_content = response['choices'][0]['message']['content'].strip()
        print(f"Generated tweet: {tweet_content}")
        return tweet_content
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return None

# Function to generate image using DALL-E
def generate_image(prompt="A futuristic crypto-themed digital artwork"):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        print(f"Generated image URL: {image_url}")
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

# Function to download an image from a URL
def download_image(image_url, save_path="generated_image.jpg"):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"Image downloaded successfully: {save_path}")
            return save_path
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

# Function to post a tweet with an image
def post_tweet_with_image():
    try:
        tweet_content = generate_tweet()
        if tweet_content:
            image_prompt = "Any image related to cryptocurrency"
            image_url = generate_image(prompt=image_prompt)

            if image_url:
                image_path = download_image(image_url)
                if image_path:
                    media = api_v1.media_upload(image_path)
                    response = client.create_tweet(
                        text=tweet_content,
                        media_ids=[media.media_id_string]
                    )
                    print(f"Tweet posted with image: {response.data['id']}")
                    return response.data['id']
    except tweepy.TweepyException as e:
        print(f"Error occurred while posting tweet: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

# Function to generate reply using OpenAI
def generate_reply(comment_text):
    try:
        messages = [{"role": "user", "content": f"Reply to this comment: {comment_text}"}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=50,
            temperature=0.4
        )
        reply_text = response['choices'][0]['message']['content'].strip()
        print(f"Generated reply: {reply_text}")
        return reply_text
    except Exception as e:
        print(f"Error generating reply: {e}")
        return None

# Function to reply to comments on the tweet
# Track the last processed mention ID to avoid replying to the same comment multiple times
last_mention_id = None

def reply_to_comments(tweet_id):
    global last_mention_id  # Use a global variable to persist the last mention ID
    try:
        user_id = client.get_me().data['id']

        # Fetch recent mentions
        response = client.get_users_mentions(
            id=user_id,
            since_id=last_mention_id,  # Fetch mentions since the last processed one
            tweet_fields=["author_id", "text", "created_at", "in_reply_to_user_id", "id"]
        )

        if response.data:
            for mention in sorted(response.data, key=lambda x: x.id):  # Sort mentions by ID to reply in order
                if mention.in_reply_to_user_id == user_id:  # Ensure it's a reply to the bot
                    print(f"New mention from {mention.author_id}: {mention.text}")
                    reply_text = generate_reply(mention.text)  # Generate a reply using OpenAI
                    client.create_tweet(
                        text=f"@{mention.author_id} {reply_text}",
                        in_reply_to_tweet_id=mention.id
                    )
                    print(f"Replied to @{mention.author_id} with: {reply_text}")

                    # Update the last mention ID after processing
                    last_mention_id = mention.id
        else:
            print("No new mentions found.")
    except tweepy.TweepyException as e:
        print(f"Error occurred while replying to comments: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Function to run the bot
def run_bot():
    while True:
        try:
            # Post a tweet with an image
            print("Generating and posting a new tweet with an image...")
            post_tweet_with_image()

            # Wait for 2 minutes before replying to comments or generating the next tweet
            print("Waiting for 3 minutes before the next operation...")
            time.sleep(180)

            # Check for comments and reply
            print("Checking for mentions to reply to...")
            tweet_id = client.get_me().data['id']  # Get the bot's user ID
            reply_to_comments(tweet_id)

            # Wait for another 2 minutes before restarting the loop
            print("Waiting for 2 minutes before generating the next tweet...")
            time.sleep(120)
        except Exception as e:
            print(f"Unexpected error occurred in the bot loop: {e}")
            time.sleep(120)  # Wait and continue in case of an error
