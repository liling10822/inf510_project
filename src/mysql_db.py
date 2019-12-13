import sqlite3

conn = sqlite3.connect('../data/career.db')
cur = conn.cursor()


def create_tables():
    # positions: id, company, title, location, description, created, url
    cur.execute('DROP TABLE IF EXISTS positions')
    cur.execute("create table positions(" +
                "position_id INTEGER primary key, "+
                "company varchar(30), "+
                "title varchar(50),"+
                "location varchar(30),"+
                "description text,"+
                "created varchar(20),"+
                "url text);")

    # visa: rank, sponsor, num_of_LCA, ave_salary, year}
    cur.execute('DROP TABLE IF EXISTS visa_records')
    cur.execute("create table visa_records("+
                "record_id INTEGER primary key, "+
                "rank integer , "+
                "sponsor varchar(50),"+
                "num_of_LCA integer , ave_salary varchar(10), ryear char(4))")

    cur.execute("SELECT name FROM sqlite_master")
    result = cur.fetchall()
    print('create table: ', result)
    conn.commit()

def refresh_jobs():
    # positions: id, company, title, location, description, created, url
    cur.execute('DROP TABLE IF EXISTS positions')
    cur.execute("create table positions(" +
                "position_id INTEGER primary key, "+
                "company varchar(30), "+
                "title varchar(50),"+
                "location varchar(30),"+
                "description text,"+
                "created varchar(20),"+
                "url text);")
    conn.commit()

if __name__ == '__main__':
    pass