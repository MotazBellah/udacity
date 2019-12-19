import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = 'postgres://ljshxrpvevmggg:8e6f92050f9a64748fb1bbb782989b87131c7187d5d7cd7786e70bd1756c9569@ec2-54-83-13-145.compute-1.amazonaws.com:5432/dcomqm3auo5p1d'
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    commands = (
        """
        CREATE SEQUENCE enrollments_id_seq;

        CREATE TABLE enrollments (
            enrollment_id TEXT NOT NULL DEFAULT nextval('enrollments_id_seq') PRIMARY KEY,
            nanodegree_key TEXT,
            udacity_user_key TEXT,
            enrolled_at DATE NOT NULL DEFAULT CURRENT_DATE,
            status TEXT NOT NULL DEFAULT 'UNENROLLED'
            );

            ALTER SEQUENCE enrollments_id_seq
            OWNED BY enrollments.enrollment_id;
        """,
        )


    for command in commands:
        db.execute(command)
    db.commit()

if __name__ == "__main__":
    main()
