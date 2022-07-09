'''MANEJADOR DE TIPOS DE DATOS
Este programa puede crear tipos de datos basandose en el tamano de su representacion y la alineacion necesaria para cada 
tipo de dato. Tambien permite crear structs y unions.
Los tipos struct se alojan en el diccionario tipos, en el que se realizaran las divisiones de espacio de la memoria para obtener
su representacion y alineacion correspondiente. El resto de los tipos se encuentra en el diccionario tiposAtomicos.
'''
tipos = {}
tiposAtomicos = {}

'''La funcino noEmpaquetado itera sobre los tipos del struct y analiza su alineacion para verificar si puede ser utilizado el espacio
de memoria dado por ultimo o debe buscarse una memoria mas alla, por no ser multiplo de la alineacion. Esto se realiza varias veces
hasta lograr alojar todos los tipos del struct
'''
def noEmpaquetado(nombre,listaDeTipos,ultimo):
	auxiliar = []
	ocupacion = 0
	final = 0
	for x in range(0,len(listaDeTipos)):
		representacion = tiposAtomicos[listaDeTipos[x]][0]
		alineacion = tiposAtomicos[listaDeTipos[x]][1]
		if ultimo == 0 or alineacion % ultimo == 0 or ultimo % alineacion == 0:
			auxiliar.append([ultimo,ultimo+representacion-1,alineacion-representacion])
			ocupacion += representacion
			final = ultimo
			ultimo += alineacion
		else:
			ultimo += (ultimo%alineacion)
			auxiliar.append([ultimo,ultimo+representacion-1,alineacion-representacion])
			ocupacion += representacion
			final = ultimo
			ultimo += alineacion
	desperdicio = final-ocupacion
	tiposAtomicos[nombre] = [final+1,tiposAtomicos[listaDeTipos[0]][1]]
	tipos[nombre] = [auxiliar,ocupacion,desperdicio,listaDeTipos]
	return ultimo
'''La funcion empaquetado toma los tipos del struct y los introduce en la memoria uno seguido del otro sin considerar su alineacion, 
unicament se toma en cuenta el tamano de su representacion.
'''
def empaquetado(nombre, listaDeTipos, ultimo):
	#se ignora la alineacion
	auxiliar = []
	ocupacion = 0
	final = 0
	for x in range(0,len(listaDeTipos)):
		representacion = tiposAtomicos[listaDeTipos[x]][0]
		alineacion = tiposAtomicos[listaDeTipos[x]][1]
		auxiliar.append([ultimo,ultimo+representacion-1,0])
		ocupacion += representacion
		final = ultimo
		ultimo += representacion
	tipos[nombre] = [auxiliar,ocupacion,0,listaDeTipos]
	tiposAtomicos[nombre] = [final+1,tiposAtomicos[listaDeTipos[0]][1]]
	return ultimo

'''La funcion optimo toma el arreglo generado por noEmpaquetado y mejora las posiciones de los tipos de struct para que no pierdan 
una cantidad grande de memoria. Primero se verifican los espacios disponibles y se alojan en una lista. Luego se itera de nuevo sobre
los tipos y si su alineacion es multiplo del espacio se agrega alli y se verifican los valores que pueden considerarse para los espacios
restantes de este,si es que existen. Existe una lista de visitados que evita modificar o darle espacio a un tipo dos veces.
En caso de que un tipo no tenga una alineacion multiplo del espacio, se verifican los demas para buscar alguno que la tenga y despues se
realiza el mismo procedimiento anterior.
'''
def optimo(nombre,listaDeTipos,ultimo):
	noEmpaquetado(nombre,listaDeTipos,ultimo)
	dictAuxiliar = tipos[nombre][0]
	desperdicio = 0
	disponibles = []
	for x in range(0,len(listaDeTipos)):
		inicio = dictAuxiliar[x][0]
		fin = dictAuxiliar[x][1]
		desperdicio = dictAuxiliar[x][2]
		disponibles.append([x,inicio,fin,desperdicio,fin-inicio])
	ultimo = dictAuxiliar[0][0]
	dic = [[0,0,0]]*len(listaDeTipos)
	ocupacion = 0
	guardado = 0
	visitados = [0]*len(listaDeTipos)
	final = 0
	for x in range(0,len(listaDeTipos)):
		if visitados[x] == 1:
			continue
		else:
			representacion = tiposAtomicos[listaDeTipos[x]][0]
			alineacion = tiposAtomicos[listaDeTipos[x]][1]
			if ultimo == 0 or alineacion % ultimo == 0 or ultimo % alineacion == 0:
				dic[x]=[ultimo,ultimo+representacion-1,alineacion-representacion]
				final = ultimo
				ultimo += representacion
				ocupacion += representacion
				if alineacion-representacion != 0:
					for y in range(x+1,len(listaDeTipos)):
						if disponibles[y][4]<=alineacion-representacion and visitados[y]==0:
							repres = tiposAtomicos[listaDeTipos[y]][0]
							al = tiposAtomicos[listaDeTipos[y]][1]
							dic[y]=[ultimo,ultimo+repres-1,al-repres]
							final = ultimo
							ultimo+=repres
							ocupacion += repres
							dic[x][2] = 0
							visitados[y]=1
							break
			else:
				ultimo += (ultimo % alineacion)
				for y in range(x+1,len(listaDeTipos)):
					al = tiposAtomicos[listaDeTipos[y]][1]
					if ultimo == 0 or al % ultimo == 0 or ultimo % al == 0 and visitados[y]==0:
						repres = tiposAtomicos[listaDeTipos[y]][0]
						al = tiposAtomicos[listaDeTipos[y]][1]
						dic[y]=[ultimo,ultimo+repres-1,al-repres]
						ocupacion += repres
						final = ultimo
						ultimo += repres
						dic[x][2] = 0
						visitados[y]=1
				dic[x]=[ultimo,ultimo+representacion-1,alineacion-representacion]
				final = ultimo
				ultimo += representacion
				ocupacion += representacion
				for y in range(x+1,len(listaDeTipos)):
					if disponibles[y][4]<=alineacion-representacion and visitados[y]==0:
						repres = tiposAtomicos[listaDeTipos[y]][0]
						al = tiposAtomicos[listaDeTipos[y]][1]
						dic[y]=[ultimo,ultimo+repres-1,al-repres]
						ocupacion += repres
						final = ultimo
						ultimo += repres
						dic[x][2] = 0
						visitados[y]=1
						break
	desperdicio = ocupacion-final
	tipos[nombre] = [dic,ocupacion,desperdicio,listaDeTipos]
	tiposAtomicos[nombre] = [final+1,tiposAtomicos[listaDeTipos[0]][1]]
	return ultimo

'''La funcion verificarTipo retorna True si nombre es un tipo en el programa
'''
def verificarTipo(nombre):
	if (nombre in tipos) or (nombre in tiposAtomicos):
		return True
	return False

'''La funcion verificarListaTipos retorna True si todos los tipos dentro de una lista son parte del programa.
'''
def verificarListaTipos(lista):
	for x in range(0,len(lista)):
		if verificarTipo(lista[x]) == False:
			print(x)
			return False
	return True
'''La funcion prettyPrinter imprime los valores deseados en pantalla dado el nombre de un tipo.
'''
def prettyPrinter(nombre,string):
	tamano = tiposAtomicos[nombre][0]
	alineacion = tiposAtomicos[nombre][1]
	desperdiciado = tipos[nombre][2]
	print("\n")
	print(string)
	print("El tamano del tipo es: "+str(tamano))
	print("La alineacion del tipo es: "+str(alineacion))
	print("La cantidad de bytes desperdiciados es: "+str(desperdiciado))
	
'''La funcion describirTipo toma el nombre de un tipo. Si es struct busca los valores para no empaquetados, empaquetados y reordenados
y si es un tipo pero no struct retorna los valores alojados en tiposAtomicos que caracterizan la alineacion, cantidad de bytes perdidos
y el tamano de dicho tipo.
'''
def describirTipo(nombre):
	if verificarTipo(nombre) == False:
		print("El nombre "+nombre+" no corresponde a un tipo creado")
	else:
		if (nombre in tipos): #es un struct
			print("El tipo "+nombre+" cuenta con:")
			ultimo = tipos[nombre][0][0][0]
			listaDeTipos = tipos[nombre][3]
			noEmpaquetado(nombre,listaDeTipos,ultimo)
			prettyPrinter(nombre,"No empaquetado:")
			empaquetado(nombre,listaDeTipos,ultimo)
			prettyPrinter(nombre,"Empaquetado:")
			optimo(nombre,listaDeTipos,ultimo)
			prettyPrinter(nombre,"Reordenando los campos de manera optima:")
		else:
			print("El tipo "+nombre+" cuenta con:")
			tamano = tiposAtomicos[nombre][0]
			alineacion = tiposAtomicos[nombre][1]
			desperdicio = 0
			try:
				desperdicio = tiposAtomicos[nombre][2]
			except:
				desperdicio = 0
			print("El tamano del tipo es: "+str(tamano))
			print("La alineacion del tipo es: "+str(alineacion))
			print("La cantidad de bytes desperdiciados es: "+str(desperdicio))
			
'''La funcion MCD calcula el maximo comun divisor de a y b
'''
def MCD(a, b):
    temporal = 0
    while b != 0:
        temporal = b
        b = a % b
        a = temporal
    return a
'''La funcion MCM calcula el minimo comun divisor de a y b
'''
def MCM(a, b):
    return (a * b) / MCD(a, b)
'''La funcion crearTipoUnion toma el nombre de un tipo y su lista de tipos e itera sobre ellos para conseguir el MCM que resulta
ser en la alineacion del tipo. Luego se guarda el tipo union.
'''
def crearTipoUnion(nombre, listaDeTipos, ultimo):
	#verificar los tipos
	if verificarTipo(nombre) == True:
		print("El nombre "+nombre+" ya corresponde a un tipo creado")
	else:
		if verificarListaTipos(listaDeTipos) == True:
			#guardar tipo
			dicc = {}
			valores = []
			for x in range(0,len(listaDeTipos)):
				dicc[x] = tiposAtomicos[listaDeTipos[x]][0]
				valores.append(tiposAtomicos[listaDeTipos[x]][0])
			for y in range(0,len(listaDeTipos)-1):
				valores[y+1]=MCM(valores[y],valores[y+1])
			alineacion = (valores[len(valores)-1])
			tamano = max(valores)
			desperdicio = max(valores)-min(valores)
			tiposAtomicos[nombre] = [tamano,alineacion,desperdicio]
			return ultimo+tamano
		else:
			print("Los tipos introducidos en el tipo Union no existen")
'''La funcion crearTiposStruct toma el nombre de un tipo y su lista de tipos y crea un tipo struct basandose en el 
guardado del registro sin empaquetar, ya que es uno de los mas rapidos. 
'''
def crearTipoStruct(nombre, listaDeTipos,ultimo):
	#verificar que los tipos de la lista existen 
	if verificarTipo(nombre) == True:
		print("El nombre "+nombre+" ya corresponde a un tipo creado")
	else:
		if verificarListaTipos(listaDeTipos) == True:
			return noEmpaquetado(nombre,listaDeTipos,ultimo)
		else:
			print("Los tipos introducidos en el tipo Struct no existen")
'''La funcion crearTipoAtomico toma el nombre de un tipo, su representacion y su alineacion y lo guarda dentro del diccionario
de todos los tipos del programa tiposAtomicos.
'''
def crearTipoAtomico(nombre,representacion,alineacion):
	if verificarTipo(nombre) == True:
		print("El nombre "+nombre+" ya corresponde a un tipo creado")
	else:
		#guardar tipo
		tiposAtomicos[nombre] = [int(representacion),int(alineacion)]
		
'''La funcion main se encarga de manejar las entradas del usuario y ademas inicializa el valor de la memoria con ultimo en 0, lo actualiza 
cada vez que se hace llamada a la creacion de algun tipo que no sea atomico.
'''
def main():
	funciona = True
	ultimo = 0
	while funciona:
		entrada = str(input(":"))
		e1 = entrada.find("ATOMICO")
		e2 = entrada.find("STRUCT")
		e3 = entrada.find("UNION")
		e4 = entrada.find("DESCRIBIR")
		e5 = entrada.find("SALIR")
		if e1 == 0:
			separacion = entrada.split(" ")
			crearTipoAtomico(separacion[1],separacion[2],separacion[3])
		elif e2 == 0:
			separacion = entrada.split(" ")
			ultimo = crearTipoStruct(separacion[1],separacion[2:],ultimo)
		elif e3 == 0:
			separacion = entrada.split(" ")
			ultimo = crearTipoUnion(separacion[1],separacion[2:],ultimo)
		elif e4 == 0:
			separacion = entrada.split(" ")
			if len(separacion) >2:
				print("Para describir un tipo, inserte solo su nombre")
			else:
				describirTipo(separacion[1])
		elif e5 == 0:
			funciona = False
		if e1 != 0 and e2 != 0 and e3 != 0 and e4 != 0 and e5!=0:
			print("La entrada no es valida")
			
main()
