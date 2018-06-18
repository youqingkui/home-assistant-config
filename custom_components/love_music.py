import os
import redis
import json
import sys
import requests

from urllib.parse import quote


def get_redis_conn():
    import redis

    redis_opts = {}
    pool = redis.ConnectionPool(
        host=redis_opts.get('host', 'localhost'),
        port=int(redis_opts.get('port', 6379)),
        socket_timeout=int(redis_opts.get('timeout', 3)),
        db=int(redis_opts.get('db', 0)),
        decode_responses=True
    )
    return redis.Redis(connection_pool=pool)


def get_love_music(dir_path):
    import os
    music_files = os.listdir(dir_path)
    music_list = [file for file in music_files if file.endswith('.mp3')]
    for name in music_list:
        push_music_redis(name)
    return music_list


def push_music_redis(music_name):
    from urllib.parse import quote

    redis_conn = get_redis_conn()
    music_url = '%s/love/%s' % ('http://192.168.31.121', quote(music_name))
    redis_conn.lpush('ha:music_queue', music_url)


def pop_music_redis():
    redis_conn = get_redis_conn()
    music_url = redis_conn.lpop('ha:music_queue')
    if music_url:
        play_music(music_url)


def play_music(music_url):
    import requests
    import json

    url = "http://127.0.0.1:8123/api/services/media_player/play_media"

    querystring = {"api_password": "9kjUMqv8n6Ba"}

    payload = {
        "entity_id": "media_player.living_room_speaker",
        "media_content_id": music_url,
        "media_content_type": "music"
    }
    payload = json.dumps(payload)
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "f8f5c153-a502-4fe4-86bb-d110f2e37c1c"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    print(response.text)


# play_model = data.get('play_model', 'START')

# if play_model == 'START':
#     get_love_music('/home/pi/.homeassistant/tts/love')
#     pop_music_redis()
# elif play_model == 'NEXT':
#     pop_music_redis()

# hass.bus.fire(play_model, { "wow": "from a Python script!" })
if __name__ == '__main__':
    argv = sys.argv
    if argv:
        if argv[1] == 'START':
            get_love_music('/home/pi/.homeassistant/tts/love')
            pop_music_redis()
        elif argv[1] == 'NEXT':
            pop_music_redis()

