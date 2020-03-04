# -*- coding: utf-8 -*-

from twitter import *
from time import sleep
import random

from apscheduler.schedulers.blocking import BlockingScheduler

schedule = BlockingScheduler()

# @schedule.scheduled_job('interval', minutes= 5)
@schedule.scheduled_job('cron', day_of_week='mon-sun', hour= random.randint(12,15))

def Init():
    token = "XXXXXXXXXXXXXXXX"
    token_secret = "XXXXXXXXXXXXXXXX"
    consumer_key = "XXXXXXXXXXXXXXXX"
    consumer_secret = "XXXXXXXXXXXXXXXX"   
   
    # premise
    # user_name =  input("Please enter username: \n")
    r_maximum = random.randint(40, 50)  # int(input("Please enter the number of user you want to follow(It can to follow until 1000 users now): \n")) #maximum follow
    f_maximum = random.randint(30, 40)

    return Twitter(auth = OAuth(token, token_secret, consumer_key, consumer_secret)), f_maximum, r_maximum

def remove(t, maximum, me):    
    # リムーブする関数で使用するリストをフォロワー100人ごとに取得する関数

    print("It's a remove turn now.")
    current = 0
    _cursor = -1
    _count = 200
    _me = me['screen_name']
    num = 0
    currentPage = 0
    maximumPage = 2 #400
    _list = list()

    while current < 7:
        #フォロワーのリスト 200 とりあえず 7*200= 1400 usersを対象
        friends = t.friends.list(screen_name= _me, cursor=_cursor, count= _count)
        current += 1
        for friend in friends['users']:
            _list.append(friend['screen_name'])
            if len(_list) == 100:
                #friendships.lookup関数の引数は100までのため
                num = destroy(_list, num, maximum)
                if num >= maximum:
                    print("All targets were removed successfully.") 
                    break
                _list = []
                continue
        _cursor = friends['next_cursor_str']

def destroy(_list, num, maximum):
    # 取得したリストを元に片思いをリムーブする関数
    tmp = _list.copy()
    ids = ','.join(tmp)
    connects = t.friendships.lookup(screen_name= ids) 
    for connect in connects:
        if "followed_by" in connect['connections']:
            pass
        else:
            t.friendships.destroy(screen_name= connect['screen_name'])
            num += 1
            print("{0:3d}: @".format(num) + connect['screen_name'] +" removed!")
            if num >= maximum:
                return num
                break
            sleep(random.randint(20, 25))
    return num

def follow(t, maximum, me, user='ゆーざー名'):
    # リストを取得し、自分のフォロワーのフォロワーをフォローする関数
    # ユーザーを選択しない場合、可能ならば自分のフォロワーをフォローする
    
    print("It's a follow turn now.")
    _cursor = -1 #default
    maximumPages = 5  #the number of page def:1000 users
    _count = 200
    current = 0 #order
    currentPage = 0 # current page

    while currentPage < maximumPages:
        statusUpdate = t.followers.list(screen_name= user, cursor=_cursor, count= _count)
        users = statusUpdate['users']
        for follow in users:
            if follow['screen_name'] == me['screen_name']:
                #フォローする対象が自分だった時
                pass
            elif follow['following'] == True:
                #既にフォローしていた時
                pass
            elif follow['follow_request_sent'] == True:
                pass
            else:
                try:
                    t.friendships.create(screen_name= follow['screen_name'])
                    current += 1
                    print("{0:3d}: @".format(current)+follow['screen_name']+" Followed!")
                    if current >= maximum:
                        break
                    sleep(random.randint(20, 25))
                except TwitterHTTPError:
                    pass
        if current >= maximum:
           break
        currentPage += 1
        _cursor=statusUpdate['next_cursor']
    print("All targets were followed successfully.")
    
def main(t, f_maximum, r_maximum):
    me = t.account.settings()
    # 自分のフォロワーを選択
    followers = t.followers.list(screen_name= me['screen_name'])
    follower = followers['users']
    for target in follower:
        user = target['screen_name']
        break

    follow(t, f_maximum, me)
    sleep(20)
    remove(t, r_maximum, me)
    sleep(20)
    follow(t, f_maximum, me, user)

if __name__ == '__main__':
    t, f_maximum, r_maximum = Init()
    main(t, f_maximum, r_maximum)

schedule.start()
