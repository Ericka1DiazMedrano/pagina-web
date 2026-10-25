import os
import sys
import mimetypes
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Asegurar tipos MIME comunes
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("text/html", ".html")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("application/json", ".json")

class RenderWebServiceHandler(BaseHTTPRequestHandler):
    server_version = "RenderStaticWebServer/1.0"

    def do_HEAD(self):
        self.serve_file(send_body=False)

    def do_GET(self):
        self.serve_file(send_body=True)

    def serve_file(self, send_body=True):
        parsed = urlparse(self.path)
        rel_path = unquote(parsed.path).lstrip("/")
        if not rel_path or rel_path == "":
            rel_path = "index.html"

        # Protección contra Directory Traversal
        normalized_path = os.path.normpath(os.path.join(BASE_DIR, rel_path))
        if not normalized_path.startswith(BASE_DIR):
            self.send_error(403, "Acceso denegado")
            return

        if not os.path.exists(normalized_path) or os.path.isdir(normalized_path):
            index_candidate = os.path.join(normalized_path, "index.html") if os.path.isdir(normalized_path) else None
            if index_candidate and os.path.exists(index_candidate):
                normalized_path = index_candidate
            else:
                self.send_error(404, f"Archivo no encontrado: {rel_path}")
                return

        file_size = os.path.getsize(normalized_path)
        mime_type, _ = mimetypes.guess_type(normalized_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        # Soporte para HTTP Range Requests (indispensable para streaming y scrubber de video.mp4)
        range_header = self.headers.get("Range")
        if range_header and range_header.startswith("bytes="):
            try:
                ranges = range_header.replace("bytes=", "").split("-")
                start = int(ranges[0]) if ranges[0] else 0
                end = int(ranges[1]) if len(ranges) > 1 and ranges[1] else file_size - 1

                if start >= file_size:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{file_size}")
                    self.end_headers()
                    return

                end = min(end, file_size - 1)
                content_length = (end - start) + 1

                self.send_response(206)
                self.send_header("Content-Type", mime_type)
                self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
                self.send_header("Content-Length", str(content_length))
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Cache-Control", "public, max-age=3600")
                self.end_headers()

                if send_body:
                    with open(normalized_path, "rb") as f:
                        f.seek(start)
                        remaining = content_length
                        chunk_size = 64 * 1024
                        while remaining > 0:
                            chunk = f.read(min(chunk_size, remaining))
                            if not chunk:
                                break
                            self.wfile.write(chunk)
                            remaining -= len(chunk)
                return
            except (ConnectionResetError, BrokenPipeError):
                return
            except Exception as e:
                self.send_error(500, f"Error interno: {e}")
                return

        # Solicitud estándar (HTTP 200)
        try:
            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(file_size))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()

            if send_body:
                with open(normalized_path, "rb") as f:
                    chunk_size = 64 * 1024
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        self.wfile.write(chunk)
        except (ConnectionResetError, BrokenPipeError):
            return

    def log_message(self, format, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()

class ThreadedServer(ThreadingHTTPServer):
    daemon_threads = True

def run():
    # Render asigna automáticamente la variable de entorno PORT (por defecto 10000)
    port = int(os.environ.get("PORT", 10000))
    server_address = ("0.0.0.0", port)
    httpd = ThreadedServer(server_address, RenderWebServiceHandler)
    print(f"Servidor Web multihilo activo escuchando en el puerto {port} (0.0.0.0:{port})...")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
        httpd.server_close()

if __name__ == "__main__":
    run()
