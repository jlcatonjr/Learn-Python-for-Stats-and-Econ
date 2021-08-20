#learnSQL.py
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy  import MetaData, Table, Column, Integer, Numeric, String, ForeignKey
# local_postgresql_engine = create_engine(
#     'postgresql+psycopg2://username:password@localhost:5432/mydb')

#remote_mysql_db_
# engine = create_engine('mysql+pymysql://cookiemonster:chocolatechip@mysql01.monster.internal/cookies',
#                                        pool_recycle = 3600)

# connection = engine.connect()

metadata = MetaData()

cookies = Table('cookies', metadata,
                Column('cookie_id', Integer(), primary_key= True),
                Column('cookie_name', String(50), index = True),
                Column('cookie_recipe_url', String(255)),
                Column('cookie_sku', String(55)),
                Column('quantity', Integer()),
                Column('unit_cost', Numeric(12,2)))

engine = create_engine('sqlite:///:memory:')
connection = engine.connect()
metadata.create_all(engine)

ins = cookies.insert().values(
    cookie_name="chocoloate chip",
    cookie_recipe_url = "http://some.aweso.me/cookie/recipe.html",
    cookie_sku = "CC01",
    quantity = "12",
    unit_cost = "0.50")

result = connection.execute(ins)
