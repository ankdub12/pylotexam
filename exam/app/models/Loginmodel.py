from system.core.model import Model
import re



class Loginmodel(Model):
    def __init__(self):
        super(Loginmodel, self).__init__()
    
    def create(self,data):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not data['name']:
            errors.append('Name cannot be blank')
        elif len(data['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        if not data['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('Email format must be valid!')
        if not data['password']:
            errors.append('Password cannot be blank')
        elif len(data['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif data['password'] != data['confirm_password']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = data['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO user (name, alias, email, password) VALUES (:name, :alias, :email, :pw_hash)"
            details = {
                'name': data['name'],
                'alias': data['alias'],
                'email': data['email'],
                'pw_hash': hashed_pw
                }
            self.db.query_db(query,details)
            get_user_query = "SELECT * FROM user ORDER BY id DESC LIMIT 1"
            user = self.db.query_db(get_user_query)
            return {"status": True, "user": user[0]}

    
    def check_login(self,data):
        password = data['password']
        user_query = "SELECT * FROM user WHERE email = :email LIMIT 1"
        user_data = {'email': data['email']
                    }
        user = self.db.query_db(user_query, user_data)
        if not user:
            return False
        else:
            if self.bcrypt.check_password_hash(user[0]['password'], password):
                return {"user": user[0]}
            else:
                return False

    