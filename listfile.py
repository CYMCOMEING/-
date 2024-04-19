import os
import shutil


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


class ListFile():
    """遍历二级目录所有文件

    root_dir--a--file1
            |  |_file2
            |_b--file3
               |_file4
    
    会把文件展开成[file1,file2,file3,file4], 通过next()和previous()获取其中的文件
    """
    def __init__(self, dir):
        self.dirs = get_dir_content(dir, mode='dir')
        self.index_d = -1
        self.max_d = len(self.dirs) - 1

        self.files = None
        self.index_f = -1
        self.max_f = -1
        if self.max_d >= 0:
            next_dir = self._next_d()
            self._load_dir(next_dir)

    def _next_d(self):
        if self.index_d >= self.max_d:  # 目录到底了
            return None

        self.index_d += 1
        return self.dirs[self.index_d]

    def _previous_d(self):
        if self.index_d <= 0:  # 目录到头了
            return None

        self.index_d -= 1
        return self.dirs[self.index_d]

    def next(self):
        if self.index_f >= self.max_f:  # 文件到底了
            next_dir = self._next_d()
            if not next_dir:  # 目录到底了
                return None
            self._load_dir(next_dir)

        self.index_f += 1
        return self.files[self.index_f]

    def previous(self):
        if self.index_f <= 0:  # 文件到头了
            previous_dir = self._previous_d()
            if not previous_dir:  # 目录到头了
                return None
            self._load_dir(previous_dir, to_end=True)

        self.index_f -= 1
        return self.files[self.index_f]

    def _load_dir(self, dir: str, to_end=False):
        self.files = get_dir_content(dir, mode='file')
        self.max_f = len(self.files) - 1
        if to_end:
            self.index_f = self.max_f + 1
        else:
            self.index_f = -1

    def curr_dir(self):
        return self.dirs[self.index_d]

    def move_dir(self, src, dst):
        try:
            index = self.dirs.index(src)
            ret = shutil.move(src, dst)
            self.dirs[index] = os.path.abspath(ret)

            if index == self.index_d:
                # 移动的目录是当前加载中的目录，所以文件要重新加载
                index_f = self.index_f
                self._load_dir(self.dirs[index])
                self.index_f = index_f
        except Exception as e:
            print(e)

    def info(self):
        return f'{self.curr_dir()} {self.index_f +1}/{self.max_f+1}'


if __name__ == "__main__":
    # lf = ListFile(r'D:\Comic\#禁漫天堂\#未整理')
    # for i in range(22):
    #     print(lf.next())
    # for i in range(3):
    #     print(lf.previous())
    print(shutil.move(r'G:\Project\图片查看器\1', r'G:\Project\图片查看器\2'))
