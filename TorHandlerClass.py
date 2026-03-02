import http.client
import urllib.request

class TorProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = "google.com"

        try:
            req = urllib.request.Request(url, headers=self.headers)

            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for header, value in response.getheaders():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())

        except Exception as e:
            self.send_error(500, f"Error fetching {url}: {e}")

    def log_message(self, format, *args):
        # Suppress log messages or customize as needed
        return
