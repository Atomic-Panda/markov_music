import os
import csv
import json
import random
import numpy as np
import pysynth as synth_main
import pysynth_p
from mix import mix_files

# 状态转移方式：前一个音的(音高,时长)概率转移至下一音的(音高,时长)
class markov():
    def __init__(self):
        # use a dict of dict to store the chain
        self.chain = {}
        self.generator = {}
        self.pitches = set()

    def add(self, key:tuple, next_key:tuple):
        if key not in self.chain:
            self.chain[key] = {}
            self.generator[key] = []
        self.chain[key][next_key] = self.chain[key].get(next_key, 0) + 1
        self.generator[key].append(next_key)
        self.pitches.add(key[0])


    def build_fullmatrix(self, filename):
        row_id = set()
        col_id = set()
        for key, va in self.chain.items():
            row_id.add(key)
            for key2, _ in va.items():
                col_id.add(key2)
        row_id, col_id = list(row_id), list(col_id)
        for key, va in self.chain.items():
            total_sum = sum(va.values())
            for k in va.keys():
                va[k] = va[k] / total_sum
        mat = np.zeros((len(row_id),len(col_id)))
        for i in range(len(row_id)):
            r = row_id[i]
            for j in range(len(col_id)):
                c = col_id[j]
                if c in self.chain[r].keys():
                    mat[i,j]=self.chain[r][c]
        with open(f'./csv/method_1/{filename}.csv','w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([""]+col_id)
            for i in range(len(row_id)):
                writer.writerow([row_id[i]]+list(mat[i]))
        return mat
        
    def build_pitchmatrix(self, filename):
        row_id = set()
        col_id = set()
        for key, va in self.chain.items():
            row_id.add(key[0])
            for key2 in va.keys():
                col_id.add(key2[0])
        row_id, col_id = list(row_id), list(col_id)
        mat = np.zeros((len(row_id),len(col_id)))
        psum = np.zeros((len(row_id)))
        for key, va in self.chain.items():
            psum[row_id.index(key[0])] += sum(va.values())
            for key2 in va.keys():
                mat[row_id.index(key[0]),col_id.index(key2[0])] += self.chain[key][key2]
        psum = np.expand_dims(psum,1).repeat(len(col_id),axis=1)
        mat /= psum
        with open(f'./csv/method_1/{filename}.csv','w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([""]+col_id)
            for i in range(len(row_id)):
                writer.writerow([row_id[i]]+list(mat[i]))
        return mat
        
    def build_pitchclassmatrix(self, filename):
        def judge_r(key):
            if key=="r":
                return key
            else:
                return key[:-1]
        row_id = set()
        col_id = set()
        for key, va in self.chain.items():
            row_id.add(judge_r(key[0]))
            for key2 in va.keys():
                col_id.add(judge_r(key2[0]))
        row_id, col_id = list(row_id), list(col_id)
        mat = np.zeros((len(row_id),len(col_id)))
        psum = np.zeros((len(row_id)))
        for key, va in self.chain.items():
            psum[row_id.index(judge_r(key[0]))] += sum(va.values())
            for key2 in va.keys():
                mat[row_id.index(judge_r(key[0])),col_id.index(judge_r(key2[0]))] += self.chain[key][key2]
        psum = np.expand_dims(psum,1).repeat(len(col_id),axis=1)
        mat /= psum
        with open(f'./csv/method_1/{filename}.csv','w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([""]+col_id)
            for i in range(len(row_id)):
                writer.writerow([row_id[i]]+list(mat[i]))
        return mat

    def save_matrix(self):
        return

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
    with open("./json/tune1.json",'r') as json_file:
        tune1 = [tuple(l) for l in json.load(json_file)]
    #  第二段
    with open("./json/tune2.json",'r') as json_file:
        tune2 = [tuple(l) for l in json.load(json_file)]


    '''
    melody looks like
    [('C', '4'),('B', '4'),('A', '1'),('F', '8'),('F', '8'),('B', '4'),('B', '8'),......,('D', '8'),('A', '4'),('B', '4'),]
    in which, every element is a tuple consists of pitch and duration
    eg, ('C','4') means 四分音符C
    '''

    beat = [('c4*',4),('c4',4),('c4',4),('c4',4)]*30
    pysynth_p.make_wav(beat, bpm=127, repeat=0, fn=u"./wav/beat.wav")

    m1 = markov()
    for i,j in zip(tune1[:-1], tune1[1:]):
        m1.add(i,j)
    m1.build_fullmatrix("tune1_full")
    m1.build_pitchmatrix("tune1_pitch")
    m1.build_pitchclassmatrix("tune1_pitchclass")
    output1 = m1.generate(100, random.choice(tune1))
    with open('./txt/output1.txt','w') as f:
        f.write(str(output1))
    synth_main.make_wav(tune1, bpm=127, repeat=0, fn=u"./wav/result1/temp0.wav")
    synth_main.make_wav(output1, bpm=127, repeat=0, fn=u"./wav/result1/temp1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result1/temp0.wav",u"./wav/music1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result1/temp1.wav",u"./wav/result1/output1.wav")

    m2 = markov()   
    for i,j in zip(tune2[:-1], tune2[1:]):
        m2.add(i,j)
    m2.build_fullmatrix("tune2_full")
    m2.build_pitchmatrix("tune2_pitch")
    m2.build_pitchclassmatrix("tune2_pitchclass")
    output2 = m2.generate(100, random.choice(tune2))
    with open('./txt/output2.txt','w') as f:
        f.write(str(output2))
    synth_main.make_wav(tune2, bpm=127, repeat=0, fn=u"./wav/result1/temp0.wav")
    synth_main.make_wav(output2, bpm=127, repeat=0, fn=u"./wav/result1/temp1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result1/temp0.wav",u"./wav/music2.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result1/temp1.wav",u"./wav/result1/output2.wav")

    for i,j in zip(tune2[:-1], tune2[1:]):
        m1.add(i,j)
    m1.build_fullmatrix("combined_full")
    m1.build_pitchmatrix("combined_pitch")
    m1.build_pitchclassmatrix("combined_pitchclass")
    output = m1.generate(200, random.choice(tune1 + tune2))
    with open('./txt/output.txt','w') as f:
        f.write(str(output))
    synth_main.make_wav(tune1 + tune2, bpm=127, repeat=0, fn=u"./wav/result1/temp0.wav")
    synth_main.make_wav(output, bpm=127, repeat=0, fn=u"./wav/result1/temp1.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result1/temp0.wav",u"./wav/music.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result1/temp1.wav",u"./wav/result1/output.wav")

    os.remove(u"./wav/result1/temp0.wav")
    os.remove(u"./wav/result1/temp1.wav")