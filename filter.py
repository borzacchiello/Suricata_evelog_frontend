def check_if_ip(ip):
    try:
        ip = ip.split(".")
        assert ( len(ip) == 4 )
        ip = map ( int, ip )
        for el in ip:
            assert ( el <= 255 and el >= 0 )
        return True
    except:
        return False

def check_if_port(port):
    try:
        port = int(port)
        assert ( port >= 0 and port <= 65535)
        return True
    except:
        return False


class Filter(object):
    def __init__(self):
        self.source_ip   = "*"
        self.source_port = "*"
        self.destination_ip   = "*"
        self.destination_port = "*"
        self.interface   = "*"
        self.protocol    = "*"
        self.sid         = "*"

    def set_source(self, src=None):
        if src is None:
            self.source_ip   = "*"
            self.source_port = "*"
            return

        src = src.split(":")
        assert ( len(src) == 2 )

        ip, port = src
        if (check_if_ip(ip) or ip=="*") and (check_if_port(port) or port=="*"):
            self.source_ip   = ip
            self.source_port = port
        else:
            raise

    def set_destination(self, dest=None):
        if dest is None:
            self.destination_ip   = "*"
            self.destination_port = "*"
            return

        dest = dest.split(":")
        assert ( len(dest) == 2 )

        ip, port = dest
        if (check_if_ip(ip) or ip=="*") and (check_if_port(port) or port=="*"):
            self.destination_ip   = ip
            self.destination_port = port
        else:
            raise

    def set_interface(self, interface=None):
        if interface is None:
            self.interface = "*"
            return

        if interface.isalnum():
            self.interface = interface
        else:
            raise

    def set_protocol(self, protocol=None):
        if protocol is None:
            self.protocol = "*"
            return

        if protocol.isalpha():
            self.protocol = protocol.upper()
        else:
            raise

    def set_sid(self, sid=None):
        if sid is None:
            self.sid = "*"
            return
        sid = int(sid)
        assert ( sid >= 0 )
        self.sid = sid

    def __str__(self):
        ris = "s_ip=%s, s_port=%s, d_ip=%s, d_port%s, interface=%s, protocol=%s" %           \
              (self.source_ip, self.source_port, self.destination_ip, self.destination_port, \
                self.interface, self.protocol)
        return ris
