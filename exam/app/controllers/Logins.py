from system.core.controller import *

class Logins(Controller):
    def __init__(self, action):
        super(Logins, self).__init__(action)
        self.load_model('Loginmodel')
        self.db = self._app.db
   
    def index(self):
        if session.has_key('id'):
            return self.load_view('mainpage.html')       
        else:
            return self.load_view('index.html')

    def logout(self):
        if session.has_key('id'):
            session.pop('id')
        if session.has_key('name'):
            session.pop('name')
        return redirect('/')


    def create(self):
        data = {
        'name': request.form['name'],
        'alias': request.form['alias'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
        }
        create_status = self.models['Loginmodel'].create(data)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id'] 
            session['name'] = create_status['user']['name']
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
        return redirect('/')

    def login(self):
        data = {
        'email' : request.form['email'],
        'password': request.form['password']
        }
        status = self.models['Loginmodel'].check_login(data)
        if status:
            session['id'] = status['user']['id']
            session['name'] = status['user']['name']
        else:
            flash("Email or password does not exist")
        return redirect('/')

   





























       