from http.server import BaseHTTPRequestHandler, HTTPServer
import json

posts = [
    {'id': 1, 'title': 'Post 1', 'content': 'This is the first post.'},
    {'id': 2, 'title': 'Post 2', 'content': 'This is the second post.'}
]

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/posts':
            self._set_response(content_type='application/json')
            self.wfile.write(json.dumps(posts).encode())
        else:
            self._set_response(404)
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/api/posts':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post = json.loads(post_data)

            if 'title' in post and 'content' in post:
                new_post = {'id': len(posts) + 1, 'title': post['title'], 'content': post['content']}
                posts.append(new_post)

                self._set_response(status_code=201, content_type='application/json')
                self.wfile.write(json.dumps(new_post).encode())
            else:
                self._set_response(status_code=400, content_type='application/json')
                self.wfile.write(json.dumps({'error': 'Missing data'}).encode())
        else:
            self._set_response(404)
            self.wfile.write(b'Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
