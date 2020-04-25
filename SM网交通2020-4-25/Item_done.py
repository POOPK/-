import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import re

class ItemDone():
    def __init__(self):
        self.font = {'family': 'MicroSoft YaHei',
                     'weight': 'bold',
                     'size': '10'}

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

    def speaktimes_re(self,file_path):
        plt.figure(figsize=(20, 8), dpi=80)
        plt.rc('font',**self.font)
        t1 = self.speaktimes_loc(file_path)
        t2 = t1['Times'].value_counts()
        t2.sort_index(inplace=True)
        x_ = t2.index
        y_ = t2.values
        plt.bar(x_,y_)
        plt.xticks(rotation=90)
        plt.xlabel('说话次数')
        plt.ylabel('次数')
        plt.title('说话次数条形图')
        plt.show()

    def speaktimes_time(self,file_path):
        plt.figure(figsize=(20, 8), dpi=80)
        t1 = pd.read_csv(file_path)
        t1['TimeStamp'] = pd.to_datetime(t1['Time'])
        t1 = t1.set_index('TimeStamp')
        t1['Count'] = 1
        t1 = t1.drop(['Time','DetailNumber','Content','Name'],axis=1)
        t1 = t1.resample('10T',label='left').sum()
        x_ = re.findall(r'\d{2}:\d{2}:\d{2}',str(t1.index)) #爷也是服了
        y_ = t1['Count'].tolist()

        plt.rc('font',**self.font)
        plt.plot(x_,y_)
        plt.xticks(rotation=-90)
        plt.title('时间与说话次数折现统计图')
        plt.xlabel('时间')
        plt.ylabel('次数')
        plt.show()


if __name__ == '__main__':
    #demo = ItemDone().speaktimes_loc(r'E:\lanfr -doc\Python inout\progression\zbpr\2020-4-14思品.csv')
    #print(demo)
    #demo = ItemDone().speaktimes_time(r'E:\lanfr -doc\Python inout\progression\zbpr\2020-4-24.csv')
    pass