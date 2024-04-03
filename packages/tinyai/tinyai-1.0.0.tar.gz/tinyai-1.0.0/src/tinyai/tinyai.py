import pyttsx3

'''
engine.save_to_file("哈儿司令!","output.mp3")
'''

engine = pyttsx3.init()

'''
from gtts import gTTS
text = "Python语音合成包是Python中的一个强大的语音合成工具"
#将text转成语音
speech = gTTS(text, lang='zh-cn')
#保存成MP3文件
speech.save("result.mp3")
'''

#设置语速
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)
# 设置音量
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 0.25)

def say(text=''):
    #转换文本为语音
    engine.say(text)
    #执行语音
    engine.runAndWait()
    engine.stop()