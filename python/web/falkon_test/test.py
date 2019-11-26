import ujson, falcon


class ObjRequestClass:
    def __init__(self):
        pass

    def on_get(self, request, response) -> None:
        name = request.params['name']

        content = {
            'Hello': name,
            'age': 25,
        }

        response.body = ujson.dumps(content)


api = falcon.API()
api.add_route('/', ObjRequestClass())

host = '127.0.0.1'
port = 8080

import bjoern

bjoern.run(api, host, port, reuse_port=True)
# bjoern.run(wsgi_application, 'unix:/path/to/socket')

# from waitress import serve
# serve(api, host='127.0.0.1', port=8080)

# from wsgiref import simple_server
# simple_server.make_server(host, port, api).serve_forever()
