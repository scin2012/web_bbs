import json
import time
from utils import log

def save(data,path):
    #json.dumps()字典dict转换成字符串s
    s=json.dumps(data,indent=2,ensure_ascii=False)
    #打开路径path文件，将s写入
    with open(path,'w+',encoding='utf-8') as f:
        f.write(s)

def load(path):
    #打开路径path文件，读出s并转换成dict返回
    with open(path,'r',encoding='utf-8') as f:
        return json.loads(f.read())

#json.dump()和json.load()主要用来读写json文件


class Model(object):
    @classmethod
    def db_path(cls):
        #提取类名
        #cls.__name__
        #self.__class__.__name__
        classname=cls.__name__
        path='data/{}.txt'.format(classname)
        return path

    @classmethod
    def _new_from_dict(cls,d):
        m=cls({})
        for k,v in d.items():
            setattr(m,k,v)
        return m

    @classmethod
    def new(cls,form,**kwargs):
        m=cls(form)
        for k,v in kwargs.items():
            setattr(m,k,v)
        m.save()
        return m

    @classmethod
    def all(cls):
        path=cls.db_path()
        models=load(path)
        ms=[cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_all(cls,**kwargs):
        all=cls.all()
        ms=[]
        k,v='',''

        for key,value in kwargs.items():
            k,v=key,value

        # __dict__是用来存储对象属性的一个字典，其键为属性名，值为属性的值。
        for m in all:
            if m.__dict__[k]==v:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        all = cls.all()
        k, v = '', ''

        for key, value in kwargs.items():
            k, v = key, value

        # __dict__是用来存储对象属性的一个字典，其键为属性名，值为属性的值。
        for m in all:
            if m.__dict__[k] == v:
                return m
        return None

    @classmethod
    def find(cls,id):
        return cls.find_by(id = id)

    @classmethod
    def get(cls,id):
        return cls.find_by(id = id)

    @classmethod
    def delete(cls,id):
        all = cls.all()
        index = -1
        for i,e in enumerate(all):
            if e.id == id:
                index = i
                break
        if index == -1:
            pass
        else:
            obj = all.pop(index)
            ms=[m.__dict__ for m in all]
            path=cls.db_path()
            save(ms,path)
            return obj

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def json(self):
        d=self.__dict__.copy()
        return d

    def save(self):
        """
           用 all 方法读取文件中的所有 model 并生成一个 list
           把 self 添加进去并且保存进文件
        """
        models=self.all()
        if self.id is None:
            if len(models) == 0:
                self.id = 1
            else:
                self.id = models[-1].id+1
            models.append(self)
        else:
            index = -1
            for i,e in enumerate(models):
                if e.id == self.id:
                    index = i
                    break
            if index != -1:
                models[index]=self

        ls=[m.__dict__ for m in models]
        path=self.db_path()
        save(ls,path)




































