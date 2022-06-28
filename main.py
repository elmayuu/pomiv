import discord
from discord.channel import VoiceChannel
from discord.player import FFmpegPCMAudio
import requests
import pydub
import time

TOKEN = ''
client = discord.Client()

voiceChannel: VoiceChannel
textChannel = 0
#speaker = [{"speaker": 2, "user": 'root'}]
queue = []
is_playing = False
flag = False
speaker = 2

@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)
    print(client.user)

@client.event
async def on_message(message):
    global voiceChannel
    global textChannel
    global queue
    global is_playing
    global flag
    global speaker
    
    if message.author.bot:
        return
    
    if message.content == '!c':
        voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
        await message.channel.send('参加したよ!')
        textChannel = message.channel
        print(message.channel)
        flag = True
        return
    
    if message.content == '!dc':
        voiceChannel.stop()
        await message.channel.send('退出したよ!')
        await voiceChannel.disconnect()
        flag = False
	return
    
    if message.content == '!about':
	await message.channel.send("https://voicevox.hiroshiba.jp/ VOICEVOX:四国めたん VOICEVOX:ずんだもん VOICEVOX:春日部つむぎ VOICEVOX:雨晴はう VOICEVOX:波音リツ VOICEVOX:玄\\
        野武宏 VOICEVOX:白上虎太郎 VOICEVOX:青山龍星 VOICEVOX:冥鳴ひまり VOICEVOX:九州そら VOICEVOX:もち子(cv 明日葉よもぎ)")
        
	arg = message.content.split(' ')
        
	if arg[0] == '!v':
	    if int(arg[1]) <= 0 and int(arg[1]) >= 20:
		return
            
            speaker = arg[1]
            
	    if message.channel == textChannel:
                if message.content.startswith('!'):
                    return
		if flag:
                    print("flag")
                    if message.author.voice.channel == voiceChannel:
                        return
                    addAudioToQueue(message.content)
                    genAudio(queue, is_playing)
                    
def addAudioToQueue(text):
    print("queue")
    queue.append(text)
    
def genAudio(queue, is_playing):
    global speaker
    print("genaudio")
    if len(queue) >= 1 and not is_playing:
        is_playing = True
        query_payload = {"text": queue[0], "key": "L1X9Q_9-G7837_l", "speaker": speaker}
        r = requests.post("https://api.su-shiki.com/v2/voicevox/audio/",
                          params=query_payload, timeout=(10.0, 300.0))
        with open("out.wav", "wb") as fp:
            fp.write(r.content)
            
        sound = pydub.AudioSegment.from_wav("out.wav")
        sound.export("out.mp3", format="mp3")
        playAudio(queue, is_playing)
        return

def playAudio(queue, is_playing):
    print("playaudio")
    time.sleep(1)
    voiceChannel.play(FFmpegPCMAudio("out.mp3"))
    del queue[0]
    is_playing = False
    genAudio(queue, is_playing)

client.run(TOKEN)
