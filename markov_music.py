import os
import json
import random
from pprint import pprint
import pysynth
import pysynth_p
from mix import mix_files

# 只考虑了一个八度的情况
class markov():
    def __init__(self):
        self.order = 4*7
        # use a dict of dict to store the chain
        self.chain = {}
        self.generator = {}

    def add(self, key:tuple, next_key:tuple):
        if key not in self.chain:
            self.chain[key] = {}
            self.generator[key] = []
        self.chain[key][next_key] = self.chain[key].get(next_key, 0) + 1
        self.generator[key].append(next_key)


    def build_matrix(self):
        for key, va in self.chain.items():
            total_sum = sum(va.values())
            for k in va.keys():
                va[k] = va[k] / total_sum

    def show_matrix(self):
        pprint(self.chain)

    def generate(self, length:int, st:tuple):
        cur_state = st
        output = []
        for i in range(length):
            output.append(cur_state)
            if(cur_state in self.generator):
                cur_state = random.choice(self.generator[cur_state])
            else:
                print("exception")
                cur_state = random.choice(list(self.generator.keys()))
        return output
    
if __name__ == "__main__":
    #  第一段
    with open("./json/tunes1.json",'r') as json_file:
        tunes1 = [tuple(l) for l in json.load(json_file)]
    #  第二段
    with open("./json/tunes2.json",'r') as json_file:
        tunes2 = [tuple(l) for l in json.load(json_file)]


    '''
    melody looks like
    [('C', '4'),('B', '4'),('A', '1'),('F', '8'),('F', '8'),('B', '4'),('B', '8'),......,('D', '8'),('A', '4'),('B', '4'),]
    in which, every element is a tuple consists of pitch and duration
    eg, ('C','4') means 四分音符C
    '''

    beat = [('c4*',4),('c4',4),('c4',4),('c4',4)]*30
    pysynth_p.make_wav(beat, bpm=127, repeat=0, fn=u"./wav/beat.wav")

    m1 = markov()   
    for i,j in zip(tunes1[:-1], tunes1[1:]):
        m1.add(i,j)
    output1 = m1.generate(100, random.choice(tunes1))
    pprint(output1)
    with open('./txt/output1.txt','w') as f:
        f.write(str(output1))
    pysynth.make_wav(tunes1, bpm=127, repeat=0, fn=u"./wav/temp0.wav")
    pysynth.make_wav(output1, bpm=127, repeat=0, fn=u"./wav/temp1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/temp0.wav",u"./wav/music1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/temp1.wav",u"./wav/output1.wav")

    m2 = markov()   
    for i,j in zip(tunes2[:-1], tunes2[1:]):
        m2.add(i,j)
    output2 = m2.generate(100, random.choice(tunes2))
    pprint(output2)
    with open('./txt/output2.txt','w') as f:
        f.write(str(output2))
    pysynth.make_wav(tunes2, bpm=127, repeat=0, fn=u"./wav/temp0.wav")
    pysynth.make_wav(output2, bpm=127, repeat=0, fn=u"./wav/temp1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/temp0.wav",u"./wav/music2.wav")
    mix_files(u"./wav/beat.wav",u"./wav/temp1.wav",u"./wav/output2.wav")

    for i,j in zip(tunes2[:-1], tunes2[1:]):
        m1.add(i,j)
    output = m1.generate(200, random.choice(tunes1 + tunes2))
    pprint(output)
    with open('./txt/output.txt','w') as f:
        f.write(str(output))
    pysynth.make_wav(tunes1 + tunes2, bpm=127, repeat=0, fn=u"./wav/temp0.wav")
    pysynth.make_wav(output, bpm=127, repeat=0, fn=u"./wav/temp1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/temp0.wav",u"./wav/music.wav")
    mix_files(u"./wav/beat.wav",u"./wav/temp1.wav",u"./wav/output.wav")

    os.remove(u"./wav/temp0.wav")
    os.remove(u"./wav/temp1.wav")

    # m1.build_matrix()
    # m1.show_matrix()