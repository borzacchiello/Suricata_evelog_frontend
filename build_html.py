from filter import Filter

default_filter = Filter()

def compute_head(order, filter=default_filter):
    html_head = """
    <html><head>
    <style>
    .alerts-table {
        border-collapse: collapse;
        width: 100%;
    }

    .column-message {
        text-wrap: normal;
        word-wrap: break-word;
    }

    th, td {
        text-align: left;
        padding: 8px;
    }

    tr:nth-child(even){background-color: #f2f2f2}
    form {
        horizontal-align: middle;
        display: block;
        margin: auto;
    }
    </style>
    </head><body>
    <h1><a href="?">ALERTS</a></h1>
    <form action = "" method = "get">
      <div style='float:left'>
        <input type="hidden" name="order" value=\"""" + order + """\"/>
        <label for="filter_src">Filter source:</label>
        <input type="text" name="filter_src" value=\"""" + filter.source_ip + ":" + filter.source_port + """\">
        <label for="filter_dst">Filter destination:</label>
        <input type="text" name="filter_dst" value=\"""" + filter.destination_ip + ":" + filter.destination_port + """\">
        <label for="filter_protocol">Filter protocol:</label>
        <input type="text" name="filter_protocol" value=\"""" + filter.protocol + """\">
        <label for="filter_sid">Filter sid:</label>
        <input type="text" name="filter_sid" value=\"""" + str(filter.sid) + """\">
      </div>
      <div>
        <input type="submit" value="Send">
      </div>
    </form>
    <br>
    <table class="alerts-table">
        <tr>
            <td><b>Type</b></td>
            <td>
                <div style='float:left'><b>Timestamp &nbsp;</b></div>
                <div style='float:left'>
                <form action = "" method = "get">
                    <input type="hidden" name="filter_src" value=\"""" + filter.source_ip + ":" + filter.source_port + """\">
                    <input type="hidden" name="filter_dst" value=\"""" + filter.destination_ip + ":" + filter.destination_port + """\">
                    <input type="hidden" name="filter_protocol" value=\"""" + filter.protocol + """\">
                    <input type="hidden" name="filter_sid" value=\"""" + str(filter.sid) + """\">
                    <button style=\" """ + ("background-color: #4CAF50" if order == "timestamp_a" else "") + """ \"
                     name="order" value="timestamp_a" type="submit">A</button>
                </form></div>
                <div style='float:left'>
                <form action = "" method = "get">
                    <input type="hidden" name="filter_src" value=\"""" + filter.source_ip + ":" + filter.source_port + """\">
                    <input type="hidden" name="filter_dst" value=\"""" + filter.destination_ip + ":" + filter.destination_port + """\">
                    <input type="hidden" name="filter_protocol" value=\"""" + filter.protocol + """\">
                    <input type="hidden" name="filter_sid" value=\"""" + str(filter.sid) + """\">
                    <button style=\" """ + ("background-color: #4CAF50" if order == "timestamp_d" else "") + """ \"
                      name="order" value="timestamp_d" type="submit">D</button>
                </form></div>
            </td>
            <td><b>Src Ip</b></td>
            <td><b>Src Port</b></td>
            <td><b>Dest Ip</b></td>
            <td><b>Dest Port</b></td>
            <td><b>Protocol</b></td>
            <td><b>Interface</b></td>
            <td class="column-message"><b>Message</b></td>
            <td><b>Category</b></td>
            <td><b>Sid<b></td>
            <td>
                <div style='float:left'><b>Severity &nbsp;</b></div>
                    <div style='float:left'>
                    <form action = "" method = "get">
                        <input type="hidden" name="filter_src" value=\"""" + filter.source_ip + ":" + filter.source_port + """\">
                        <input type="hidden" name="filter_dst" value=\"""" + filter.destination_ip + ":" + filter.destination_port + """\">
                        <input type="hidden" name="filter_protocol" value=\"""" + filter.protocol + """\">
                        <input type="hidden" name="filter_sid" value=\"""" + str(filter.sid) + """\">
                        <button style=\" """ + ("background-color: #4CAF50" if order == "severity_a" else "") + """ \"
                      name="order" value="severity_a" type="submit">A</button>
                    </form></div>
                    <div style='float:left'>
                    <form action = "" method = "get">
                        <input type="hidden" name="filter_src" value=\"""" + filter.source_ip + ":" + filter.source_port + """\">
                        <input type="hidden" name="filter_dst" value=\"""" + filter.destination_ip + ":" + filter.destination_port + """\">
                        <input type="hidden" name="filter_protocol" value=\"""" + filter.protocol + """\">
                        <input type="hidden" name="filter_sid" value=\"""" + str(filter.sid) + """\">
                        <button style=\" """ + ("background-color: #4CAF50" if order == "severity_d" else "") + """ \"
                      name="order" value="severity_d" type="submit">D</button>
                    </form></div>
            </td>
            <td><b>Download Packet<b></td>
        </tr>
    """
    return html_head

def page_buttons(page, order, filter):
    button = """
    </table>
    <div style='float:left'>
    <form action = "" method = "get">
        <input type="hidden" name="order" value=\"""" + order + """\"/>
        <input type="hidden" name="filter_src" value=\"""" + filter.source_ip + ":" + filter.source_port + """\">
        <input type="hidden" name="filter_dst" value=\"""" + filter.destination_ip + ":" + filter.destination_port + """\">
        <input type="hidden" name="filter_protocol" value=\"""" + filter.protocol + """\">
        <input type="hidden" name="filter_sid" value=\"""" + str(filter.sid) + """\">
        <button name="page" value=\"""" + str(page-1 if page > 0 else 0) + """\" type="submit"> prev page </button>
    </form></div>
    <div>
    <form action = "" method = "get">
        <input type="hidden" name="order" value=\"""" + order + """\"/>
        <input type="hidden" name="filter_src" value=\"""" + filter.source_ip + ":" + filter.source_port + """\">
        <input type="hidden" name="filter_dst" value=\"""" + filter.destination_ip + ":" + filter.destination_port + """\">
        <input type="hidden" name="filter_protocol" value=\"""" + filter.protocol + """\">
        <input type="hidden" name="filter_sid" value=\"""" + str(filter.sid) + """\">
        <button name="page" value=\"""" + str(page+1) + """\" type="submit"> next page </button>
    </form></div>
    """
    return button

html_tail = """
</body></html>
"""

def packet_download_builder(id):
    download_packet_button = """
    <form action = "" method = "post">
        <button name="id" value=\"""" + str(id) + """\" type="submit">download</button>
    </form>
    """
    return download_packet_button

def build_html(rows, page=0, order="timestamp_d", filter=default_filter):
    body = ""
    for row in rows:
        idd, sid, timestamp, ttype, src_ip, dest_ip, src_port, dest_port, protocol, interface, message, category, severity = row
        body += "<tr><td>"+ttype+"</td><td>"+timestamp+"</td><td>"+src_ip+"</td><td>"+src_port       + \
                "</td><td>"+dest_ip+"</td><td>"+dest_port+"</td><td>"+protocol+"</td><td>"+interface + \
                "</td><td class=\"column-message\">"+message+"</td><td>"+category+"</td><td>"+sid    + \
                "</td><td>"+severity + "</td><td>"+packet_download_builder(idd)+"</td></tr>\n"
    return compute_head(order, filter) + body + page_buttons(page, order, filter) + html_tail

def build_table_packet(payload, packet):
    return "<table border=\"1\"><tr><td><b>payload<b></td></tr><tr><td>" + \
                (payload if payload else "_empty_")+"</td></tr><tr><td>" + \
                "<b>packet<b></td></tr><tr><td>"                     + \
                (packet if packet else "_empty_")+"</td></tr></table>"