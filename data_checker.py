#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from Levenshtein import distance as levd
"""
Data structure:
|-- novel_abstract_infor: dict
    |-- novel_name: string
    |-- novel_status: (full: has ended/active: to be continue to next chapter)
    |-- novel_avatar: string, url to image
    |-- novel_language: language of novel (English, Chinese, Vietnamese)
    |-- novel_url: string (link to novel main page)
    |-- chapter_total: string (numeric), -1 for not completed
    |-- chapter_curr: string (numeric) as the highest of ready chapter in database
    |-- author: string
    |-- type: string
    |-- citation: string (zh, en, vi, etc)
    |-- craw_from: target url (truyenfull, novalhall, 69)
    |-- chapter_infor: dict
        |-- ch_name: string
        |-- ch_url: string
        |-- ch_index: string (numeric, from 1 to N)
        |-- ch_content: string (include '\n' symbol as FE layout)
"""

class ScyllaBase():
    def __init__(self) -> None:
        pass
    
    def connect(self):
        pass

    def disconnect(self):
        pass

    def set_hosting(self):
        pass

    def add_content(self, content: dict) -> None:
        pass

    def update_content(self, content: dict) -> None:
        pass

    def delete_content(self, content: dict) -> None:
        pass

    def re_connect(self):
        pass

    def get_infor_novel(self, novel_name: str) -> dict:
        """
        get:
            + novel url
            + status
        && addtional infor as the args for comparison:
            + novel name
            + chapter number
        """
        return {}

    def count_novel(self, type='lang-vi'):
        pass

    def count_chapter(self, type='lang-vi'):
        pass

class DataChecker(ScyllaBase):
    def __init__(self) -> None:
        super.__init__()

    def check_novel(self, novel_name: str) -> bool:
        """
        purpose: check for decision the novel is needed to download or not
        return:
            + True: if novel is existing
            + False: if nodel is not existing
        comparison method: Levenhaustein distance
        with distance threshold = 98
        """
        return True

    def check_chapters(self) -> bool:
        """
        purpose: check for decision the chapter is needed to download or not
        method: assert index, 
                if index of target chapter is larger than maximal existing chapter --> need to download
        return:
            + True: if novel is existing
            + False: if nodel is not existing
        """
        return True