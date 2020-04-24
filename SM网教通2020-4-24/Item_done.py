import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class ItemDone():
    def __init__(self):
        pass

    def speaktimes_loc(self,file_path):
        pd.set_option('display.max_rows', None) #显示所有行
        t1 = pd.read_csv(file_path)
        name_list = list(set(t1['Name'].tolist()))
        speak_name_num = len(name_list)
        speak_times_list = pd.DataFrame(np.zeros((speak_name_num, 1)),index=name_list,columns=['Times'])
        speak_times = t1['Name'].value_counts()  # 求出每个人的出现次数
        for i in range(speak_name_num):
            speak_times_list.loc[name_list[i],'Times'] = speak_times[name_list[i]]
        speak_times_list = speak_times_list.sort_values(by='Times', ascending=False)
        return speak_times_list

if __name__ == '__main__':
    demo = ItemDone().speaktimes_loc(r'E:\lanfr -doc\Python inout\progression\zbpr\2020-4-14思品.csv')
    print(demo)
