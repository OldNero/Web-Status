from flask import Flask, request, render_template, Markup
from http_status import Status
import httpx
import socket

app = Flask(__name__)

''' Get url from input box - done '''
''' Return server status  - done'''
''' Catch url errors - done '''
''' Catch server errors '''


@app.route("/", methods=["GET", "POST"])
def index():
    getUrl = request.args.get("url")
    if getUrl != None:
        try:
            url = httpx.get(getUrl, timeout=5.00)
            code =  url.status_code
            code_msg = Status(code, strict=False)
            
            if code:
                
                ip_addr = socket.gethostbyname('google.com')
                result = Markup(f" <br><h3> URL: { ip_addr}</h3> <br> <h3>Status Code: {code}</h3> <h3><br> Status Message: {code_msg.description}</h3>")
                return render_template("Index.html", result=result)
                
        except httpx.NetworkError:
            result = Markup(f" <br><h3>An error occurred while interacting with the network ( or possible invalid URL).</h3>")
            
        except httpx.ProtocolError:
            result = Markup(f" <br><h3>The protocol was violated.</h3>")
            
        except httpx.ProxyError:
            result = Markup(f" <br><h3>An error occurred while establishing a proxy connection.</h3>")
            
        except httpx.UnsupportedProtocol:
            result = Markup(f" <br><h3>Attempted to make a request to an unsupported protocol.</h3>")
                
        except httpx.InvalidURL:
            result = Markup(f" <br><h3>{getUrl} either doesn't exist or server is blocking all traffic.</h3>")
        
        except httpx.TimeoutException:
            result = Markup(f" <br><h3>{getUrl} has timed out.</h3>")
        
        except httpx.StreamError:
            result = Markup(f" <br><h3>The developer made a mistake. Sorry!</h3>")
        
        return render_template("Index.html", result=result)
            

    return render_template("Index.html")


if __name__ == "__main__":
    app.run(debug=True)
