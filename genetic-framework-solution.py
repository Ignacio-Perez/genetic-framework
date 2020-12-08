# -*- coding: utf-8 -*-
#=====================================================================
# IA: Ejercicio 2 entregable para el grupo 2 de IA (TI)
# Algoritmos geneticos
# Dpto. de C. de la Computación e I.A. (Univ. de Sevilla)
#=====================================================================

# PROFESOR: Ignacio Perez Hurtado de Mendoza
# perezh at us dot es

#=====================================================================
# FRAMEWORK DE ALGORITMOS GENETICOS
#=====================================================================
# En este ejercicio vamos a sacar partido de la programacion orientada a objetos
# y hacer uso de algunos patrones de disenyo para hacer un software de calidad.

# ¿Que es un patron de disenyo?
# https://en.wikipedia.org/wiki/Software_design_pattern

# Los patrones que usaremos seran los siguientes:
# Singleton pattern: https://en.wikipedia.org/wiki/Singleton_pattern
# Strategy pattern: https://en.wikipedia.org/wiki/Strategy_pattern

# No hace falta tener conocimiento previo de patrones de disenyo, pero se recomienda
# revisar los enlaces anteriores. El ejercicio va a estar guiado punto a punto
# y solo habra que completar codigo. El objetivo de este ejercicio es aprender
# a crear un framework en Python para algoritmos geneticos y resolver un problema interesante. 
# Dicho sea de paso, tener conocimiento de patrones de disenyo es algo muy importante 
# de cara al mercado laboral, asi que aprovechad este ejercicio para tener una experiencia
# practica en Python.

# ¿Empezamos?

#=====================================================================

# PRIMERA PARTE: DEFINICION DE CLASES Y METODOS [5 puntos]

#=====================================================================

# Necesitaremos el modulo random:
import random

# Necesitaremos el modulo time para medir tiempos:
import time

# Necesitaremos math para alguna funcion
import math

#======================================================================
# Vamos a definir una clase Cromosoma para codificar el genotipo de un individuo

class Cromosoma(object):
    
    # Constructor que recibe un cromosoma como lista de genes y crea el objeto de tipo cromosoma
    def __init__(self,cromosoma):
        if (not isinstance(cromosoma,list)): # Primeramente miramos si el cromosoma que nos han pasado es una lista
            raise Exception("Error: el cromosoma debe venir representado como lista")
        if (len(cromosoma)==0): # El cromosoma debe tener al menos un elemento
            raise Exception("Error: la longitud del cromosoma es cero")
        self.__cromosoma = cromosoma # Los atributos que empiezan por dos guiones bajos son privados, ojo se esta pasando la lista por referencia
        self.__valor = None # Este es el valor de fitness del cromosoma, inicialmente vacio
        
        
    def evalua(self,fitness): # metodo que recibe una funcion de fitness y actualiza el valor del cromosoma
        self.__valor = fitness(self.__cromosoma)    
        
        
    def getGen(self,i):
       return self.__cromosoma[i]
    
    
    @property
    def valor(self):
        return self.__valor;
     
    @property
    def cromosoma(self):
        return self.__cromosoma

    @property
    def longitud(self):
        return len(self.__cromosoma)

    def setGen(self,i,gen): # Esta funcion cambia un gen del cromosoma
        self.__cromosoma[i] = gen

    def __str__(self): # Este metodo genera una cadena de texto para el cromosoma, es como toString de Java
        cad = str(self.__cromosoma)
        if (self.__valor != None):
            cad += " " + str(self.__valor)
        return cad
        
    def __repr__(self): # Este metodo es necesario para imprimir por pantalla el cromosoma
        return self.__str__()

#========================================================================
# EJEMPLOS:

# >> cr1 = Cromosoma([1,0,1,1,1,0,1,0,0,1])
# >> cr1
# [1, 0, 1, 1, 1, 0, 1, 0, 0, 1]
# >> cr1.longitud
# 10
# >> cr1.getGen(4)
# 1
# >> cr1.setGen(4,0)
# >> cr1.getGen(4)
# 0
# >> cr1
# [1, 0, 1, 1, 0, 0, 1, 0, 0, 1]

def binario_a_decimal(x):
    return sum(b*(2**i) for (i,b) in enumerate(x)) 
    

def fitness1(cromosoma):
    x = binario_a_decimal(cromosoma)
    return x**2

# >> cr1.evalua(fitness1)
# >> cr1.valor
# 346921

#===========================================================================

# Definimos una clase Poblacion como un wrapper sobre una lista de individuos, esto
# nos vendra bien si luego queremos anyadir mas atributos, como la suma total del fitness de los individuos
# Python permite anyadir atributos a un objeto de forma dinamica

class Poblacion(object):
    def __init__(self,individuos):
        if (not isinstance(individuos,list)): # Primeramente miramos si los individuos vienen como lista
            raise Exception("Error: los individuos deben venir definidos como lista")
        if (len(individuos)==0): # Debe haber almenos un individuo
            raise Exception("Error: poblacion vacia")
        self.individuos = individuos # Es un atributo publico
   
    def __str__(self): # Este metodo genera una cadena de texto para el cromosoma, es como toString de Java
        return str(self.individuos)
        
    def __repr__(self): # Este metodo es necesario para imprimir por pantalla el cromosoma
        return self.__str__()

#========================================================================
#EJEMPLOS:

# >> cr1 = Cromosoma([1,0,1,1,1,0,1,0,0,1])
# >> cr2 = Cromosoma([0,0,1,1,0,1,0,0,1,1])
# >> individuos = [cr1,cr2]
# >> poblacion = Poblacion(individuos)
# >> poblacion
# [[1, 0, 1, 1, 1, 0, 1, 0, 0, 1], [0, 0, 1, 1, 0, 1, 0, 0, 1, 1]]

#========================================================================
# Vamos a definir una clase DefinicionGenotipo para definir las caracteristicas del genotipo de un problema genetico, 
# es decir, la lista de genes y la longitud de individuos

class DefinicionGenotipo(object):
    # La clase DefinicionGenotipo recibe una lista de genes y la longitud de individuos    
    
    def __init__(self,genes,longitud):
        if (not isinstance(genes,list)): # Primeramente miramos si los genes que nos han pasado vienen como lista
            raise Exception("Error: los genes deben venir representados como lista")
        if (len(set(x for x in genes)) != len(genes)): # No pueden haber genes repetidos
            raise Exception("Error: hay genes repetidos")
        if (len(genes)<2): # Al menos necesitamos 2 genes diferentes
            raise Exception("Error: insuficientes genes")
        if (longitud<=0):
            raise Exception("Error: la longitud de individuos debe ser mayor o igual que cero")
        self.__genes = genes
        self.__longitud = longitud
   
    @property
    def genes(self):
        return self.__genes
    
    @property
    def longitud(self):
        return self.__longitud

    def __str__(self): 
        return ''.join(("genes: ",str(self.__genes),". Longitud de individuos: ",str(self.__longitud)))
        
    def __repr__(self):
        return self.__str__()


#===============================================================================
# EJEMPLOS:
       
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> cuad_gen
# genes: [0, 1]. Longitud de individuos: 10


#==============================================================================
# Vamos a usar el patron Estrategia para definir diferentes estrategias de mutacion, para ello
# primero crearemos una clase abstracta EstrategiaMutacion que tiene un metodo "muta" que recibe un
# objeto de tipo Cromosoma, una probabilidad de mutacion, la definicion de un genotipo y realiza una mutacion 

# Strategy pattern: https://en.wikipedia.org/wiki/Strategy_pattern

class EstrategiaMutacion(object):

    def muta(self, cromosoma, prob, definicionGenotipo):  # Habra que implementar esta funcion en las clases heredadas
         raise NotImplementedError('EstrategiaMutacion es una clase abstracta!')

#=======================================================================

# A continuacion se implementa la mutacion en un punto (pagina 10 del tema 5)
# Usaremos el patron Singleton. Este codigo se proporciona como ejemplo para los siguientes ejercicios.

#https://es.wikipedia.org/wiki/Singleton

class MutacionEnUnPunto(EstrategiaMutacion):
    # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def muta(self, cromosoma, prob, definicionGenotipo): # Implementamos el metodo
        for i in range(cromosoma.longitud):
            if (random.random()<prob):
                cromosoma.setGen(i,random.sample(definicionGenotipo.genes,1)[0])


#=======================================================================
# EJEMPLOS:
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> cr1 = Cromosoma([1,0,0,1,1,0,1,0,1,0])
# >> MutacionEnUnPunto().muta(cr1,0.2,cuad_gen)
# >> cr1
# [1, 0, 0, 1, 1, 0, 0, 0, 1, 0]
# >> MutacionEnUnPunto().muta(cr1,0.2,cuad_gen)
# >> cr1
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 0]
#========================================================================
#EJERCICIO 1 [0.5 puntos]: Define la clase MutacionPorIntercambio, que debe heredar
# de EstrategiaMutacion, ser una clase singleton e implementar la mutacion 
# por intercambio (pagina 11 del tema 5). 
# Nota: Aplicar la mutacion solo si un numero entero al azar en [0,1) es menor que la probabilidad dada.


class MutacionPorIntercambio(EstrategiaMutacion):
    # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
 
    def muta(self, cromosoma, prob, definicionGenotipo):
        if (random.random()<prob):
            i = random.randint(0,cromosoma.longitud-1)
            j = random.randint(0,cromosoma.longitud-1)
            gen = cromosoma.getGen(i)
            cromosoma.setGen(i,cromosoma.getGen(j))
            cromosoma.setGen(j,gen)


#=======================================================================
# EJEMPLOS:

# >> ciudades =DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE',],8)
# >> cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
# >> MutacionPorIntercambio().muta(cr1,0.5,ciudades)
# >> cr1
# ['HU', 'MA', 'CA', 'SE', 'AL', 'CO', 'GR', 'JA']
# >> MutacionPorIntercambio().muta(cr1,0.5,ciudades)
# >> cr1
# ['CA', 'MA', 'HU', 'SE', 'AL', 'CO', 'GR', 'JA']


#========================================================================

#EJERCICIO 2 [0.5 puntos]: Define la clase MutacionPorMezcla, que debe heredar
# de EstrategiaMutacion, ser una clase singleton e implementar la mutacion 
# por mezcla (pagina 11 del tema 5). 
# Nota: Aplicar la mutacion solo si un numero entero al azar en [0,1) es menor que la probabilidad

class MutacionPorMezcla(EstrategiaMutacion):
    # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
 
    def muta(self, cromosoma, prob, definicionGenotipo):
        if (random.random()<prob):
            i = random.randint(0,cromosoma.longitud-1)
            j = random.randint(0,cromosoma.longitud-1)
            a = min(i,j)
            b = max(i,j)+1
            l = cromosoma.cromosoma[a:b]
            random.shuffle(l)
            for i in range(a,b):
                cromosoma.setGen(i,l[i-a])
                
            
            


#========================================================================
# EJEMPLOS:

# >> ciudades = DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE',],8)
# >> cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
# >> MutacionPorMezcla().muta(cr1,1.0,ciudades)
# >> cr1
# ['HU','SE','CA','AL','MA','GR','CO','JA']
# >> MutacionPorMezcla().muta(cr1,0.5,ciudades)
# >> cr1
# ['HU', 'MA', 'SE', 'GR', 'CA', 'AL', 'CO', 'JA']

#========================================================================

# Vamos a usar el patron Estrategia tambien para definir diferentes estrategias de cruce, para ello
# primero crearemos una clase abstracta EstrategiaCruce que tiene un metodo "cruza" que recibe dos
# objetos de tipo Cromosoma y realiza un cruce devolviendo una lista de dos elementos con los dos
# cromosomas hijos.


class EstrategiaCruce(object):

    def cruza(self, cromosoma1, cromosoma2): # Habra que implementar esta funcion en las clases heredadas
         raise NotImplementedError('EstrategiaCruce es una clase abstracta!')

#=======================================================================

# A Continuacion se muestra como ejemplo la clase CruceEnUnPunto que implementa el cruce en un punto

class CruceEnUnPunto(EstrategiaCruce):
    # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def cruza(self, cromosoma1, cromosoma2):
        if (cromosoma1.longitud != cromosoma2.longitud):
            raise Exception("Error: Los cromosomas deben tener la misma longitud")
        pos=random.randrange(1,cromosoma1.longitud-1)
        l1= cromosoma1.cromosoma[:pos] + cromosoma2.cromosoma[pos:] 
        l2= cromosoma2.cromosoma[:pos] + cromosoma1.cromosoma[pos:] 
        return [Cromosoma(l1),Cromosoma(l2)]
        
        
#========================================================================
# EJEMPLOS:
# >> cr1 = Cromosoma([1,0,0,1,1,0,1,0,1,0])        
# >> cr2 = Cromosoma([0,0,1,0,0,1,1,1,0,1])        
# >> CruceEnUnPunto().cruza(cr1,cr2) 
# [[1, 0, 0, 1, 1, 0, 1, 0, 0, 1], [0, 0, 1, 0, 0, 1, 1, 1, 1, 0]]
# >> CruceEnUnPunto().cruza(cr1,cr2)
# [[1, 0, 1, 0, 0, 1, 1, 1, 0, 1], [0, 0, 0, 1, 1, 0, 1, 0, 1, 0]]

#=======================================================================
# EJERCICIO 3  [1 punto]: Define la clase CruceBasadoEnOrden, que debe heredar
# de EstrategiaCruce, ser una clase singleton e implementar el cruce basado
# en orden (pagina 13 del tema 5). 

 
class CruceBasadoEnOrden(EstrategiaCruce):
    # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance

    def cruza(self, cromosoma1, cromosoma2):
        if (cromosoma1.longitud != cromosoma2.longitud):
            raise Exception("Error: Los cromosomas deben tener la misma longitud")
        pos1=random.randrange(1,cromosoma1.longitud-1)
        pos2=random.randrange(1,cromosoma1.longitud-1)
        if (pos1>pos2):
            aux = pos1
            pos1 = pos2
            pos2 = aux
        l1 = [None]*cromosoma1.longitud
        l2 = [None]*cromosoma1.longitud
        for i in range(pos1,pos2+1):
            l1[i] = cromosoma1.getGen(i)
            l2[i] = cromosoma2.getGen(i)
        indices = [x for x in range(pos2+1,cromosoma1.longitud)]+[x for x in range (0,pos2+1)]
        c1=(pos2+1)%cromosoma1.longitud
        c2=(pos2+1)%cromosoma1.longitud
        for i in indices:
            if (cromosoma2.getGen(i) not in l1):
                l1[c1]=cromosoma2.getGen(i)
                c1 = (c1+1)%cromosoma1.longitud
            if (cromosoma1.getGen(i) not in l2):
                l2[c2]=cromosoma1.getGen(i)
                c2 = (c2+1)%cromosoma1.longitud
        
        
        return [Cromosoma(l1),Cromosoma(l2)]
            
    
#======================================================================
# EJEMPLOS:
# >>  cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
# >>  cr2 = Cromosoma(['AL','CO','HU','SE','GR','CA','JA','MA'])  
# >> CruceBasadoEnOrden().cruza(cr1,cr2)
# [['SE', 'CA', 'JA', 'MA', 'AL', 'CO', 'GR', 'HU'],
#  ['MA', 'AL', 'CO', 'SE', 'GR', 'CA', 'JA', 'HU']]

# >> CruceBasadoEnOrden().cruza(cr1,cr2)        
# [['HU', 'SE', 'CA', 'GR', 'JA', 'MA', 'AL', 'CO'],
#  ['CA', 'CO', 'HU', 'MA', 'AL', 'GR', 'JA', 'SE']]


#======================================================================
# EJERCICIO 4 [1 punto]: Define la clase CruceBasadoEnCiclos, que debe heredar
# de EstrategiaCruce, ser una clase singleton e implementar el cruce basado
# en ciclos (pagina 15 del tema 5). 
# Nota1: Recuerda que puedes usar funciones auxiliares (opcional), pero respeta el paradigma
# de programacion orientada a objetos y encapsula las funciones auxiliares como
# funciones privadas de la clase.
# Nota2: Una funcion privada debe tener un nombre que comienza por dos guiones bajos.


class CruceBasadoEnCiclos(EstrategiaCruce):
     # Esto implementa el patron singleton    
    instance = None
    
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
    
    def __generaCiclos(self, cromosoma1, cromosoma2):
        ciclos = [None]*cromosoma1.longitud
        contador=0
        inicio = 0
        while (inicio<cromosoma1.longitud):
            i = inicio
            while (ciclos[i]==None):
                ciclos[i] = contador
                i = cromosoma1.cromosoma.index(cromosoma2.cromosoma[i])
            contador+=1
            while (inicio<cromosoma1.longitud and ciclos[inicio] != None):
                inicio+=1
        return ciclos    
    
    def cruza(self, cromosoma1, cromosoma2):    
        if (cromosoma1.longitud != cromosoma2.longitud):
            raise Exception("Error: Los cromosomas deben tener la misma longitud")
        ciclos = self.__generaCiclos(cromosoma1,cromosoma2)
        l1 = [None]*cromosoma1.longitud
        l2 = [None]*cromosoma1.longitud
        for i in range(cromosoma1.longitud):
            if (ciclos[i]%2 == 0):
                l1[i] = cromosoma1.getGen(i)
                l2[i] = cromosoma2.getGen(i)
            else:
                l1[i] = cromosoma2.getGen(i)
                l2[i] = cromosoma1.getGen(i)  
        return [Cromosoma(l1),Cromosoma(l2)]
            
        

#====================================================================
# EJEMPLOS:
# >>  cr1 = Cromosoma(['HU','SE','CA','MA','AL','CO','GR','JA'])
# >>  cr2 = Cromosoma(['JA','HU','GR','SE','AL','CA','CO','MA'])  
# >> CruceBasadoEnCiclos().cruza(cr1,cr2)
# [['HU', 'SE', 'GR', 'MA', 'AL', 'CA', 'CO', 'JA'],
#  ['JA', 'HU', 'CA', 'SE', 'AL', 'CO', 'GR', 'MA']]

# >>  cr1 = Cromosoma([1,2,3,4,5,6,7,8,9])
# >>  cr2 = Cromosoma([9,3,7,8,2,6,5,1,4])  
# >> CruceBasadoEnCiclos().cruza(cr1,cr2)
# [[1, 3, 7, 4, 2, 6, 5, 8, 9], [9, 2, 3, 8, 5, 6, 7, 1, 4]]


#=====================================================================
# Para generar individuos iniciales tambien usaremos el patron Estrategia,
# mediante la clase EstrategiaGenerador que tiene el metodo generaIndividuo
# que devuelve un individuo aleatorio inicial. Tambien tiene un metodo generaPoblacion
# que devuelve una poblacion inicial

class EstrategiaGenerador(object):
    
     def generaIndividuo(self, definicionGenotipo):  # Habra que implementar esta funcion en las clases heredadas
         raise NotImplementedError('EstrategiaGenerador es una clase abstracta!')
         
     def generaPoblacion(self, definicionGenotipo, tamPoblacion):
         individuos = [None]*tamPoblacion         
         for i in range(tamPoblacion):
            individuos[i] = self.generaIndividuo(definicionGenotipo)
         return Poblacion(individuos)
         
     def generaPoblacionEvaluada(self, definicionGenotipo, tamPoblacion, fitness):
         individuos = [None]*tamPoblacion         
         for i in range(tamPoblacion):
            individuos[i] = self.generaIndividuo(definicionGenotipo)
            individuos[i].evalua(fitness)
         return Poblacion(individuos)

#=====================================================================
# Como ejemplo, se incluye el codigo de la clase GeneradorConRepetidos (singleton), 
# que genera un individuo inicial aleatorio permitiendo genes repetidos

class GeneradorConRepetidos(EstrategiaGenerador):
    # Esto implementa el patron singleton    
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
        
    def generaIndividuo(self, definicionGenotipo):
        l = [None]*definicionGenotipo.longitud
        for i in range(definicionGenotipo.longitud):
             l[i] = random.choice(definicionGenotipo.genes)
        return Cromosoma(l)

#=======================================================================
# Ejemplos:
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> GeneradorConRepetidos().generaIndividuo(cuad_gen) 
#  [1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
# >> GeneradorConRepetidos().generaIndividuo(cuad_gen) 
# [1, 0, 1, 0, 0, 0, 1, 1, 0, 1]
# >> GeneradorConRepetidos().generaPoblacion(cuad_gen,5) 
# [[1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
#  [0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
#  [0, 1, 1, 1, 1, 0, 0, 1, 0, 1],
#  [0, 0, 1, 0, 1, 1, 0, 1, 0, 0],
#  [1, 1, 0, 0, 1, 0, 1, 0, 1, 1]]

# >> GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1)
# [[0, 0, 1, 0, 1, 1, 1, 0, 0, 1] 394384, 
#  [1, 0, 1, 0, 1, 0, 0, 0, 0, 0] 441,
#  [1, 0, 0, 1, 0, 0, 0, 1, 0, 0] 18769, 
#  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0] 74529, 
#  [0, 1, 0, 1, 1, 1, 0, 1, 1, 1] 910116]


#========================================================================
# EJERCICIO 5 [0.5 puntos]: Define la clase GeneradorPermutacion, que debe heredar de EstrategiaGenerador,
# ser una clase singleton e implementar la generacion de individuos como una permutacion
# aleatoria de la lista de genes. No se permiten genes repetidos 

class GeneradorPermutacion(EstrategiaGenerador):
    # Esto implementa el patron singleton    
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance
        
    def generaIndividuo(self, definicionGenotipo):
        l = list(definicionGenotipo.genes)
        random.shuffle(l)
        return Cromosoma(l)

#========================================================================
# Ejemplos:
# >> ciudades = DefinicionGenotipo(['AL','CA','CO','GR','HU','MA','JA','SE',],8) 
# >> GeneradorPermutacion().generaIndividuo(ciudades)
# ['AL', 'CA', 'HU', 'GR', 'JA', 'SE', 'MA', 'CO']
# >> GeneradorPermutacion().generaIndividuo(ciudades)
# ['HU', 'JA', 'AL', 'MA', 'CO', 'CA', 'SE', 'GR']

# GeneradorPermutacion().generaPoblacion(ciudades,5)
# [['CO', 'HU', 'SE', 'GR', 'MA', 'AL', 'JA', 'CA'],
#  ['CA', 'HU', 'AL', 'MA', 'CO', 'JA', 'GR', 'SE'],
#  ['CA', 'MA', 'JA', 'AL', 'HU', 'CO', 'SE', 'GR'],
#  ['HU', 'MA', 'CO', 'GR', 'SE', 'AL', 'JA', 'CA'],
#  ['MA', 'JA', 'CA', 'HU', 'SE', 'GR', 'AL', 'CO']]

#=======================================================================       
# Definamos ahora una clase Estrategia para los metodos de seleccion de individuos,
# esta clase tiene el metodo selecciona que recibe una poblacion EVALUADA (lista de cromosomas con su valor asignado)
# y devuelve un individuo de acuerdo al criterio de seleccion. Adicionalmente tiene el metodo
# seleccionaLista, que recibe una poblacion y un numero entero n (n >0), devolvera una
# lista de n individuos seleccionados.

class EstrategiaSeleccion(object):
    # Este metodo es opcional y prepara una poblacion para facilitar los calculos de 
    # de la seleccion de individuos. No poner codigo aqui, si hace falta se implementa
    # en las clases heredadas.      
    def preparaPoblacion(self, poblacionEvaluada):
        pass

    def selecciona(self, poblacionEvaluada):  # Habra que implementar esta funcion en las clases heredadas
        raise NotImplementedError('EstrategiaSeleccion es una clase abstracta!')
  
    def seleccionaLista(self, poblacionEvaluada, n):
        seleccion = [None]*n        
        for i in range(n):
            seleccion[i] = self.selecciona(poblacionEvaluada)
        return seleccion
    

#========================================================================
# EJERCICIO 6 [0.5 puntos]: Completar el codigo de la clase SeleccionTorneo.
# esta clase tiene dos atributos tamTorneo (K en los apuntes), para indicar el numero
# de individuos que se eligen aleatoriamente para participar en el torneo. Y opt
# que es la funcion max o min dependiendo de si queremos maximizar o minimizar
# Nota1: No es un singleton ya que tiene argumentos (tamTorneo y opt)
# Nota2: quitar la linea que pone pass e introducir vuestro codigo. 

class SeleccionTorneo(EstrategiaSeleccion):

    def __init__(self,tamTorneo,opt):
        self._tamTorneo = tamTorneo
        self._opt = opt
    
    @property
    def tamTorneo(self):
        return self._tamTorneo
        
    @property
    def opt(self):
        return self._opt
    
    def selecciona(self, poblacionEvaluada):
        torneo = random.sample(poblacionEvaluada.individuos,self._tamTorneo)
        return self._opt(torneo,key = lambda x : x.valor)
       

#===========================================================================
# EJEMPLO:
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> poblacion = GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1)
# >> poblacion
# [[1, 0, 1, 1, 1, 1, 1, 0, 1, 1] 797449,
# [1, 1, 0, 0, 0, 1, 1, 1, 1, 1] 990025,
# [1, 1, 1, 1, 1, 0, 0, 0, 1, 1] 638401,
# [1, 0, 0, 0, 1, 1, 0, 1, 1, 0] 187489,
# [0, 0, 0, 1, 1, 0, 0, 1, 0, 0] 23104]

# >> SeleccionTorneo(4,min).selecciona(poblacion)
# [0, 0, 0, 1, 1, 0, 0, 1, 0, 0] 23104

# >> SeleccionTorneo(4,max).selecciona(poblacion)
# [1, 1, 0, 0, 0, 1, 1, 1, 1, 1] 990025

# >> SeleccionTorneo(3,min).seleccionaLista(poblacion,3)
# [[1, 0, 0, 0, 1, 1, 0, 1, 1, 0] 187489,
#  [1, 0, 0, 0, 1, 1, 0, 1, 1, 0] 187489,
#  [0, 0, 0, 1, 1, 0, 0, 1, 0, 0] 23104]

#=============================================================================
# EJERCICIO 7 [0.5 puntos]: Completar el codigo de la clase SeleccionRuleta que 
# hereda de EstrategiaSeleccion.
# Esta clase es un singleton y debe implementar el metodo selecciona, 
# tambien conocido como metodo proporcional a la valoracion
# Ver tema 5 (paginas 17-19)
# Nota: quitar la linea que pone pass e introducir vuestro codigo

class SeleccionRuleta(EstrategiaSeleccion):
  # Esto implementa el patron singleton    
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
        return cls.instance    
    
    
    # El metodo preparaPoblacion calcula la suma total de todas las funciones de fitness
    # y tambien la suma acumulada. En python se pueden anyadir nuevos atributos a un objeto de forma dinamica
    # previamente ordena la poblacion de mayor a menor fitness para que las selecciones sean mas eficientes
    def preparaPoblacion(self,poblacionEvaluada):
        poblacionEvaluada.individuos.sort(key= lambda x : x.valor, reverse=True)
        suma = 0
        for individuo in poblacionEvaluada.individuos:
            suma+=individuo.valor
            individuo.sumaParcial = suma
        poblacionEvaluada.sumaTotal = suma
        

    #definir el metodo selecciona, tened en cuenta que podeis usar el atributo sumaTotal de la poblacion
    #y el atributo sumaParcial para cada individuo, pues la poblacion ya ha sido preparada antes de llamar a esta funcion
    def selecciona(self, poblacionEvaluada):
        x = random.random()*poblacionEvaluada.sumaTotal;
        for individuo in poblacionEvaluada.individuos:
            if individuo.sumaParcial > x:
                return individuo
        return None
    

#==================================================================
# EJEMPLO:
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> poblacion = GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1)
# >> poblacion
# [[1, 0, 0, 0, 0, 1, 0, 0, 0, 0] 1089, 
#  [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096, 
#  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0] 74529,
#  [0, 1, 0, 0, 1, 0, 1, 1, 0, 0] 44100,
#  [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264]

# >> SeleccionRuleta().preparaPoblacion(poblacion)
# >> poblacion  
# [[0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264,
#  [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096,
#  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0] 74529,
#  [0, 1, 0, 0, 1, 0, 1, 1, 0, 0] 44100,
#  [1, 0, 0, 0, 0, 1, 0, 0, 0, 0] 1089]

# >> SeleccionRuleta().selecciona(poblacion)
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264

# >> SeleccionRuleta().selecciona(poblacion)
# [0, 1, 0, 0, 1, 0, 1, 1, 0, 0] 44100

# >> SeleccionRuleta().selecciona(poblacion)
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264

# >> SeleccionRuleta().selecciona(poblacion)
# [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096

# >> SeleccionRuleta().seleccionaLista(poblacion,3)
# [[0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264,
# [0, 0, 1, 0, 1, 1, 0, 1, 1, 0] 190096,
# [0, 0, 0, 1, 1, 0, 0, 0, 1, 1] 627264]


#================================================================================
# EJERCICIO 8 [0.5 puntos]  Completar el codigo de la clase SeleccionElitista.
# esta clase tiene dos atributos propElite (numero real entre 0 y 1), para indicar
# la proporcion de individuos de la seleccion que perteneceran a la elite. Y opt
# que es la funcion max o min dependiendo de si queremos maximizar o minimizar
# Nota1: No es un singleton ya que tiene argumentos (propElite y opt)
# Nota2: quitar la linea que pone pass e introducir vuestro codigo.
# Nota3: Fijarse que aqui no implementamos el metodo selecciona sino seleccionaLista 

class SeleccionElitista(EstrategiaSeleccion):

    def __init__(self,propElite,opt):
        self.__propElite = propElite
        self.__opt = opt
    
    @property
    def propElite(self):
        return self.__propElite
        
    @property
    def opt(self):
        return self.__opt
    
     
    # El metodo preparaPoblacion ordena la poblacion de mejor a peor fitness 
    def preparaPoblacion(self,poblacionEvaluada):
        if (self.__opt == max):
            poblacionEvaluada.individuos.sort(key= lambda x : x.valor, reverse=True)
        else:
            poblacionEvaluada.individuos.sort(key= lambda x : x.valor)
    # Esta clase modifica el metodo seleccionaLista de la clase padre.
    # No es necesario implementar el metodo selecciona.
    # Elegir los primeros n*propEliteindividuos de la poblacion evaluada
    # Elegir aleatoriamente los restantes individuos de entre el resto 
    # (hasta completar n)
    # Mirar explicacion en pagina 20 del tema 5
    def seleccionaLista(self, poblacionEvaluada, n):
        seleccion = [None]*n
        elite = int(self.__propElite * n)        
        for i in range(elite):
            seleccion[i] = poblacionEvaluada.individuos[i]
        for i in range(elite,n):
            j = random.randint(elite,len(poblacionEvaluada.individuos)-1)
            seleccion[i] = poblacionEvaluada.individuos[j]
        return seleccion


#===============================================================================
# >> cuad_gen = DefinicionGenotipo([0,1],10)
# >> poblacion = GeneradorConRepetidos().generaPoblacionEvaluada(cuad_gen,5,fitness1)
# [[0, 0, 0, 0, 1, 0, 0, 1, 0, 1] 430336, 
#  [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556, 
#  [0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904, 
#  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281, 
#  [1, 0, 0, 1, 1, 1, 1, 1, 1, 0] 255025]


# >> SeleccionElitista(0.5,min).preparaPoblacion(poblacion)
# >> poblacion
# [[0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904, 
#  [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281, 
#  [1, 0, 0, 1, 1, 1, 1, 1, 1, 0] 255025, 
#  [0, 0, 0, 0, 1, 0, 0, 1, 0, 1] 430336,
#  [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556]

# >> SeleccionElitista(0.5,min).seleccionaLista(poblacion,4)
# [[0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904,
# [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281,
# [1, 0, 0, 1, 1, 1, 1, 1, 1, 0] 255025,
# [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556]

# >> SeleccionElitista(0.5,min).seleccionaLista(poblacion,4)
# [[0, 0, 1, 0, 1, 0, 0, 1, 0, 0] 21904,
# [1, 0, 1, 0, 1, 0, 1, 0, 1, 0] 116281,
# [0, 1, 0, 0, 0, 0, 1, 0, 1, 1] 695556,
# [0, 0, 0, 0, 1, 0, 0, 1, 0, 1] 430336]



#================================================================================
# Vamos a definir la clase ProblemaGenetico incluyendo todo lo necesario:
# DefinicionGenotipo
# EstrategiaMutacion
# EstrategiaCruce
# EstrategiaGenerador
# EstrategiaSeleccion
# Funcion de fitness (igual que en la practica 5)
# Funcion decodifica (igual que en la practica 5)

class ProblemaGenetico(object):
    
    def __init__(self,definicionGenotipo, 
                      estrategiaMutacion, 
                      estrategiaCruce, 
                      estrategiaGenerador, 
                      estrategiaSeleccion,
                      fitness,
                      decodifica):

        self.definicionGenotipo = definicionGenotipo
        self.estrategiaMutacion = estrategiaMutacion
        self.estrategiaCruce = estrategiaCruce
        self.estrategiaGenerador = estrategiaGenerador
        self.estrategiaSeleccion = estrategiaSeleccion
        self.fitness = fitness
        self.decodifica = decodifica

    def muta(self,c,prob):
        self.estrategiaMutacion.muta(c,prob,self.definicionGenotipo)
   
    def cruza(self, c1, c2):
        return self.estrategiaCruce.cruza(c1,c2)
        
    def generaPoblacionInicial(self, tamPoblacion):
        return self.estrategiaGenerador.generaPoblacionEvaluada(self.definicionGenotipo,tamPoblacion,self.fitness)
    
    def preparaPoblacion(self,p):
        self.estrategiaSeleccion.preparaPoblacion(p)
        
    def seleccionaLista(self,p,n):
        return self.estrategiaSeleccion.seleccionaLista(p,n)

    def decodifica(self,c):
        return self.decodifica(c)
        
    def evalua(self,c):
        c.evalua(self.fitness)
      
    # Algoritmo genetico segun pseudocodigo de la pagina 22 del tema 5
      # Parametros: 
      # propCruce: proporcion de individuos que se van a cruzar (numero real en [0,1]
      # probMutar: probabilidad de mutacion (numero real en [0,1])
      # generaciones: numero de generaciones en el bucle principal (numero entero >0)
      # tamPoblacion: numero de individuos en la poblacion
      # opt: funcion "max" si estamos maximizando o "min" si estamos minimizando
      # Salida:
      # Una lista con el tiempo de ejecucion en segundos, 
      # el fenotipo y el valor del mejor individuo encontrado
    def ejecutaAlgoritmoGenetico(self,propCruce,probMutar,generaciones,tamPoblacion,opt):
        t0 = time.clock()
        poblacion = self.generaPoblacionInicial(tamPoblacion)
        individuosACruzar = int(round(propCruce * tamPoblacion))
        if (individuosACruzar%2!=0):
            individuosACruzar+=1
        individuosANoCruzar = tamPoblacion - individuosACruzar
        assert (individuosACruzar + individuosANoCruzar) == tamPoblacion
        for generacion in range(generaciones):
            self.preparaPoblacion(poblacion)
            p1 = self.seleccionaLista(poblacion,individuosACruzar)
            p2 = self.seleccionaLista(poblacion,individuosANoCruzar)
            random.shuffle(p1)
            for i in range (0,len(p1),2):
                hijos = self.cruza(p1[i],p1[i+1])
                p1[i] = hijos[0]
                p1[i+1] = hijos[1]
            p4 = p1 + p2
            for individuo in p4:
                self.muta(individuo,probMutar)
                self.evalua(individuo)
            poblacion.individuos = p4
        mejor = opt(poblacion.individuos,key=lambda x : x.valor)
        t1 = time.clock()
        return [t1-t0,self.decodifica(mejor.cromosoma),mejor.valor]
            
      
      
#===============================================================================
           
#EJEMPLO:

# >> cuad_gen1 = ProblemaGenetico(DefinicionGenotipo([0,1],10),MutacionEnUnPunto(),CruceEnUnPunto(),GeneradorConRepetidos(),SeleccionRuleta(),fitness1,binario_a_decimal)
# >> cuad_gen1.ejecutaAlgoritmoGenetico(0.6,0.1,500,100,max)  
# [1.0463019999999972, 1023, 1046529]


# >> cuad_gen2 = ProblemaGenetico(DefinicionGenotipo([0,1],10),MutacionEnUnPunto(),CruceEnUnPunto(),GeneradorConRepetidos(),SeleccionTorneo(10,min),fitness1,binario_a_decimal)
# >> cuad_gen2.ejecutaAlgoritmoGenetico(0.6,0.1,500,100,min)  
# [1.5345849999999999, 0, 0]




#==================================================================================    
           
# SEGUNDA PARTE: EXPERIMENTACION  [5 puntos]
           
#==================================================================================

# PROBLEMA DEL VIAJANTE
# A continuacion se detallan las coordenadas cartesianas de 53 localizaciones en la ciudad de Berlin.

localizacion = [None]*53
localizacion[0]= (386.0, 825.0)
localizacion[1]= (565.0, 575.0)
localizacion[2]= (25.0, 185.0)
localizacion[3]= (345.0, 750.0)
localizacion[4]= (945.0, 685.0)
localizacion[5]= (845.0, 655.0)
localizacion[6]= (880.0, 660.0)
localizacion[7]= (25.0, 230.0)
localizacion[8]= (525.0, 1000.0)
localizacion[9]= (580.0, 1175.0)
localizacion[10]= (650.0, 1130.0)
localizacion[11]= (1605.0, 620.0)
localizacion[12]= (1220.0, 580.0)
localizacion[13]= (1465.0, 200.0)
localizacion[14]= (1530.0, 5.0)
localizacion[15]= (845.0, 680.0)
localizacion[16]= (725.0, 370.0)
localizacion[17]= (145.0, 665.0)
localizacion[18]= (415.0, 635.0)
localizacion[19]= (510.0, 875.0) 
localizacion[20]= (560.0, 365.0)
localizacion[21]= (300.0, 465.0)
localizacion[22]= (520.0, 585.0)
localizacion[23]= (480.0, 415.0)
localizacion[24]= (835.0, 625.0)
localizacion[25]= (975.0, 580.0)
localizacion[26]= (1215.0, 245.0)
localizacion[27]= (1320.0, 315.0)
localizacion[28]= (1250.0, 400.0)
localizacion[29]= (660.0, 180.0)
localizacion[30]= (410.0, 250.0)
localizacion[31]= (420.0, 555.0)
localizacion[32]= (575.0, 665.0)
localizacion[33]= (1150.0, 1160.0)
localizacion[34]= (700.0, 580.0)
localizacion[35]= (685.0, 595.0)
localizacion[36]= (685.0, 610.0)
localizacion[37]= (770.0, 610.0)
localizacion[38]= (795.0, 645.0)
localizacion[39]= (720.0, 635.0)
localizacion[40]= (760.0, 650.0)
localizacion[41]= (475.0, 960.0)
localizacion[42]= (95.0, 260.0)
localizacion[43]= (875.0, 920.0)
localizacion[44]= (700.0, 500.0)
localizacion[45]= (555.0, 815.0)
localizacion[46]= (830.0, 485.0)
localizacion[47]= (1170.0, 65.0)
localizacion[48]= (830.0, 610.0)
localizacion[49]= (605.0, 625.0)
localizacion[50]= (595.0, 360.0)
localizacion[51]= (1340.0, 725.0)
localizacion[52]= (1740.0, 245.0)


# Esta es la definicion del genotipo, en donde cada ciudad es un numero en [0,52]:

berlin_genetico = DefinicionGenotipo([gen for gen in range(0,53)],53)

# Usaremos una clase singleton para precomputar la matriz de distancias y tener disponibles
# todas las distancias sin que tener que calcular una y otra vez la distancia euclidea

class BerlinDistancias(object):
     # Esto implementa el patron singleton    
    instance = None
    def __new__(cls, *args, **kargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls,*args,**kargs)
            cls.instance.__generaDistancias()
        return cls.instance

    def __calculaDistancia(self,i,j):
        return math.sqrt(sum([(a-b)**2 for (a,b) in zip(localizacion[i],localizacion[j])]))
    
    def __generaDistancias(self):
        self.__distancia = [[0 for x in range(len(localizacion))] for y in range(len(localizacion))] 
        self.__minDistancia = None
        self.__maxDistancia = None
        for i in range(len(localizacion)):
            self.__distancia[i][i] = 0.0
            for j in range (i+1,len(localizacion)):
                self.__distancia[i][j] = self.__calculaDistancia(i,j)
                self.__distancia[j][i] = self.__distancia[i][j]
                if (self.__maxDistancia==None or self.__distancia[j][i]>self.__maxDistancia):
                    self.__maxDistancia=self.__distancia[j][i]
                if (self.__minDistancia==None or self.__distancia[j][i]<self.__minDistancia):
                    self.__minDistancia=self.__distancia[j][i]   
                    
    # Devuelve la maxima distancia entre dos localizaciones
    @property
    def maxDistancia(self):
        return self.__maxDistancia
     
    # Devuelve la minima distancia entre dos localizaciones
    @property
    def minDistancia(self):
        return self.__minDistancia
      
    # Devuelve la distancia entre dos localizaciones    
    def distancia(self,i,j):
        return self.__distancia[i][j]
        
   
                            
#==============================================================================      
# EJEMPLOS        
    
# >> BerlinDistancias().distancia(4,2)
# 1047.091209016674

# >> BerlinDistancias().distancia(2,4)
#  1047.091209016674

# >> BerlinDistancias().distancia(2,2)
#  0.0

# >> BerlinDistancias().maxDistancia
# 1716.049241717731

# >> BerlinDistancias().minDistancia
#  15.0



#==============================================================================
# A continuacion proporcionamos la funcion berlinFitness1 que devuelve la distancia del recorrido
# codificado en un cromosoma que viene como lista de genes. No olvidar que la ultima ciudad conecta con la primera 
# Nota: cuando useis esta funcion en el algoritmo genetico, recordad que hay que minimizar

def berlinFitness1(c):
    distancia = 0.0
    for i in range(0,len(c)-1,2):
        distancia += BerlinDistancias().distancia(c[i],c[i+1])
    distancia+=BerlinDistancias().distancia(c[52],c[0])
    return distancia    

#==============================================================================
# EJEMPLOS:
# >> c1 = [x for x in range(0,53)]
# >> berlinFitness1(c1)
# 13066.991153587061

# >> c2 =  [x for x in range(0,53,2)] + [x for x in range(1,53,2)]
# >> berlinFitness1(c2)
# 14328.89331480243

#===============================================================================
# Proporcionamos tambien la funcion berlinFitnesss2 para maximizar, es decir devuelve
# un numero mas grande cuanto mas corto sea el recorrido.


def berlinFitness2(c):
    return BerlinDistancias().maxDistancia * 53 - berlinFitness1(c)

#================================================================================
# EJEMPLOS:
# Nota: no tienen porque salir exactamente estos valores, depende de la implementacion
# >> c1 = [x for x in range(0,53)]
# >> berlinFitness2(c1)
# 77883.61865745268

# >> c2 =  [x for x in range(0,53,2)] + [x for x in range(1,53,2)]
# >> berlinFitness2(c2)
#  76621.71649623732


#==============================================================================
# EJERCICIO 9 [5 puntos]: crear al menos 5 instancias de la clase ProblemaGenetico denominadas
# problemaBerlin1, problemaBerlin2, etc, con las siguientes caracteristicas (elegir a vuestro criterio):
# 1.- Usar la variable berlin_genetico como definicion del genotipo
# 2.- Elegir entre mutacion por intercambio y mutacion por mezcla como estrategia de mutacion
# 3.- Elegir entre cruce basado en orden y cruce basado en ciclos como estrategia de cruces
# 4.- Usar el generador de permutaciones como estrategia de generacion 
# 5.- Elegir entre seleccion por torneo, seleccion por ruleta o seleccion elitista como estrategia de seleccion
# 6.- Elegir la funcion de fitness adecuada entre berlinFitness1 y berlinFitness2 segun la estrategia de seleccion elegida
# 7.- Usar la funcion identidad como funcion decodifica (puede ser una funcion lambda)

# Los parametros de los algoritmos geneticos resultante son:
# 1.- Tamanyo de torneo (si procede). Valores interesantes: 1, 3, 5, 15, 20, 25, 30, 40, 53
# 2.- Proporcion de elite (si procede). Valores interesantes: 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
# 3.- Proporcion de cruce. Valores interesantes: 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
# 4.- Probabilidad de mutacion. Valores interesantes: 0.0, 0.01, 0.1, 0.2, 0.5, 0.8, 1.0
# 5.- Numero de generaciones. Valores interesantes: 100, 200, 500, 1000, 2000, 5000
# 6.- Tamanyo de la poblacion. Valores interesantes: 10, 50, 100, 500, 1000

# Nota: No todos los valores daran buenos resultados, pero son interesantes desde el punto 
# de vista de la comprension de los algoritmos geneticos.

# SE PIDE:

# Realizar al menos 5 ejecuciones del algoritmo genetico por cada instancia definida del problema (25 experimentos en total),
# variando los valores de los parametros del algoritmo en cada ejecucion,
# podeis tomar como referencia los valores interesantes que se mencinal (o elegir los valores que querais). 
# Para cada ejecucion se pide escribir lo siguiente (con comentarios en el propio codigo)

# 1.- Las estrategias del problema genetico (mutacion, cruce, seleccion)
# 2.- Decir que funcion de fitness se ha usado
# 3.- Los valores de los parametros utilizados en el algoritmo genetico 
# 4.- La deficinion de la variable problemaBerlin1
# 5.- La llamada al metodo ejecutaAlgoritmoGenetico.
# 6.- La salida del metodo ejecutaAlgoritmoGenetico.
# 7.- El tiempo de ejecucion y el valor de fitness de la mejor solucion obtenida
# 8.- Un parrafo CORTO de conclusiones sobre el resultado.


# SE VALORARA:
# a) La relevancia de las combinaciones de estrategias y parametros elegidos
# b) Buena organizacion y presentacion de los resultados, claridad y sintesis 
# c) Saber explicar que ocurre cuando se escogen valores extremos (probabilidad de mutacion 0 o 1 por ejemplo)
# d) Encontrar al menos una buena combinacion de estrategias y parametros que haga converger EN POCO TIEMPO al algoritmo al optimo global

# HAY UNA PLANTILLA PARA LA DOCUMENTACION AL FINAL DE ESTE DOCUMENTO

#==================================================================================
# EJEMPLO (incluyendo documentacion):

# EXPERIMENTO NUMERO 0
# --------------------

# ESTRATEGIAS:
# Las estrategias de este ejemplo son:
# 1.- Mutacion por intercambio
# 2.- Cruce basado en orden
# 3.- Seleccion por torneo

# FITNESS:
# He usado la funcion berlinFitness1 como fitness

# PARAMETROS:
# Los parametros de este ejemplo son:
# 1.- Tamanyo de torneo = 30
# 2.- Proporcion de cruce = 0.6
# 3.- Probabilidad de mutacion = 0.2
# 4.- Numero de generaciones = 1000
# 5.- Tamanyo de poblacion = 100
# 6.- Funcion "min" para obtener el mejor individuo

# DEFINICION DEL PROBLEMA:
# Esta es la definicion del problema:
problemaBerlin0 = ProblemaGenetico(berlin_genetico,
                                   MutacionPorIntercambio(),
                                   CruceBasadoEnOrden(),
                                   GeneradorPermutacion(),
                                   SeleccionTorneo(30,min),
                                   berlinFitness1,
                                   lambda x : x)

problemaBerlin1 = ProblemaGenetico(berlin_genetico,
                                   MutacionPorIntercambio(),
                                   CruceBasadoEnCiclos(),
                                   GeneradorPermutacion(),
                                   SeleccionTorneo(30,min),
                                   berlinFitness1,
                                   lambda x : x)

problemaBerlin2 = ProblemaGenetico(berlin_genetico,
                                   MutacionPorIntercambio(),
                                   CruceBasadoEnOrden(),
                                   GeneradorPermutacion(),
                                   SeleccionRuleta(),
                                   berlinFitness2,
                                   lambda x : x)

# LLAMADA AL ALGORITMO:  
# Esta es la llamada al algoritmo genetico:                                 
problemaBerlin0.ejecutaAlgoritmoGenetico(0.6,0.2,1000,100,min) 
problemaBerlin1.ejecutaAlgoritmoGenetico(0.6,0.2,1000,100,min) 
problemaBerlin2.ejecutaAlgoritmoGenetico(0.6,0.2,1000,100,max) 
# SALIDA DEL ALGORITMO:
# Esta es la salida del algoritmo genetico:
#[11.667443000000006,
# [7,
#  42,
#  6,
#  15,
#  50,
#  20,
#  14,
#  52,
#  47,
#  26,
#  32,
#  49,
#  37,
#  38,
#  12,
#  28,
#  10,
#  9,
#  4,
#  25,
#  40,
#  39,
#  51,
#  11,
#  3,
#  0,
#  24,
#  5,
#  29,
#  16,
#  48,
#  46,
#  18,
#  31,
#  21,
#  17,
#  22,
#  1,
#  41,
#  8,
#  23,
#  30,
#  44,
#  34,
#  27,
#  13,
#  35,
#  36,
#  45,
#  19,
#  33,
#  43,
#  2],
# 3282.4725918022136]

# TIEMPO Y FITNESS:
# Ha tardado 11.66 segundos y el fitness de la mejor solucion es 3282.47

# CONCLUSIONES: 
# ...
# ...
# ...

#=============================================================================
# PLANTILLA PARA DOCUMENTACION

# EXPERIMENTO NUMERO X
#---------------------

# ESTRATEGIAS:

# FITNESS:

# PARAMETROS:

# DEFINICION DEL PROBLEMA:

# LLAMADA AL ALGORITMO:  

# SALIDA DEL ALGORITMO:

# TIEMPO Y FITNESS:

# CONCLUSIONES: 
