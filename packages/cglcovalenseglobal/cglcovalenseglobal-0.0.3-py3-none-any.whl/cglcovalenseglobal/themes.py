import os
from sqlalchemy import MetaData,Table, Column, Integer, String,DateTime,text
from sqlalchemy import insert,select,update
# from config.database import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_PORT=5432
DB_PWD="Admin%4012345$"
DB_USER="postgres@covalense-postgres-database"
DB_NAME="postgres"
DB_HOST="covalense-postgres-database.postgres.database.azure.com"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_project_content(project):
    current_session=SessionLocal()
    res = current_session.execute(text(f"SELECT * from project_content where title='{project}';"))
    current_session.close()
    return res.fetchone()

def get_project_themes(project_id):
    current_session=SessionLocal()
    res = current_session.execute(text(f"SELECT * from themes_mangement where project_id='{project_id}';"))
    current_session.close()
    return res.fetchone()


def get_project_recommended_query(project_id):
    current_session=SessionLocal()
    res = current_session.execute(text(f"SELECT question from recommended_queries where project_id='{project_id}';"))
    result = res.fetchall()
    current_session.close()
    final_result = [item[0] for item in result]
    return final_result