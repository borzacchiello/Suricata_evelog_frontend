import json
import sqlite3
import datetime

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

def try_json(json_dict, field, cast_to=lambda x: x):
    try:
        ris = cast_to(json_dict[field])
    except:
        ris = ""
    return ris

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
                ( id       integer, 
                  tmst   timestamp,
                  type        text, 
                  src_ip      text, 
                  dest_ip     text,
                  src_port    text,
                  dest_port   text,
                  prot        text,
                  in_iface    text, 
                  message     text,
                  category    text,
                  severity integer,
                  PRIMARY KEY (id) )
                  ''')
        for i in range(self.max_db_index):
            c.execute("INSERT INTO alert VALUES ('%s', '0000-00-00', 'empty', '', '', '', '', '', '', '', '', '')" % i)
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
                continue
            ttype     = try_json(d, "event_type")
            timestamp = try_json(d, "timestamp")
            src_ip    = try_json(d, "src_ip")
            dest_ip   = try_json(d, "dest_ip")
            proto     = try_json(d, "proto")
            in_iface  = try_json(d, "in_iface")
            message   = try_json(try_json(d, "alert"), "signature")
            category  = try_json(try_json(d, "alert"), "category" )
            severity  = try_json(try_json(d, "alert"), "severity" , cast_to=int)
            src_port  = try_json(d, "src_port")
            dest_port = try_json(d, "dest_port")

            timestamp_formatted = timestamp[:19].replace("T", " ") if timestamp != "" else ""
            c.execute(""" UPDATE alert
                          SET tmst='%s', type='%s', src_ip='%s', dest_ip='%s', src_port='%s', dest_port='%s', 
                              prot='%s', in_iface='%s', message='%s', category='%s', severity='%s'
                          WHERE id='%s';
                      """ % ( timestamp_formatted, ttype, src_ip, dest_ip, src_port, dest_port,
                              proto, in_iface, message, category, severity, str(self.curr_db_index)))
            self.curr_db_index = (self.curr_db_index + 1) % self.max_db_index
        if lines:
            self.conn.commit()

    def get_n_lines(self, n, page=0):
        c = self.conn.cursor()
        rows = []
        for row in c.execute("SELECT * FROM alert WHERE type <> 'empty' ORDER BY tmst DESC LIMIT %s OFFSET %s" % (n, n*page)):
            rows.append(map(lambda x: str(x), row[1:]))
        return rows

    def quit(self):
        self.eve_file.close()
        self.conn.close()