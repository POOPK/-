from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
#import traceback

class Get_main():
    def __init__(self):
        pass

    def getData(self,room_num,file_path):
        wb = webdriver.Chrome(r'.\chromedriver.exe')
        wb.implicitly_wait(10)
        wb.get(
            'http://uc.101.com/passport/login.html?app_id=fj&callback_url=http%3A%2F%2Ffj.101.com%2F&sdp_app_id=a33ada46-c6f0-4c9f-9a11-076e29c489c8')
        wb.find_element_by_xpath('//input[@id="login_name"]').send_keys()
        wb.find_element_by_xpath('//input[@id="password"]').send_keys()
        ele1 = wb.find_element_by_xpath('//div[@id="agreement"]/i')
        if ele1.get_attribute('class') == 'iconfont text-theme icon-unchecked':
            ele1.click()
        else:
            wb.quit()
        wb.find_element_by_xpath('//a[@class="submit-btn button-theme"]').click()
        wb.find_element_by_xpath('//ul[@class="nav-list fl clearfix"]/li[2]/a').click()
        Ac = ActionChains(wb)
        wb.find_element_by_xpath('//*[@id="private-live-list"]/div/div[1]/div[%d]/div[1]/img' % room_num).click()  # 有时间改下

        # time.sleep(5)
        for handle in wb.window_handles:
            wb.switch_to.window(handle)
            if '直播间' in wb.title:
                wb.switch_to.window(handle)
        self.wb = wb
        wb.switch_to.frame(wb.find_element_by_xpath('//div[@class="_2CLsu1uOFB"]/iframe'))  # 这狗东西有frame的 费我一堆时间
        time.sleep(1)
        morenews = wb.find_element_by_xpath('//*[@id="msg-flow-wrapper"]/div[1]')
        time.sleep(1)
        morenews.click()  # 防止老师禁言时出错误 先点一下来获取数据格式

        '''example = wb.find_element_by_xpath('//div[@class="_31l5pdWWjZ down-msg"]').get_attribute('data-msgid') #str
        example_front = example.split('-')[0]
        example_back = example.split('-')[1]
        print(example_front,example_back)'''
        example = [i.get_attribute('data-msgid') for i in wb.find_elements_by_xpath('//div[@id="msg-flow-wrapper"]/div[@class="_31l5pdWWjZ down-msg"]')]
        #print(example)
        def detail_back_max(list):
            detail_max = []
            for i in list:
                detail_max.append(int(i.split('-')[1]))
            return max(detail_max)

        detail_num = detail_back_max(example)
        detail_front = example[0].split('-')[0]
        QDindex = 0
        last_content = ''
        while True:
            try:
                if QDindex >= 30:  #自动签到循环间隔
                    QDindex = 0
                    self.QD()
                QDindex += 1
                #qdinfo = self.wb2.find_element_by_xpath()
                no_speaking = wb.find_element_by_xpath('//div[@class="_2779f4I_KN"]/div[1]').get_attribute('class')
                if no_speaking == "_3bCGS_LBe-":
                    print('进入禁言循环')
                    no_speaking_times = 0
                    A = True
                    while A:
                        if QDindex >= 1500:
                            QDindex = 0
                            self.QD()
                        QDindex += 1
                        no_speaking_in = wb.find_element_by_xpath('//div[@class="_2779f4I_KN"]/div[1]').get_attribute('class')
                        #加time.sleep影响整体速度
                        if no_speaking_in == "_3bCGS_LBe-":
                            no_speaking_times += 1
                            print('还在禁言...循环次数:%d...\r'%no_speaking_times)
                        else:
                            print('解除禁言')
                            time.sleep(1)
                            example = [i.get_attribute('data-msgid') for i in wb.find_elements_by_xpath('//div[@id="msg-flow-wrapper"]/div[@class="_31l5pdWWjZ down-msg"]')]
                            detail_num = detail_back_max(example)
                            detail_front = example[0].split('-')[0]
                            A = False
                else:
                    if detail_num == last_content: #防止反复记入一个数值
                        raise ValueError
                    readyd = wb.find_element_by_xpath('//div[@data-msgid="%s"]' % (detail_front + '-' + str(detail_num)))
                    data_name = readyd.find_element_by_xpath('.//span[@class="_2b7_McSYzw"]/span').get_attribute('title')
                    try:
                        data_content = readyd.find_element_by_xpath('.//div[@class="_28zJUzkaD0"]/span/span').text
                        data_content = data_content.replace('"','“') #csv中的,和""具有特殊意义
                        data_content = data_content.replace(',','，')
                        data_content = data_content.replace(' ','_')
                    except:
                        data_content = '[表情符号-未知]'

                    data_time = readyd.find_element_by_xpath('.//div[@class="_2fT3_5yu2n _3zr-hu3gqj"]').text
                    print(data_name, data_content, data_time, detail_num)

                    path = file_path

                    self.data_write(data_time,detail_num,data_name,data_content,path)
                    last_content = detail_num
                    detail_num += 1
            except:
                example = [i.get_attribute('data-msgid') for i in wb.find_elements_by_xpath('//div[@id="msg-flow-wrapper"]/div[@class="_31l5pdWWjZ down-msg"]')]
                detail_num = detail_back_max(example)
                detail_front = example[0].split('-')[0]

    def data_write(self,d_time, d_num, d_name, d_content, path):
        if not os.path.exists(path):
            with open(path, 'a', encoding='utf-8') as f:
                f.write('{},{},{},{}'.format('Time', 'DetailNumber', 'Name', 'Content'))
                f.write('\n')
                f.write('{},{},{},{}'.format(d_time,d_num,d_name,d_content))
                f.write('\n')
        else:
            with open(path, 'a', encoding='utf-8') as f:
                f.write('{},{},{},{}'.format(d_time,d_num,d_name,d_content))
                f.write('\n')

    def QD(self):
        self.wb.switch_to.default_content()
        QDinfo = self.wb.find_elements_by_xpath('//div[@id="player"]/div') #elements不会报错 会返回空列表 所以不用再加判断
        if len(QDinfo) == 12:
            QDwindow = self.wb.find_element_by_xpath('//div[@class="_2XArK8uzpA"]/../following-sibling::div[1]')
            QDwindow.find_element_by_xpath('.//button[@class="ant-btn ant-btn-primary ant-btn-lg"]').click()
            print('已签到')
        else:
            print('无签到')
        print(len(QDinfo))
        self.wb.switch_to.frame(self.wb.find_element_by_xpath('//div[@class="_2CLsu1uOFB"]/iframe'))

if __name__ == '__main__':
    Main = Get_main()
    Main.getData(1,os.path.join(os.path.dirname(__file__),'多线程测试.csv'))
