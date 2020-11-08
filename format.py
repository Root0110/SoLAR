# coding   : utf-8
# @Time    :9/21/20 10:04
# @Author  :Xiaohan
# @FileName:format.py
# @SoftWare:PyCharm
nums = ['D0E720E9A118478CF5F728F8F57CCC24','D0E555E9A118478CF5F728F8F57CCC24']
res = []
single = []

for n in nums:
    single = []
    for i in range(0,len(n),2):
        single.append('0x'+ n[i:i+2])
    res.append(single)
print(res)

