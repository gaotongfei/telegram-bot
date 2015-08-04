# coding=utf-8
from helper import getUpdates, google_api, sendMessage, youdao_api, nasa_api
import collections
import time

'''
:param update_id_deque: 这是一个长度为2的双队列，可在对列两端进行append，pop操作
如果你不理解它的意思，看以下的例子

>>> a = collections.deque(maxlen=2)
>>> a
deque([], maxlen=2)
>>> a.append(1)
>>> a
deque([1], maxlen=2)
>>> a.append(2)
>>> a
deque([1, 2], maxlen=2)
>>> a.append(3)
>>> a
deque([2, 3], maxlen=2)

'''
update_id_deque = collections.deque(maxlen=2)
chat_id = 0


def main():
    '''
    用getUpdate方法，获取bot的消息列表
    '''
    updates = getUpdates()
    rs = updates["result"]
    global update_id_deque
    '''
    update_id_deque每次都append，消息列表中最后一条信息的update_id，其中update_id是
    自增长的，bot每收到一条消息，update_id都会加1，如果没有收到新消息，则update_id不变，
    将update_id放入update_id_deque的目的是，通过计算update_id_deque[0]和update_id_deque[1]
    的差，可以知道是否收到了新消息。
    '''
    update_id_deque.append(rs[-1]['update_id'])

    '''
    update_id_deque长度为1时不做任何处理，这中情况出现在程序刚运行时
    '''
    if len(update_id_deque) == 1:
        pass
    '''
    update_id_deque长度为2时，求出这个[1]与[0]之差
    若差是0，这说明没有收到新的消息，
    若差不是0，这说明收到了新的消息，由于我是间隔一定时间运行一次main函数，在这间隔期间
    有可能收到不止一条消息。
    :param delta: 则告诉你期间一共收到多少条消息
    :param message_text: 接收到的消息
    如果收到的消息以
        /g开头，则执行google函数，返回json
        /trans开头，则执行translate函数，返回json
        /nasa开头，则执行nasa_pic函数，返回json
        /help开头，则直接发送消息给用户
    '''
    if len(update_id_deque) == 2:
        print("len is 2")
        delta = update_id_deque[1] - update_id_deque[0]
        if delta != 0:
            for _ in rs[-delta:]:
                message_text = _['message']['text']

                if message_text.startswith('/g'):
                    global chat_id
                    chat_id = _['message']['chat']['id']
                    google(message_text[3:])
                    update_id_deque.append(rs[-1]['update_id'])

                elif message_text.startswith('/trans'):
                    chat_id = _['message']['chat']['id']
                    translate(message_text[7:])
                    update_id_deque.append(rs[-1]['update_id'])

                elif message_text.startswith('/nasa'):
                    chat_id = _['message']['chat']['id']
                    if len(message_text.strip()) == 5:
                        nasa_pic(message=None)
                    else:
                        nasa_pic(message_text[6:])
                    update_id_deque.append(rs[-1]['update_id'])
                elif message_text.startswith('/help'):
                    chat_id = _['message']['chat']['id']
                    help_message = str("命令列表：\n \
                            * /g <关键词> google搜索 \n \
                            * /trans <翻译的内容> \n \
                            * /nasa [日期(若不填，默认为美国时间当日, 格式如2015-08-03)]")
                    sendMessage(chat_id, help_message)


def google(message):
    '''
    得到用户输入的内容，将google api 返回的结果发送给用户
    '''
    google_rs_message = ''
    rs = google_api(message)['responseData']['results']
    for _ in rs[:1]:
        google_rs_message += "{}\n{}".format(_['url'].encode('utf-8'), _['content'].encode('utf-8'))
        sendMessage(chat_id, str(google_rs_message))


def translate(message):
    '''
    同上，不同的api，返回结果不同，如何处理需要查看它返回的json格式
    '''
    rs = youdao_api(message)
    if rs['errorCode'] == 0:
        if 'basic' in rs:
            translate_rs_message = "{}\n{}".format(rs['translation'][0].encode('utf-8'), rs['basic']['explains'][0].encode('utf-8'))
        else:
            translate_rs_message = "{}".format(rs['translation'][0].encode('utf-8'))
        sendMessage(chat_id, str(translate_rs_message))
    elif rs['errorCode'] == 20:
        sendMessage(chat_id, u"要翻译的文本过长")
    elif rs['errorCode'] == 30:
        sendMessage(chat_id, u"无法进行有效的翻译")
    elif rs['errorCode'] == 40:
        sendMessage(chat_id, u"不支持的语言类型")
    elif rs['errorCode'] == 50:
        sendMessage(chat_id, u"无效的key")
    elif rs['errorCode'] == 60:
        sendMessage(chat_id, u"无词典结果，仅在获取词典结果生效")


def nasa_pic(message):
    '''
    同上
    '''
    rs = nasa_api(message)
    if 'error' in rs:
        sendMessage(chat_id, rs['error'])
    else:
        nasa_pic_and_explanation = "{}".format(rs['url'])
        sendMessage(chat_id, nasa_pic_and_explanation)

while True:
    main()
    '''
    每两秒执行一次，缺点显而易见，因为很多时候bot并没有接收到消息，但是
    它还是执行了main函数，telegram提供了另外一种方式用来获取消息更新：webhook，
    但是它要求必须是https，等我搞好https支持后再来优化
    '''
    time.sleep(2)
