import psycopg2


class DBException(Exception):
    pass


def connect(dbname):
    import credentials
    try:
        con = psycopg2.connect(host=credentials.hostname, user=credentials.username, password=credentials.password,
                               dbname=credentials.database)
    except psycopg2.Error as e:
        raise DBException(e)

    return con


def create_tables(cur, con):
    return True


def write_identifications(inj_list, cur, con):
    try:
        cur.executemany("""
INSERT INTO identifications (
    mzid,
    pep1,
    pep2,
    linkpos1,
    linkpos2,
    charge,
    "passThreshold",
    "fragTolerance",
    "ionTypes",
    "crosslinker_modMass",
    "rank",
    scores,
    "isDecoy",
    protein,
    file,
    "scanID",
    "peakList_id"
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", inj_list)
        con.commit()

    except psycopg2.Error as e:
        raise DBException(e)

    return []


def write_peaklists(inj_list, cur, con):
    try:
        cur.executemany("""INSERT INTO "peakLists" (id, peaklist) VALUES (%s, %s)""",
                        inj_list)
        con.commit()

    except sqlite3.Error as e:
        raise DBException(e)

    return []


def write_modifications(inj_list, cur, con):
    try:
        cur.executemany("""INSERT INTO modifications (id, name, mass, residues) VALUES (%s, %s, %s, %s)""",
                        inj_list)
        con.commit()
    except sqlite3.Error as e:
        raise DBException(e)

    return []

