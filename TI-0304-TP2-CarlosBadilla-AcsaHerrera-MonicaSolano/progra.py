from flask import Flask, render_template, request, redirect, url_for, abort, session ##Se importan las librerias
app = Flask("Restaurante") 
from pyswip import Prolog ##Se importa prolog desde pyswip
from pyswip import *

p= Prolog()


##Funcion que se encarga de cargar todos los predicados de archivo de texto a la base de conocimientos
def Leer_Archivo():
    fo = open("/home/momo/Desktop/Predicados.txt", "a+")
    str = fo.readline(); ##Lee la linea del archivo
    while str !='':
        p.assertz(str) ##Agrega a la base de conocimientos
        str = fo.readline() ##Lee la linea del archivo
    fo.close()
#################################################################################
##Funcion que se encarga de agregar los predicados al archivo de texto
def Escribir_Archivo(Predicado):
    fo= open("Predicados.txt","a+") ##Abre el archivo
    fo.write(Predicado) ## Escribe en el archivo de texto
    fo.close

########## Funcion que se llama en la pagina de inicio de la app ##############################
@app.route('/') 
def home(): 
	return render_template('momo.html')

@app.route('/Insertar')
def Insertar():
    return render_template('Opciones.html')

@app.route('/Ingresa Restaurante')
def Ingresa_Restaurante():
    return render_template('contacto.html')

@app.route('/Ingresa Platillo')
def Ingresa_Platillo():
    return render_template('Platillo.html')

########### Funcion de consulta#################################################################
@app.route('/Consulta de restaurante')
def Consulta():
    fo = open("/home/momo/Desktop/Predicados.txt", "a+")
    linea = fo.readline();
    if linea =='':
        return render_template('Vacia.html')
    else:
        return render_template('primeraventana.html')
    fo.close()

##################### Agregar restaurante #####################################################

##Se obtienen los datos de la pagina
@app.route('/Obtener', methods=['POST'])
def Obtener():
    centro_comida = request.form['restaurante']
    tipo = request.form['tipo_comida']
    lugar= request.form['ubicacion']
    telefono= request.form['telefono']
    horario= request.form['horario']
    print (tipo)
    AgregarRestaurante(centro_comida,tipo,lugar,telefono,horario)## Se invoca a la funcion para agregar el restaurante
    return render_template('Verificacion.html') ## Verifica que fue ingresado

def AgregarRestaurante(Restaurante,Tipo_comida,Ubicacion,Telefono,Horario):
    agregar_restaurante="restaurante("+Restaurante.lower()+","+Tipo_comida.lower()+","+Ubicacion.lower()+","+Telefono.lower()+","+Horario.lower()+")"
    p.assertz(agregar_restaurante) ## Inserta en la base de conocimientos
    Escribir_Archivo(agregar_restaurante) ## Agrega en el archivo de texto
    Escribir_Archivo("\n")
######################## Agregar PLatillo #####################################################

##Se obtienen los datos de la pagina
@app.route('/Obtener platillo', methods=['POST'])
def Obtener_platillo():
    restaurante = request.form['restaurante']
    platillo = request.form['platillo']
    sabor= request.form['sabor']
    pais= request.form['pais']
    ingrediente= request.form['ingrediente']
    AgregarPlatillo(restaurante,platillo,sabor,pais,ingrediente) ## Se invoca a la funcion para agregar el platillo
    return render_template('Verificacion_platillo.html')

def AgregarPlatillo(Restaurante,Platillo,Sabor,Pais,Ingredientes):
    agregar_Platillo=  "platillo("+Restaurante.lower()+","+Platillo.lower()+","+Sabor.lower()+","+Pais.lower()+","+"["+Ingredientes.lower()+"]"+")"
    p.assertz(agregar_Platillo)## Inserta en la base de conocimientos
    Escribir_Archivo(agregar_Platillo)## Agrega en el archivo de texto
    Escribir_Archivo("\n")


#################################################################################
##############################Consultas##########################################
#################################################################################


############### Verifica si un elemento es parte de la lista ###################
def NoEsta_enLista(Lista,elemento):
    for i in Lista:
        if i == elemento:
            return False
        else:
            return True

############### Imprime la lista de todos los restaurantes############################################
@app.route('/Consulta de restaurantes')
def Consulta_de_restaurantes():
    
    ListaRest = []
    for i in p.query("restaurante(Restaurante,_,_,_,_)"):
        if ListaRest == []: ## la lista esta vacia
            ListaRest.append(i ["Restaurante"]) ## Agrega el restaurante
        elif NoEsta_enLista(ListaRest, i ["Restaurante"]): ## Verifica que el rest no este en la lista
            ListaRest.append(i ["Restaurante"])## Agrega el restaurante
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
        restaurante = list(ListaRest)
    	return render_template('Consulta.html',restaurante=restaurante) ## retorna la lista de rest a la pag
    
###################### Consulta del restaurane por nombre############################################

@app.route('/Consulta nombre del restaurante')
def Rest_por_Nombres():
    return render_template('Rest_por_Nombres.html')

@app.route('/Consulta nombre del restaurante', methods=['POST'])
def Consulta_res_por_nombre():
    restaurante =  request.form['restaurante']## Recibe el nombre del restaurante
    NombreRest = restaurante.lower()## lo convierte en minuscul
    ListaRest = []
    for i in p.query( "restaurante("+NombreRest+",TipoComida,Ubicacion,Telefono,Horario)"): ## Hace la consulta
            ListaRest.append(i["Ubicacion"])##  agrgega la ubicacion a la lista
            ListaRest.append(i["TipoComida"])##  agrgega  el tipo de comida a la lista
            ListaRest.append(i["Telefono"])## agrgega el telefono a la lista
            ListaRest.append(i["Horario"])## agrgega el horario a la lista
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	nombre = list (ListaRest )
    	return render_template('Consulta_nombre.html',nombre=nombre) ## Retorna el resultado	
   
##########################Consulta del restaurane por tipo de comida###############################

@app.route('/Consulta de tipo de comida')
def Rest_por_Tipo():
    return render_template('Rest_por_Tipo.html')


@app.route('/Consulta nombre del tipo de comida', methods=['POST'])
def Consulta_Rest_por_Tipo():
    tipo_comida = request.form['tipo_comida']## Recibe el tipo de comida
    ListaRest = []
    Comida=tipo_comida.lower()## lo convierte en minuscula
    for i in p.query( "restaurante(Restaurante,"+Comida+",_,_,_)"):## Hace la consulta
        if ListaRest == []:
            ListaRest.append(i ["Restaurante"])
        elif NoEsta_enLista(ListaRest, i ["Restaurante"]):
            ListaRest.append(i ["Restaurante"])## Lo agrgega a la lista
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	tipo= list(ListaRest)
    	return render_template('Consulta_tipocomida.html',tipo=tipo)## Retorna el resultado
########Consulta de los ingredientes de los platillos de un restaurante############################

@app.route('/Consulta de los ingredientos')
def Platillos_ingredientes():
    return render_template('Platillos_ingredientes.html')

@app.route('/Consulta por ingrediente', methods=['POST'])
def Consulta_Rest_por_ingrediente():
    restaurante = request.form['restaurante']## Recibe el nombre del restaurante
    ingrediente = request.form['ingrediente']## Recibe el nombre del ingrediente
    
    rest=restaurante.lower()## lo convierte en minuscula
    ing=ingrediente.lower()## lo convierte en minuscula
    ListaPlat=[]
    for plato in p.query("platillo("+rest+",Platillo,_,_,Ingredientes)"):## Hace la consulta
        Lista = plato["Ingredientes"]
        for i in Lista:
            if str(i)==ing:
                ListaPlat.append(plato["Platillo"])## Lo agrgega a la lista
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	ingrediente_select = list(ListaPlat)
    	return render_template('Consulta_ingrediente.html',ingrediente_select=ingrediente_select)## Retorna el resultado
#####################Consulta de los platillos del restaurante################################

@app.route('/Consulta platillos del restaurante')
def Platillos_qTiene_Rest():
    return render_template('Platillos_qTiene_Rest.html')

@app.route('/Consulta por platillo', methods=['POST'])
def Platillos_Rest():
    restaurante = request.form['restaurante'] ## Recibe el nombre del restaurante

    restaurant=restaurante.lower()## lo convierte en minuscula
    ListaPlat=[]
    RestaurantePlatillo = list(p.query("platillo("+restaurant+",Platillo,_,_,_)"))## Hace la consulta
    for restaurant in p.query( "platillo("+restaurant+",Platillo,_,_,_)"):
        ListaPlat.append(restaurant["Platillo"])## Lo agrgega a la lista
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	restaurante_platillo= list (ListaPlat)
    	return render_template('Consulta_por_platillo_en_rest.html',restaurante_platillo=restaurante_platillo) ## Retorna el resultado

#####################Consulta de los restaurantes segun el pais del platillo##################################

@app.route('/Consulta por platillo de paises')
def Rest_qTiene_PlatilloPais():
    return render_template('Rest_qTiene_PlatilloPais.html')

@app.route('/Consulta por pais', methods=['POST'])
def Rest_Platillo_Pais():
    lugar = request.form['pais']## Recibe el pais
    pais=lugar.lower() ## lo convierte en minuscula
    ListaRest=[]
    for restaurante in p.query( "platillo(Restaurante,_,_,"+pais+",_)"): ## Hace la consulta
        if ListaRest == []:
            ListaRest.append(restaurante["Restaurante"])
        elif NoEsta_enLista(ListaRest, restaurante["Restaurante"]):
            ListaRest.append(restaurante["Restaurante"]) ## Lo agrgega a la lista
    if ListaRest == []:
        return render_template('Vacia.html')
    else:
    	pais= list(ListaRest)
    	return render_template('Consulta_pais_ingredientes.html',pais=pais) ## Retorna el resultado

###################################################################################################

##############
Leer_Archivo()  ##Se carga la base de conocimientos 
##############
if __name__ == '__main__': 
	app.run()
