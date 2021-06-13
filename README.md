# 1. 文件

method_1.py, method_2.py对应两种不同的生成方式

converter.py用于将PySynth格式的MIDI转换为方法二可用的(pitch,hit)元组格式

mix.py用于将生成的旋律与44拍的鼓点音频混音结合

# 2. 目录

csv目录存放两种方法各自的马尔科夫链转移矩阵，以及对应的可视化表格图片

json目录存放两首样例旋律在PySynth格式下的谱子

txt目录存放生成旋律在PySynth格式下的谱子

wav目录存放两种方法各自生成的旋律音频
