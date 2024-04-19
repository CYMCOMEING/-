from sqlalchemy.orm import Session
from sqlalchemy import desc
from threading import Lock
import functools

from database import models
from database.database import engine

models.Base.metadata.create_all(bind=engine)  # 创建表
db_lock = Lock()

def lock(lock:Lock):
    def wrapper1(func):
        @functools.wraps(func)
        def wrapper2(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper2
    return wrapper1

@lock(db_lock)
def add_comic(db: Session, comic: models.Comic, commit=True) -> models.Comic:
    db.add(comic)
    if commit:
        db.commit()
        db.refresh(comic)
    return comic

@lock(db_lock)
def add_comics(db: Session, comics: list[models.Comic], commit=True):
    db.add_all(comics)
    if commit:
        db.commit()

@lock(db_lock)
def query_comic(db: Session, comic_id: int) -> models.Comic | None:
    return db.query(models.Comic).filter(models.Comic.comicid == comic_id).first()

@lock(db_lock)
def query_static(db: Session, static: int) -> list[models.Comic] | None:
    return db.query(models.Comic).filter(models.Comic.static == static).all()

@lock(db_lock)
def query_sort_comicid(db: Session, static: int) -> list[models.Comic] | None:
    return db.query(models.Comic) \
            .filter(models.Comic.static == static) \
            .order_by(models.Comic.comicid) \
            .all()

'''
static
tag
排序 按comicid
'''
@lock(db_lock)
def query_filter_comic(db: Session, static: int=None, tag: str=None, search:str=None, isAsc: bool=None) -> list[models.Comic] | None:
    """根据参数搜索comic

    Args:
        db (Session): 数据库会话
        static (int, optional): satatic属性. Defaults to None.
        tag (str, optional): 搜索的tag. Defaults to None.
        isAsc (bool, optional): 是否升序. Defaults to None.

    Returns:
        list[models.Comic] | None: 返回结果
    """
    query = db.query(models.Comic) \
        .join(models.Comic_Tag, models.Comic.id == models.Comic_Tag.comicid)
    
    if tag:
        query = query.join(models.Tag, models.Tag.id == models.Comic_Tag.tagid) \
            .filter(models.Tag.text == tag)
    if static != None:
        query = query.filter(models.Comic.static == static)
    if search != None:
        query = query.filter(models.Comic.title.like(f'%{search}%'))
    if desc != None:
        if isAsc:
            query = query.order_by(models.Comic.comicid)
        else:
            query = query.order_by(desc(models.Comic.comicid))
    return query.all()

@lock(db_lock)
def modify_comic(db: Session, comic: models.Comic, **kwargs) -> models.Comic:
    db.refresh(comic)
    if 'chapters' in kwargs:
        if kwargs['chapters'] not in comic.chapters:
            comic.chapters.append(kwargs['chapters'])
    if 'url' in kwargs:
        comic.url = kwargs['url']
    if 'static' in kwargs:
        comic.static = kwargs['static']
    if 'title' in kwargs:
        comic.title = kwargs['title']
    if 'description' in kwargs:
        comic.description = kwargs['description']
    if 'page' in kwargs:
        comic.page = kwargs['page']
    if 'author' in kwargs:
        comic.author = kwargs['author']
    if 'tags' in kwargs:
        tags = set(kwargs['tags'])
        for tag in tags:
            res_tag = db.query(models.Tag).filter(
                models.Tag.text == tag).first()
            if not res_tag:
                res_tag = models.Tag(text=tag)
                db.add(res_tag)
            if res_tag not in comic.tags:
                comic.tags.append(res_tag)
    db.commit()
    db.refresh(comic)
    return comic