import os
import json
import sqlite3
import datetime

def compute_datetime(timestamp):
    t = timestamp[:19].replace("T", " ")
    t = t.split(" ")
    d = t[0].split("-")
    h = t[1].split(":")
    return datetime.datetime(int(d[0]), int(d[1]), int(d[2]), int(h[0]), int(h[1]), int(h[2]))

def follow(thefile, seek=None):
    if seek is not None:
        thefile.seek(seek)
    yield "-init"
    while True:
        line = thefile.readline()
        if not line:
            yield "-end"
            yield "-init"
        yield line.strip()

class EveLoader(object):
    def __init__(self, filepath):
        self.eve_file = open(filepath, "r")
        self.gen = follow(self.eve_file, 0)
        self.curr_db_index = 0
        self.max_db_index  = 10000
        self.conn = sqlite3.connect('eve_json.db')
        c = self.conn.cursor()
        c.execute( 'DROP TABLE IF EXISTS alert' )
        c.execute('''
            CREATE TABLE alert
                ( id      integer, 
                  tmst  timestamp,
                  type       text, 
                  src_ip     text, 
                  dest_ip    text,
                  src_port   text,
                  dest_port  text,
                  prot       text,
                  in_iface   text, 
                  message    text,
                  category   text,
                  severity   text,
                  PRIMARY KEY (id) )
                  ''')
        for i in range(self.max_db_index):
            c.execute("INSERT INTO alert VALUES ('%s', '0000-00-00', '', '', '', '', '', '', '', '', '', '')" % i)
        self.conn.commit()

    def _read(self):
        assert ( self.gen.next() == "-init" )
        lines = []
        for line in self.gen:
            if line == "-end":
                break
            if line != "":
                lines.append(line)
        return lines

    def reload(self):
        lines = self._read()
        c = self.conn.cursor()
        for line in lines:
            try:
                d = json.loads(line)
            except:
                sys.stderr.write("WARNING: json malformed line")
            ttype     = "ALERT"
            timestamp = d["timestamp"]
            src_ip    = d["src_ip"]
            dest_ip   = d["dest_ip"]
            proto     = d["proto"]
            in_iface  = d["in_iface"]
            message   = d["alert"]["signature"]
            category  = d["alert"]["category"]
            severity  = d["alert"]["severity"]
            try:
                src_port  = d["src_port"]
                dest_port = d["dest_port"]
            except:
                src_port  = ""
                dest_port = ""
            timestamp_formatted = compute_datetime(timestamp)
            c.execute(""" UPDATE alert
                          SET tmst='%s', type='%s', src_ip='%s', dest_ip='%s', src_port='%s', dest_port='%s', 
                              prot='%s', in_iface='%s', message='%s', category='%s', severity='%s'
                          WHERE id='%s';
                      """ % (str(timestamp_formatted), ttype, src_ip, dest_ip, src_port, dest_port,
                             proto, in_iface, message, category, severity, str(self.curr_db_index)))
            self.curr_db_index = (self.curr_db_index + 1) % self.max_db_index
        self.conn.commit()

    def get_n_lines(self, n):
        c = self.conn.cursor()
        rows = []
        for row in c.execute("SELECT * FROM alert WHERE type <> '' ORDER BY tmst DESC LIMIT %s" % n):
            rows.append(map(lambda x: str(x), row[1:]))
        return rows

    def quit(self):
        self.eve_file.close()
        self.conn.close()