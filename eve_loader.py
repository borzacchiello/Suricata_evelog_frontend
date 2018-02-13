from os import stat
from stat import ST_SIZE
from os.path import abspath
import sys
import json
import sqlite3
from filter import Filter

# If the file has been truncated, return an error. This must be tested in depth.
def follow(file_obj):
    yield "-init"
    while True:
        pos  = file_obj.tell()
        line = file_obj.readline()
        if not line:
            if stat(file_obj.name)[ST_SIZE] < pos:
                yield "-err"
            else:
                yield "-end"
            yield "-init"
        yield line.strip()

def try_json(json_dict, field, cast_to=lambda x: x):
    try:
        ris = cast_to(json_dict[field])
    except:
        ris = ""
    return ris

def compute_order(order):
    if order == "timestamp_d":
        return "tmst DESC"
    elif order == "timestamp_a":
        return "tmst"
    elif order == "severity_a":
        return "severity"
    elif order == "severity_d":
        return "severity DESC"
    raise Exception("compute_order: wrong parameter")

def compute_filter(filter):
    where_clause = " type <> 'empty' "
    if filter.source_ip != "*":
        where_clause += "AND src_ip='%s' " % filter.source_ip
    if filter.source_port != "*":
        where_clause += "AND src_port=%s " % filter.source_port
    if filter.destination_ip != "*":
        where_clause += "AND dest_ip='%s' " % filter.destination_ip
    if filter.destination_port != "*":
        where_clause += "AND dest_port=%s " % filter.destination_port
    if filter.interface != "*":
        where_clause += "AND in_iface='%s' " % filter.interface
    if filter.protocol != "*":
        where_clause += "AND prot='%s' " % filter.protocol
    return where_clause

default_filter = Filter()

class EveLoader(object):

    def _init_db(self):
        c = self.conn.cursor()
        c.execute( 'DROP TABLE IF EXISTS alert' )
        c.execute('''
            CREATE TABLE alert
                ( id        integer,
                  sid       integer,
                  tmst    timestamp,
                  type         text, 
                  src_ip       text, 
                  dest_ip      text,
                  src_port  integer,
                  dest_port integer,
                  prot         text,
                  in_iface     text, 
                  message      text,
                  category     text,
                  severity  integer,
                  payload      text,
                  PRIMARY KEY (id) )
                  ''')
        for i in range(self.max_db_index):
            c.execute("INSERT INTO alert VALUES ('%s', '', '0000-00-00', 'empty', '', '', '', '', '', '', '', '', '', '')" % i)
        self.conn.commit()

    def _init_file_read(self):
        self.eve_file = open(self.eve_path, "r")
        self.gen = follow(self.eve_file)

    def __init__(self, filepath):
        self.eve_path = abspath(filepath)
        self.curr_db_index = 0
        self.max_db_index  = 10000
        self.conn = sqlite3.connect('eve_json.db')
        self._init_db()
        self._init_file_read()

    def _read(self):
        assert ( self.gen.next() == "-init" )
        lines = []
        for line in self.gen:
            if line == "-end":
                break
            if line == "-err": # The file has been truncated, reload the whole db!
                               # The logfile has been rotated/emptied.
                sys.stderr.write("WARNING: file truncated, reloading the whole db!\n")
                self._init_db()
                self.eve_file.close()
                self._init_file_read()
                self.reload()
                return []
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
                sys.stderr.write("WARNING: json malformed line: %s\n" % line)
                continue
            ttype     = try_json(d, "event_type")
            sid       = try_json(try_json(d, "alert"), "signature_id" )
            timestamp = try_json(d, "timestamp")
            src_ip    = try_json(d, "src_ip")
            dest_ip   = try_json(d, "dest_ip")
            proto     = try_json(d, "proto").upper()
            in_iface  = try_json(d, "in_iface")
            message   = try_json(try_json(d, "alert"), "signature")
            category  = try_json(try_json(d, "alert"), "category" )
            severity  = try_json(try_json(d, "alert"), "severity" , cast_to=int)
            src_port  = try_json(d, "src_port",  cast_to=int)
            dest_port = try_json(d, "dest_port", cast_to=int)
            payload   = try_json(d, "payload")

            if payload != "": print "DEBUG", payload, self.curr_db_index

            timestamp_formatted = timestamp[:19].replace("T", " ") if timestamp != "" else ""

            c.execute(""" UPDATE alert
                          SET sid= %s, tmst='%s', type='%s', src_ip='%s', dest_ip='%s', src_port='%s', dest_port='%s', 
                              prot='%s', in_iface='%s', message='%s', category='%s', severity='%s', payload='%s' 
                          WHERE id='%s';
                      """ % ( sid, timestamp_formatted, ttype, src_ip, dest_ip, src_port, dest_port,
                              proto, in_iface, message, category, severity, payload, str(self.curr_db_index)))
            self.curr_db_index = (self.curr_db_index + 1) % self.max_db_index
        if lines:
            self.conn.commit()

    def get_n_lines(self, n, page=0, order="timestamp_d", filter=default_filter):
        c = self.conn.cursor()
        o = compute_order(order)
        f = compute_filter(filter)
        rows = []
        for row in c.execute("SELECT * FROM alert WHERE %s ORDER BY %s LIMIT %s OFFSET %s" % (f, o, n, n*page)):
            rows.append(map( str , row[:len(row)-1]))
        return rows

    def get_payload_id(self, idd):
        c = self.conn.cursor()
        rows = []
        for row in c.execute("SELECT payload FROM alert WHERE id=%s" % idd):
            rows.append(row)
        assert ( len(rows) == 1 and len(rows[0]) == 1 )
        return rows[0][0]

    def quit(self):
        self.eve_file.close()
        self.conn.close()