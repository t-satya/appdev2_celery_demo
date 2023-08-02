from flask import Flask,request,jsonify,current_app
from flask_restful import Api
from config import LocalDevelopmentConfig
from models import *
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore,Security,utils
from articleAPI import *
from celery import Celery 
from celery.schedules import crontab
import os
from weasyprint import HTML
from jinja2 import Template
from mail import send_mail  



app = None
api = None
user_datastore = None
cel=None
#flask-security-too
def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    
    api = Api(app)
    CORS(app)

    cel = Celery("main")

    cel.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    enable_utc=app.config["ENABLE_UTC"],
    timezone=app.config["TIMEZONE"],
)

    class ContextTask(cel.Task):
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return self.run(*args,**kwargs) 
            
    cel.Task = ContextTask

    app.app_context().push()      
    return app, api,cel,user_datastore

#creates db schema,roles and admin 
def initialize():
   with app.app_context():
        global user_datastore
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()

        if not table_names:  # If no tables exist
            db.create_all()

            admin_role = Role(name='admin', description='Administrator')
            customer_role = Role(name="customer",description="Customer")
            db.session.add(admin_role)
            db.session.add(customer_role)
            db.session.commit()
            
            admin_user=user_datastore.create_user(username="admin",email='admin@mail.com',
                                        password=utils.hash_password('password'),
                                        active=1)
            admin_user.roles.append(admin_role)

            db.session.commit()
            print("Database tables created.")
        else:
            print("Database tables already exist.")

app,api,cel,user_datastore = create_app()
initialize()




@cel.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=12,hour=17), add_together.s(9, 6), name='add every 10')
    sender.add_periodic_task(crontab(minute=39,hour=12),send_articles_as_mail.s(),name="send all articles")

@cel.task()
def add_together(x,y):
    return x+y

def get_template_path(filename):
    # Get the directory where the current module (this file) is located
    module_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the template file
    template_path = os.path.join(module_dir, filename)

    return template_path
@cel.task()
def send_articles_as_mail():
    articles = Article.query.all()
    all_articles=[]
    for art in articles:
        all_articles.append({"title":art.title,"content":art.content})
    template_path = get_template_path("static/articles.html")
    print(all_articles)
    with open(template_path) as file_:
        template= Template(file_.read())
        message = template.render(data=all_articles)
    html = HTML(string=message)
    html.write_pdf(target="articles.pdf")
    send_mail("admin@mail.com",subject="All articles",message=message,
                attachment_file="articles.pdf")


@app.route("/api/trigger_celery/<int:x>/<int:y>")
def add_async(x,y):
    result = add_together.delay(x,y)
    return jsonify({
        "result":result.get()
    })

@cel.task()
def daily_remainder_mail():
    pass





#add resources
api.add_resource(ArticleAPI,"/api/articles")

#signup
@app.post("/api/signup")
def create_user():
   data = request.json
   customer_role = Role.query.filter_by(name="customer").first()
   customer=user_datastore.create_user(username=data['username'],
                                       email=data['email'],
                                       password = utils.hash_password(data['password']),
                               )
   customer.roles.append(customer_role)
   db.session.commit()
   return jsonify({"message":"User Created"})



if __name__ == '__main__':
  # Run the Flask app
  app.run(port=3000)