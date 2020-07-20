# -*- coding:utf-8 -*-
from pandora.day08_spider.Netease.Crawler import Crawler
import click
import os

"""
Website:http://cuijiahua.com
Author:Jack Cui
Refer:https://github.com/darknessomi/musicbox
"""


class Netease(object):
    """
    网易云音乐下载
    """

    def __init__(self, timeout, folder, quiet, cookie_path):
        object.__init__(self)
        self.crawler = Crawler(timeout, cookie_path)
        self.folder = '.' if folder is None else folder
        self.quiet = quiet

    def download_song_by_search(self, song_name, song_num):
        """
        根据歌曲名进行搜索
        :params song_name: 歌曲名字
        :params song_num: 下载的歌曲数
        """

        try:
            song = self.crawler.search_song(song_name, song_num, self.quiet)
        except:
            click.echo('download_song_by_serach error')
        # 如果找到了音乐, 则下载
        if song != None:
            self.download_song_by_id(song.song_id, song.song_name, song.song_num, self.folder)

    def download_song_by_id(self, song_id, song_name, song_num, folder='.'):
        """
        通过歌曲的ID下载
        :params song_id: 歌曲ID
        :params song_name: 歌曲名
        :params song_num: 下载的歌曲数
        :params folder: 保存地址
        """
        try:
            url = self.crawler.get_song_url(song_id)
            # 去掉非法字符
            song_name = song_name.replace('/', '')
            song_name = song_name.replace('.', '')
            self.crawler.get_song_by_url(url, song_name, song_num, folder)

        except:
            click.echo('download_song_by_id error')


if __name__ == '__main__':
    timeout = 60
    output = 'Musics'
    quiet = True
    cookie_path = 'Cookie'
    netease = Netease(timeout, output, quiet, cookie_path)
    music_list_name = './music_list/music_list.txt'
    # 如果music列表存在, 那么开始下载
    if os.path.exists(music_list_name):
        with open(music_list_name, 'r', encoding="utf-8") as f:
            music_list = list(map(lambda x: x.strip(), f.readlines()))
        for song_num, song_name in enumerate(music_list):
            netease.download_song_by_search(song_name, song_num + 1)
    else:
        click.echo('music_list.txt not exist.')
