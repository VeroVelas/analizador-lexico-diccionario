from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Diccionario de sinónimos
sinonimos = {
    'rápido': 'veloz',
    'lento': 'pausado',
    'feliz': 'contento',
    'triste': 'afligido',
    'inteligente': 'listo',
    'tonto': 'necio',
    'grande': 'enorme',
    'pequeño': 'diminuto',
    'fuerte': 'robusto',
    'débil': 'frágil',
    'amable': 'cortés',
    'bello': 'hermoso',
    'feo': 'desagradable',
    'alto': 'elevado',
    'bajo': 'reducido',
    'caro': 'costoso',
    'barato': 'económico',
    'fácil': 'sencillo',
    'difícil': 'complicado',
    'nuevo': 'moderno',
    'viejo': 'antiguo',
    'bueno': 'beneficioso',
    'malo': 'perjudicial',
    'bonito': 'atractivo',
    'horrible': 'espantoso',
    'limpio': 'aseado',
    'sucio': 'desordenado',
    'alegre': 'jovial',
    'serio': 'formal',
    'tranquilo': 'pacífico',
    'nervioso': 'ansioso',
    'claro': 'lúcido',
    'oscuro': 'tenebroso',
    'amplio': 'extenso',
    'estrecho': 'reducido',
    'dulce': 'azucarado',
    'amargo': 'desagradable',
    'caliente': 'ardiente',
    'frío': 'helado',
    'joven': 'juvenil',
    'anciano': 'veterano',
    'rico': 'opulento',
    'pobre': 'necesitado',
    'amigable': 'cordial',
    'hostil': 'antipático',
    'interesante': 'atrayente',
    'aburrido': 'tedioso',
    'cansado': 'agotado',
    'enérgico': 'vigoroso',
    'morir': 'fallecer'
}

# Función para reemplazar palabras por sus sinónimos, manejando mayúsculas
def reemplazar_sinonimos(texto):
    palabras = re.findall(r'\b\w+\b', texto)
    nuevo_texto = []
    palabras_cambiadas = set()

    for palabra in palabras:
        palabra_minuscula = palabra.lower()
        nueva_palabra = sinonimos.get(palabra_minuscula, palabra_minuscula)
        if palabra.istitle():
            nueva_palabra = nueva_palabra.capitalize()
        elif palabra.isupper():
            nueva_palabra = nueva_palabra.upper()
        nuevo_texto.append(nueva_palabra)
        if nueva_palabra.lower() != palabra_minuscula:
            palabras_cambiadas.add(palabra)
    
    # Reconstruir el texto con los reemplazos
    patron = re.compile(r'\b\w+\b')
    nuevo_texto_completo = patron.sub(lambda match: sinonimos.get(match.group().lower(), match.group()), texto)
    
    return nuevo_texto_completo, palabras_cambiadas

# Función para analizar el texto y contar palabras, números y símbolos
def analizar_texto(texto):
    num_palabras = len(re.findall(r'\b\w+\b', texto))
    num_lineas = len(texto.splitlines())
    num_simbolos = len(re.findall(r'[^\w\s]', texto))
    num_numeros = len(re.findall(r'\d', texto))
    return num_palabras, num_lineas, num_simbolos, num_numeros

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        texto = request.form['texto']
        num_palabras, num_lineas, num_simbolos, num_numeros = analizar_texto(texto)
        texto_reemplazado, palabras_cambiadas = reemplazar_sinonimos(texto)

        resultados = []
        lineas = texto.splitlines()
        lineas_reemplazadas = texto_reemplazado.splitlines()
        for i, (entrada, resultante) in enumerate(zip(lineas, lineas_reemplazadas), 1):
            num_simbolos_linea = len(re.findall(r'[^\w\s]', entrada))
            num_numeros_linea = len(re.findall(r'\d', entrada))
            palabras_cambiadas_linea = "x" if any(palabra in entrada for palabra in palabras_cambiadas) else ""
            resultados.append({
                'entrada': entrada,
                'resultante': resultante,
                'cambiadas': palabras_cambiadas_linea,
                'numeros': "x" if num_numeros_linea > 0 else "",
                'simbolos': "x" if num_simbolos_linea > 0 else "",
                'linea': i
            })

        return render_template('index.html', resultados=resultados)

    return render_template('index.html', resultados=None)

if __name__ == '__main__':
    app.run(debug=True)
