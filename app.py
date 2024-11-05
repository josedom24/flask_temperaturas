from flask import Flask, request,url_for,render_template,abort
from lxml import etree
import requests
import os
app = Flask(__name__)	

@app.route('/',methods=["GET","POST"])
def inicio():
	ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
	file_path = ROOT_PATH + "/" + "sevilla.xml"
	doc=etree.parse(file_path)
	municipios=doc.findall("municipio")
	return render_template("inicio.html",municipios=municipios)

@app.route('/<code>')
def temperatura(code):
	url="http://www.aemet.es/xml/municipios/localidad_"+code+".xml"
	try:
		response = requests.get(url)
		response.raise_for_status()  # Verifica si la descarga fue exitosa
		doc = etree.fromstring(response.content)
	except:
		abort(404)
	name=doc.find("nombre").text
	max=doc.find("prediccion/dia/temperatura").find("maxima").text
	min=doc.find("prediccion/dia/temperatura").find("minima").text
	return render_template("temperaturas.html",name=name,max=max,min=min)

if __name__ == '__main__':
	app.run('0.0.0.0',8080, debug=True)
