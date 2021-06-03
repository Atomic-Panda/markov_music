import os
import json
import random
import numpy as np
import pandas as pd
import pysynth as synth_main
import pysynth_p
from mix import mix_files
from converter import restore

# 生成方式：
# 1. 设定小节数（总时长）
# 2. 前一音（休止符）起始点hit概率转移至当前音起始点hit，从而实现时间上的音符切割
# 3. 根据前一音pitch和当前音起始点hit概率转移至当前音pitch
# 小节数设为九小节，因为素材为弱拍起始，故八小节多加一小节
# 时间划分的最小单位为十六分音符，故hit也采取了模16的操作
# 由于第3步中状态由双参数确定，导致每个状态转移的可选项较少甚至没有选项，此时用方法一的方式进行状态转移
# 由于该稀疏性，生成曲可能与原曲重合度较高，可以通过给所有可能一个很小的基础概率来让变化更丰富

def load_data(id):
    with open(f"./json/pitch{id}.json",'r') as json_file:
        pitch = json.load(json_file)
    with open(f"./json/hit{id}.json",'r') as json_file:
        hit = json.load(json_file)
    return pitch, hit
def get_hit_mat(hit):
    hit_mat = np.zeros((16,16))
    hit_sum = np.zeros((16))
    for i,j in zip(hit[:-1], hit[1:]):
        hit_mat[i][j] += 1
        hit_sum[i] += 1
    hit_sum = np.expand_dims(hit_sum,1).repeat(16,axis=1)
    return hit_mat/hit_sum
def save_hit_mat(mat):
    data_df = pd.DataFrame(mat)
    writer = pd.ExcelWriter('./csv/method_2/hit.xlsx')
    data_df.to_excel(writer,'page_1',float_format='%.5f')  #关键3，float_format 控制精度，将data_df写到hhh表格的第一页中。若多个文件，可以在page_2中写入
    writer.save()
def generate_hit(hit_mat):
    bar_count = 0
    hit = [0]
    while bar_count<9:
        new_hit = np.random.choice(16,p=hit_mat[hit[-1]])
        if new_hit < hit[-1]:
            bar_count += 1
        hit.append(new_hit)
    return hit[:-1]
def get_pitch_hit_mat(pitch, hit):
    pitch_hit_mat = {}
    pitch_mat = {}    
    for i in range(1,len(pitch)):
        last_p = pitch[i-1]
        now_p = pitch[i]
        now_h = hit[i]
        if last_p not in pitch_hit_mat:
            pitch_hit_mat[last_p] = {}
            for j in range(16):
                pitch_hit_mat[last_p][j]=[]
        pitch_hit_mat[last_p][now_h].append(now_p)
        if last_p not in pitch_mat:
            pitch_mat[last_p] = []
        pitch_mat[last_p].append(now_p)
    return pitch_hit_mat, pitch_mat
def generate_pitch(hit, pitch_hit_mat, last_p, pitch_mat=None, pitch=None):
    output_pitch = [last_p]
    for i in range(1, len(hit)):
        next_pitch_hit = pitch_hit_mat[output_pitch[-1]][hit[i]]
        next_pitch = pitch_mat[output_pitch[-1]]
        if len(next_pitch_hit):
            output_pitch.append(random.choice(next_pitch_hit))
        elif len(next_pitch):
            output_pitch.append(random.choice(next_pitch))
        else:
            output_pitch.append(random.choice(pitch))
    return output_pitch
def generate_tune(pitch, hit):
    hit_mat = get_hit_mat(hit)
    save_hit_mat(hit_mat)
    output_hit = generate_hit(hit_mat)
    pitch_hit_mat, pitch_mat = get_pitch_hit_mat(pitch, hit)
    output_pitch = generate_pitch(output_hit, pitch_hit_mat, random.choice(pitch), pitch_mat, pitch)
    return output_pitch, output_hit

if __name__ == "__main__":
    pitch, hit = load_data(1)
    output_pitch, output_hit = generate_tune(pitch, hit)
    tune = restore(output_pitch, output_hit)
    synth_main.make_wav(tune, bpm=127, repeat=0, fn=u"./wav/result2/temp.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result2/temp.wav",u"./wav/result2/output1.wav")
    
    pitch, hit = load_data(2)
    output_pitch, output_hit = generate_tune(pitch, hit)
    tune = restore(output_pitch, output_hit)
    synth_main.make_wav(tune, bpm=127, repeat=0, fn=u"./wav/result2/temp.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result2/temp.wav",u"./wav/result2/output2.wav")

    pitch0, hit0 = load_data(1)
    pitch1, hit1 = load_data(2)
    pitch = pitch0 + pitch1
    hit = hit0 + hit1
    output_pitch, output_hit = generate_tune(pitch, hit)
    tune = restore(output_pitch, output_hit)
    synth_main.make_wav(tune, bpm=127, repeat=0, fn=u"./wav/result2/temp.wav")
    mix_files(u"./wav/beat.wav",u"./wav/result2/temp.wav",u"./wav/result2/output.wav")

    os.remove(u"./wav/result2/temp.wav")