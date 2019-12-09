import wave
import numpy
from pyaudio import PyAudio
import matplotlib.pyplot as plt
import os
import time
#from pydub import AudioSegment

def audio_processing(inputName, cutoffRatio = 0.6):
    cwd = os.getcwd()
    wf = wave.open(cwd + '\\' + 'Audios' + '\\'+ f'{inputName}.wav', 'rb')
    #参数检测
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True)
    nframes = wf.getnframes()
    framerate = wf.getframerate()

    # 读取完整的帧数据到str_data中，这是一个string类型的数据
    str_data = wf.readframes(nframes)
    wf.close()
    # 将波形数据转换成数组
    wave_data = numpy.frombuffer(str_data, dtype=numpy.short)
    # 将wave_data数组改为2列，行数自动匹配
    wave_data.shape = -1,2

    # 将数组转置
    wave_data = wave_data.T
    maxAmplitude = max(wave_data[0])

    #cutoffRatio = 0.6
    startTime = time.time()
    drumArrayRough = []
    drumAarrayOutput = []
    drumTimeSet = set()
    for i in range(len(wave_data[0])):
        if abs(wave_data[0][i] > cutoffRatio * maxAmplitude):
            currentTime = '%.1f'%(i/framerate)
            if not currentTime in drumTimeSet:
                if not str(float(currentTime)-0.1) in drumTimeSet:
                    drumArrayRough.append((currentTime, wave_data[0][i]))
                    drumAarrayOutput.append(float(currentTime))
                    drumTimeSet.add(currentTime)
    endTime = time.time()

    print('Time for finding drums', endTime-startTime)
    print('Length of drum list: ', len(drumArrayRough))
    #for element in drumAarrayOutput:
        #print(element)

    return nframes, framerate, wave_data[0], drumAarrayOutput

def time_plt(nframes, framerate, wave_data, ratio=1):
    # test use
    time = numpy.arange(0, nframes//ratio)*(1.0/framerate)
    plt.subplot(111)
    plt.plot(time, wave_data[:nframes//ratio], c='r')
    plt.xlabel('time (seconds)')
    plt.show()

def storeMusic(inputName, wave_data):
    with open('audio_storage.txt','a') as w:
        w.write(f'{inputName}: {wave_data}')
        w.write('\n')

def getMusicAmount(file):
    count = 0
    for element in file:
        if element == '\n':
            count += 1
    return count

def audio_extract():
    with open('audio_storage.txt','r') as r:
        numMusic = getMusicAmount(r.read())
    with open('audio_storage.txt','r') as r:
        outputDict = dict()
        for _ in range(numMusic):
            currentLine = r.readline()
            nameIndex = currentLine.find(':')
            name = currentLine[:nameIndex]
            currentLine = currentLine[nameIndex+2:]
            currentLine = currentLine.strip('\n')
            currentLine = currentLine.strip('[')
            currentLine = currentLine.strip(']')
            tempList = []
            for value in currentLine.split(','):
                tempList.append(float(value))
            outputDict[name] = tempList
    return outputDict

def audio_store(inputName, cutoffRatio):
    print('Process started...')
    nframes, framerate, wave_data, drumAarrayOutput = audio_processing(inputName, cutoffRatio)
    print(drumAarrayOutput)
    # time_plt(nframes, framerate, wave_data, 1)
    print('storing...')
    storeMusic(inputName, drumAarrayOutput)
    print('process cleared')


# Update Audio Here:
# audio_store('Beethoven_Virus', 0.7) # set cutoffRatio
