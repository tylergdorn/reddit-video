import requests
import praw
import yaml
from gtts import gTTS

credentials = {}
with open('creds.yaml') as f:
    credentials = yaml.safe_load(f)
assert len(credentials) == 5, "failed to load credentials"

reddit = praw.Reddit(client_id=credentials["client_id"], client_secret=credentials["client_secret"], password=credentials["password"], username=credentials["username"], user_agent=credentials["user_agent"])
audio_dir = './audio/'

for dumb_post in reddit.subreddit('askreddit').top('day', limit=2):
    print(dumb_post.title)
    dumb_post.comments.replace_more(0)
    # We may care to read the selftext eventually, but they usually suck anyway
    post_tts = gTTS(dumb_post.title, lang='en')
    post_tts.save(f'{audio_dir}{dumb_post.id}.mp3')

    for dumb_comment in dumb_post.comments.list()[:5]:
        print(dumb_comment.id)
        tts = gTTS(dumb_comment.body, lang='en')
        tts.save(f'{audio_dir}{"".join([x for x in dumb_post.title if x.isalnum()])} - {dumb_comment.id}.mp3')