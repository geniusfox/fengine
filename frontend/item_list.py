#coding=utf-8
from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import * 
from sqlalchemy.orm import sessionmaker

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/fengine?charset=utf8'
# db = SQLAlchemy(app)
# Base = declarative_base()
#获取数据库连接
def get_engine():
	mysql_engine = create_engine('mysql://root:@localhost:3306/fengine?charset=utf8',encoding = "utf-8",echo =True)
	return mysql_engine

Base = declarative_base()
metadata = MetaData(get_engine())

# class FullLoanItem(Base):
# 	__tablename__ = 'all_loan_items'
# 	id = Column(db.Integer,primary_key = True)
# 	# update_time = Column(Integer)
# 	loan_title = db.Column(String)
# 	loan_amount = db.Column(Integer)
# 	loan_term = db.Column(Integer)
# 	loan_type = db.Column(String)
# 	interest_rate = db.Column(Integer)
# 	dest_url = db.Column(String)
# 	progress_rate = db.Column(Integer)
# 	credit_rating = db.Column(String)
# 	site_id = db.Column(String)
# 	# unique_id = Column(String)
# 	# item_status = Column(Integer)

class FullLoanItem(Base):
	__tablename__ = 'all_loan_items'
	id = Column(Integer,primary_key = True)
	update_time = Column(Integer)
	loan_title = Column(String)
	loan_amount = Column(Integer)
	loan_term = Column(Integer)
	loan_type = Column(String)
	interest_rate = Column(Integer)
	min_investment = Column(Integer)
	dest_url = Column(String)
	progress_rate = Column(Integer)
	credit_rating = Column(String)
	site_id = Column(String)
	unique_id = Column(String)
	item_status = Column(Integer)


@app.route("/loan_items")
def loan_items():
	engine = get_engine()
	Session = sessionmaker(bind=engine)
	session = Session()
	conn = engine.connect()
	items = session.query(FullLoanItem)[1:20]
	# for item in items:
	# 	print item.loan_title
	return render_template('item_list.html', items = items)
	# return "Hello world! %s " % name

if __name__ == "__main__":
	app.run(debug=True)
