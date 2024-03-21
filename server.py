from http.server import BaseHTTPRequestHandler, HTTPServer
import re
from release_note import ReleaseNote

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Analyse de l'URL pour obtenir les paramètres
        url_parts = self.path.split('?')
        if len(url_parts) > 1:
            query_string = url_parts[1]
            params = dict(qc.split('=') for qc in query_string.split('&'))
            version = params.get('version', '')
        else:
            version = ''

        # Valider le format du numéro de version
        if version == '':
            self.send_error(400, 'Bad Request: Version number is missing')
            return
        elif not re.match(r'^\d+\.\d+\.\d+$', version):
            self.send_error(400, 'Bad Request: Incorrect version number format')
            return

        # Si la validation réussit, poursuivez le traitement
        try:
            message = f'Traitement de la version {version}'
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            release_note = ReleaseNote()
            message += f'\n Release note object created'

            release_note.set_version(version)
            message += f'\n Version set'

            release_note.set_issues()
            message += f'\n Issues set'
            
            html = release_note.set_content()
            message += f'\n Content set'

            release_note.create_or_update()
            message += f'\n Release note created or updated : '+release_note.url

            self.wfile.write(message.encode())
        except Exception as e:
            # En cas d'erreur, renvoyer un message d'erreur approprié
            self.send_error(500, f'Internal Server Error: {str(e)}')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()