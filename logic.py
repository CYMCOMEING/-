import os
import re

from database.database import db
from database.crud import *
from database.models import *

class DbNoDataError(Exception):
    pass


class Comiclogic():
    def __init__(self, root_dir, filter:dict):
        self.root_dir = root_dir
        self.comics = query_filter_comic(db, **filter)
        if not self.comics:
            raise DbNoDataError('数据库没有对应数据')
        self.comic_index = 0
        self.load_comic(self.comics[self.comic_index])
        self.load_chapter(self.chapters[self.chapter_index])

    def get_comic_dir(self, comicid:int, title:str) -> str:
        return os.path.join(self.root_dir, get_efficacious_filename('-'.join((str(comicid), title))))

    def curr_file(self) -> str:
        if self.imgs:
            return self.imgs[self.img_index]
        return None
    
    def load_comic(self, comic:Comic):
        self.chapters = comic.chapters
        if not self.chapters:
            raise DbNoDataError(f'漫画{self.comics[self.comic_index].comicid}没有对应章节')
        self.chapters.sort(key=lambda chapter: chapter.chapter_num)
        self.chapter_index = 0

    def load_chapter(self, chapter: Chapter):
        self.comic_dir = self.get_comic_dir(chapter.comicid, chapter.title)
        if not os.path.exists(self.comic_dir):
            raise NotADirectoryError(f'漫画目录不存在. {self.comic_dir}')
        self.imgs = get_dir_content(self.comic_dir, mode='file')
        self.img_index = 0

    def next(self) -> str:
        # 下一页
        if self.img_index + 1 < len(self.imgs):
            self.img_index += 1
            return self.curr_file()
        # 下一章
        else:
            return self.next_chapter()
        
    def next_chapter(self) -> str:
        # 下一章
        if self.chapter_index + 1 < len(self.chapters):
            self.chapter_index += 1
            self.load_chapter(self.chapters[self.chapter_index])
            return self.curr_file()
        # 下一部漫画
        else:
            return self.next_comic()
    
    def next_comic(self) -> str:
        # 下一部漫画
        if self.comic_index + 1 < len(self.comics):
            self.comic_index += 1
            self.load_comic(self.comics[self.comic_index])
            self.load_chapter(self.chapters[self.chapter_index])
            return self.curr_file()
        # 漫画到底了
        return None

    def previous(self) -> str:
        # 上一页
        if self.img_index > 0:
            self.img_index -= 1
            return self.curr_file()
        else:
            return self.previous_chapter()
    
    def previous_chapter(self) -> str:
        # 上一章最后一页
        if self.chapter_index > 0:
            self.chapter_index -= 1
            self.load_chapter(self.chapters[self.chapter_index])
            self.img_index = len(self.imgs) - 1
            return self.curr_file()
        else:
            return self.previous_comic()
    
    def previous_comic(self) -> str:
        # 上一部漫画最后一章
        if self.comic_index > 0:
            self.comic_index -= 1
            self.load_comic(self.comics[self.comic_index])
            self.chapter_index = len(self.chapters) - 1
            self.load_chapter(self.chapters[self.chapter_index])
            self.img_index = len(self.imgs) - 1
            return self.curr_file()
        # 漫画到顶了
        return None
    

    def set_status_pass(self, status: int):
        """改变漫画状态

        Args:
            status (int): 0下载中，1未整理，2通过，3黑名单，4喜爱
        """
        comic = self.comics[self.comic_index]
        modify_comic(db, comic, static=status)

    def get_comic_title(self) -> str:
        return self.comics[self.comic_index].title

    def info(self) -> str:
        if len(self.chapters) > 1:
            chapter_info = f'第{self.chapter_index+1}话 '
        else:
            chapter_info = ''
        return f'{self.comic_index +1}/{len(self.comics)} {os.path.basename(self.comic_dir)} {chapter_info}{self.img_index +1}/{len(self.imgs)}  static:{self.comics[self.comic_index].static}'


def get_efficacious_filename(filename: str) -> str:
    """把windows中不能创建文件或目录的特殊符号转成中文符号

    中文双引号有闭合的，先不管，都用一种
    """
    char_dict = {'\\': '、', '/': '、', ':': '：', '*': '',
                 '?': '？', '"': '“', '<': '《', '>': '》', '|': '丨'}
    for i, j in char_dict.items():
        filename = re.sub(re.escape(i), j, filename)
    return filename


def get_dir_content(dir: str, mode: str = 'all') -> list:
    '''获取目录下所有文件
    paramete: dir 指定的目录
    mode: mode 'file' 读取文件 ，'dir' 读取目录，其他读取文件和目录
    '''
    ret_list = []
    for i in os.listdir(dir):
        path = os.path.abspath(os.path.join(dir, i))
        if (mode == 'file' and os.path.isfile(path)) or (mode == 'dir' and os.path.isdir(path)):
            ret_list.append(path)
        elif mode != 'file' and mode != 'dir':
            ret_list.append(path)

    return ret_list


if __name__ == "__main__":
    pass
