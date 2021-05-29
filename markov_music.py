import random
from pprint import pprint
import pysynth

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
    tunes = [('c4',4),('d4',4),('e4',4),('c4',4),('d4',4),('g4',4),('g4',4),\
    # ('r',4),
    ('e4',4),('a4',8),('a4',8),('a4',4),('a4',4),('g4',8),('e4',8),('g4',4),('e4',4),\
    # ('r',4),
    ('c4*',4),('c4',4),('c4',4),('a4',8),('a4',8),('g4',4),('e4',4),('g4',4),\
    # ('r',4),
    ('d4',8),('d4',4),('e4',8),('e4',8),('d4',8),('c4',8),('e4',8),('d4',2),\
    # ('r',4)
    ]
    #  将下列输入复制至原代码 Line 39.
    #  第一段
    #  C = C#
    tunes1 = [('r',2),('r',8),('b5',8),('a5',8),('b5',8),\
    ('e5',4),('b5',8),('a5',8),('r',4),('b5',8),('d6',8),\
    ('r',4),('b5',8),('a5',8),('r',4),('b5',8),('e5',8),\
    ('e5',8),('g5',4),('f#5',4),('d5',8),('b4',8),('e5',8),\
    ('e5',8),('b4',4),('a4',8),('d4',8),('a4',4),('b4',8),\
    ('b4',4),('r',4),('b4',2),\
    ('e5*',4),('g5',4),('f#5',4),('d5',8),\
    ('d5*',4),('r',8),('r',8),('b4',4),\
    ('c5',4),('e5',8),('b5',8),('f#5',4),('g5',4)]

    #  第二段
    #  C = C#  F = F#
    tunes2 = [('r',2),('r',8),('d6',8),('c#6',8),('a5',8),\
    ('f#5',4),('b4',4),('b4',8),('c#5',8),('d5',8),('f#5',8),\
    ('e5',4),('e5',8),('c#6',8),('d6',8),('c#6',8),('a5',8),('e5',8),\
    ('f#5',4),('f#5',8),('c#6',8),('d6',8),('c#6',8),('a5',8),('e5',8),\
    ('f#5',4),('f#8',8),('b4*',4),('b4',16),('c#5',16),('d5',16),('e5',16),\
    ('f#5',4),('b4',4),('b4',8),('c#5',8),('d5',8),('f#5',8),\
    ('e5',4),('e5',8),('a5',4),('g5',8),('f#5',8),('e5',8),\
    ('b4*',8),('f#4*',8),('b4',8),('c#5*',8),('a4*',8),('c#5',8),\
    ('d5*',8),('b4*',8),('f4',4),('r',4),('r',8)]

    # num = 500
    # pitch = random.choices(['c4','d4','e4','f4','g4','a4','b4'],k=num)
    # duration = random.choices([4,8,16], weights=[2,4,8], k=num)
    # melody = []
    # for i,j in zip(pitch, duration):
        # melody.append((i,j))


    # pprint(melody)
    '''
    melody looks like
    [('C', '4'),('B', '4'),('A', '1'),('F', '8'),('F', '8'),('B', '4'),('B', '8'),......,('D', '8'),('A', '4'),('B', '4'),]
    in which, every element is a tuple consists of pitch and duration
    eg, ('C','4') means 四分音符C
    '''
    m = markov()
    melody = tunes1
    for i,j in zip(melody[:-1], melody[1:]):
        m.add(i,j)

    output = m.generate(100, random.choice(melody))
    pprint(output)

    # m.build_matrix()
    # m.show_matrix()

    pysynth.make_wav(melody, bpm=127, repeat=0, fn=u"music.wav")    
    pysynth.make_wav(output, bpm=127, repeat=0, fn=u"noise.wav")