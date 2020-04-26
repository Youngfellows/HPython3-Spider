# -*- coding:utf-8 -*-

class Song(object):
    """
    歌曲对象，用于存储歌曲的信息
    """

    def __init__(self, song_id, song_name, song_num, song_url=None):
        object.__init__(self)
        self.song_id = song_id
        self.song_name = song_name
        self.song_num = song_num
        self.song_url = '' if song_url is None else song_url
