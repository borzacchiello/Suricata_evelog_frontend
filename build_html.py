html_head = """
<html><head>
<style>
table {
    border-collapse: collapse;
    width: 100%;
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
<h1> ALERTS </h1>
<table>
    <tr>
        <td><b>Type</b></td>
        <td>
            <div style='float:left'><b>Timestamp &nbsp;</b></div>
            <div style='float:left'>
            <form action = "" method = "get">
                <button name="order" value="timestamp_a" type="submit">A</button>
            </form></div>
            <div style='float:left'>
            <form action = "" method = "get">
                <button name="order" value="timestamp_d" type="submit">D</button>
            </form></div>
        </td>
        <td><b>Src Ip</b></td>
        <td><b>Dest Ip</b></td>
        <td><b>Src Port</b></td>
        <td><b>Dest Port</b></td>
        <td><b>Protocol</b></td>
        <td><b>Interface</b></td>
        <td><b>Message</b></td>
        <td><b>Category</b></td>
        <td>
            <div style='float:left'><b>Severity &nbsp;</b></div>
                <div style='float:left'>
                <form action = "" method = "get">
                    <button name="order" value="severity_a" type="submit">A</button>
                </form></div>
                <div style='float:left'>
                <form action = "" method = "get">
                    <button name="order" value="severity_d" type="submit">D</button>
                </form></div>
        </td>
    </tr>
"""

def button(page, order):
    button = """
    </table>
    <div style='float:left'>
    <form action = "" method = "get">
        <input type="hidden" name="order" value=\"""" + order + """\"/>
        <button name="page" value=\"""" + str(page-1 if page > 0 else 0) + """\" type="submit"> prev page </button>
    </form></div>
    <div>
    <form action = "" method = "get">
        <input type="hidden" name="order" value=\"""" + order + """\"/>
        <button name="page" value=\"""" + str(page+1) + """\" type="submit"> next page </button>
    </form></div>
    """
    return button

html_tail = """
</body></html>
"""

def build_html(rows, page=0, order="timestamp_d"):
    body = ""
    for row in rows:
        timestamp, ttype, src_ip, dest_ip, src_port, dest_port, protocol, interface, message, category, severity = row
        body += "<tr><td>"+ttype+"</td><td>"+timestamp+"</td><td>"+src_ip+"</td><td>"+dest_ip         + \
                "</td><td>"+src_port+"</td><td>"+dest_port+"</td><td>"+protocol+"</td><td>"+interface + \
                "</td><td>"+message+"</td><td>"+category+"</td><td>"+"</td><td>"+severity+"</td></tr>\n"
    return html_head + body + button(page, order) + html_tail