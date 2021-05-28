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
            cur_state = random.choice(self.generator[cur_state])
            output.append(cur_state)
        return output
    
if __name__ == "__main__":
    tigers = [('c4',4),('d4',4),('e4',4),('c4',4),('d4',4),('g4',4),('g4',4),\
    # ('r',4),
    ('e4',4),('a4',8),('a4',8),('a4',4),('a4',4),('g4',8),('e4',8),('g4',4),('e4',4),\
    # ('r',4),
    ('c4*',4),('c4',4),('c4',4),('a4',8),('a4',8),('g4',4),('e4',4),('g4',4),\
    # ('r',4),
    ('d4',8),('d4',4),('e4',8),('e4',8),('d4',8),('c4',8),('e4',8),('d4',2),\
    # ('r',4)
    ]

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
    melody = tigers
    for i,j in zip(melody[:-1], melody[1:]):
        m.add(i,j)

    output = m.generate(100, random.choice(melody))
    pprint(output)

    # m.build_matrix()
    # m.show_matrix()

    pysynth.make_wav(tigers, bpm=127, repeat=0, fn=u"tigers.wav")    
    pysynth.make_wav(output, bpm=127, repeat=0, fn=u"noise.wav")
