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
</style>
</head><body>
<h1> ALERTS </h1>
<table>
    <tr>
        <td><b>Type</b></td>
        <td><b>Timestamp</b></td>
        <td><b>Src Ip</b></td>
        <td><b>Dest Ip</b></td>
        <td><b>Src Port</b></td>
        <td><b>Dest Port</b></td>
        <td><b>Protocol</b></td>
        <td><b>Interface</b></td>
        <td><b>Message</b></td>
        <td><b>Category</b></td>
        <td><b>Severity</b></td>
    </tr>
"""

html_tail = """
</table>
</body></html>
"""

def build_html(rows):
    body = ""
    for row in rows:
        timestamp, ttype, src_ip, dest_ip, src_port, dest_port, protocol, interface, message, category, severity = row
        body += "<tr><td>"+ttype+"</td><td>"+timestamp+"</td><td>"+src_ip+"</td><td>"+dest_ip         + \
                "</td><td>"+src_port+"</td><td>"+dest_port+"</td><td>"+protocol+"</td><td>"+interface + \
                "</td><td>"+message+"</td><td>"+category+"</td><td>"+"</td><td>"+severity+"</td></tr>\n"
    return html_head + body + html_tail