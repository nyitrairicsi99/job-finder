# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

def markignored(id):
    foundrow = -1
    rowdata = []
    file = open("lastjobs.txt",encoding='utf-8')
    i = 0
    for row in file:
        row = row.strip().split(" | ")
        if len(row)>1 and int(row[0])==id: #nem elválasztó
            foundrow = i
            rowdata = row
            break
        i = i + 1 
    
    if foundrow>-1:
        with open('lastjobs.txt', 'r',encoding='utf-8') as file:
            data = file.readlines()

        data[foundrow] = rowdata[0] + ' | 1 | ' + rowdata[2] + ' | ' + rowdata[3] + ' | ' + rowdata[4] + ' | ' + rowdata[5] + '\n'

        with open('lastjobs.txt', 'w',encoding='utf-8') as file:
            file.writelines( data )

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/" or self.path=="/favicon.ico":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Profession.hu állások</title><style>div.container,p {width: 300px; float:left; height: 150px; background-color: lightgrey; margin: 5px}</style></head>", "utf-8"))
            self.wfile.write(bytes("""
            <script>
                function deleterow(id) {
                    console.log(id)
                    fetch("/"+id, {
                        method: "POST",
                    }).then(data => {
                        window.location.reload();
                    }).catch(error => {
                        window.location.reload();
                    });
                }
            </script>
            """, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            file = open("lastjobs.txt",encoding='utf-8')
            for row in reversed(file.readlines()):
                row = row.strip().split(" | ")
                if len(row)>1: #nem elválasztó
                    if row[1]=="0":
                        self.wfile.write(bytes("<div class='container'><p><a href='"+row[5]+"' target='_blank'><strong>"+row[2]+"</strong></a><br />"+row[3]+"<br />"+row[4]+"<br /><i style='cursor: pointer;' onclick=deleterow("+(row[0])+")>Törlés</i></p></div>", "utf-8"))
            file.close()

            

            self.wfile.write(bytes("</body></html>", "utf-8"))
    def do_POST(self):
        id = int(self.path.replace("/",""))
        markignored(id)

    

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")