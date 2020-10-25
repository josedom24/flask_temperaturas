from flask import Flask, request,url_for,render_template,abort
from lxml import etree
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
	try:
		doc=etree.parse("http://www.aemet.es/xml/municipios/localidad_"+code+".xml")
	except:
		abort(404)
	name=doc.find("nombre").text
	max=doc.find("prediccion/dia/temperatura").find("maxima").text
	min=doc.find("prediccion/dia/temperatura").find("minima").text
	return render_template("temperaturas.html",name=name,max=max,min=min)

if __name__ == '__main__':
	#port=os.environ["PORT"] //Para heroku
	port="5000"
	app.run('0.0.0.0',int(port), debug=True)
