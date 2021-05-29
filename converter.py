# 本代码将通用谱转换为音高列表pitch和音符起点列表hit，两者分离存储
# 模仿生成时，先将小节切分开，再往每个单位里填一个音
# 音符起点列表示例：[0,4,12,8,...]
# 目前只针对4/4拍，最小单位为十六分音符，限定每个音符时值不超过全音符，故出现a,b且a>b时，该音时值为b+16-a
import json
def convert(tune, id):
    pitch = [t[0] for t in tune]
    length = [16/t[1] if t[1]>0 else -24/t[1] for t in tune]
    time = 0
    hit = []
    for l in length:
        hit.append(int(time))
        time += l
        time %= 16
    with open(f"./json/pitch{id}.json",'w') as json_file:
        json.dump(pitch,json_file)
    with open(f"./json/hit{id}.json",'w') as json_file:
        json.dump(hit,json_file)
def restore(pitch, hit):
    tune = []
    for i in range(len(pitch)):
        if i == len(pitch)-1:
            l = 16-hit[i]
        else:
            l = hit[i+1]-hit[i]
        if l < 0:
            l += 16
        if l % 3:
            l = 16/l
        else:
            l = -24/l
        tune.append((pitch[i], int(l)))
    return tune

if __name__ == "__main__":
    with open("./json/tune1.json",'r') as json_file:
        tune1 = [tuple(l) for l in json.load(json_file)]
    with open("./json/tune2.json",'r') as json_file:
        tune2 = [tuple(l) for l in json.load(json_file)]
    convert(tune1,1)
    convert(tune2,2)