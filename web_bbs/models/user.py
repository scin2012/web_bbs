from models import Model

class User(Model):
    def __init__(self,form):
        self.id = form.get('id',None)
        self.username = form.get('username','')
        self.password = form.get('password', '')

    def salt_password(self,password,salt = 'vn3q4@(*&^*'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1=sha256(password)
        hash2=sha256(hash1+salt)
        return hash2

    @classmethod
    def register(cls,form):
        name=form.get('username','')
        pwd=form.get('password','')
        if len(name)>2 and User.find_by(username = name) is None:
            u = User.new(form)
            u.password = u.salt_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls,form):
        u=User(form)
        user=User.find_by(username = u.username)
        if user is not None and user.password == u.salt_password(u.password):
            return user
        else:
            return None