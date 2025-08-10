#!/usr/bin/env python3
"""
Proxy server que añade headers para bypasear la página de contraseña de localtunnel
"""

from flask import Flask, request, Response
import requests

app = Flask(__name__)

# URL base de la API real
API_BASE = "http://localhost:5000"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    """Proxy todas las peticiones a la API real"""
    
    # Construir URL completa
    url = f"{API_BASE}/{path}"
    
    # Copiar headers de la petición original
    headers = dict(request.headers)
    headers.pop('Host', None)
    
    # Preparar la petición
    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        params=request.args,
        allow_redirects=False
    )
    
    # Crear respuesta
    response = Response(resp.content, resp.status_code)
    
    # Copiar headers de respuesta
    for key, value in resp.headers.items():
        if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']:
            response.headers[key] = value
    
    # CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    
    return response

if __name__ == '__main__':
    print("🚀 Proxy server iniciado en puerto 5001")
    print("   Este proxy añade headers para bypasear localtunnel")
    app.run(host='0.0.0.0', port=5001, debug=False)