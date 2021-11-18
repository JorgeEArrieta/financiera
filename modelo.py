from tkinter import messagebox
from datetime import date
from datetime import datetime
from re import compile
from sqlite3 import connect
from requests import get
from requests import ConnectionError
from bs4 import BeautifulSoup


#Clase para configurar datos comunes.
class ConfigApp():

    """
    Esta clase contiene los valores principales para permitir la parametrización
    de la aplicación.
    """

    #Valores consantes:
    
    MES = ['Enero','Febrero','Marzo','Abril',
           'Mayo','Junio','Julio','Agosto',
           'Septiembre','Noviembre', 'Diciembre']

    CUOTAS = [1, 3, 6, 12, 18, 24, 30]
        
    MONEDA = ['Peso', 'Dolar', 'Euro']

    TIP_INGRESO = ['Sueldo', 'Venta']

    TIP_GASTO = ['Servicios', 'Mantenimiento del Hogar', 'Alimentos', 'Automóvil',
                'Obra Social', 'Medicamentos', 'Transporte', 'Cuidado personal',
                'Mascotas', 'Entretenimiento', 'Gastos varios']


    #Constructor.
    def __init__(self):

        """
        Verifica que exista la tabla "parametros". De no existir, la crea.
        Asimismo, llama a la funcion "verifica_parametros" para chequear que existan los parametros básicos.
        """
    
        
        conector = connect('base.db')
        sql_cursor = conector.cursor()

        sql_cursor.execute("""CREATE TABLE IF NOT EXISTS "parametros" (
	                        "grupo"       INTEGER,
                            "tipo"	      TEXT(10)
                            );""")

        conector.commit()
        sql_cursor.close()
        conector.close()

        self.verifica_parametros()


    def verifica_parametros(self):
        
        """"
        Verifica que existan los parametros en la base de datos. 
        De no existir, los crea.
        """

        conector = connect('base.db')
        
        for i in self.TIP_INGRESO:
            sql_query = conector.cursor()
            sql_insert = conector.cursor()

            sql_query.execute("""SELECT tipo FROM parametros WHERE
                              grupo = 'Ingreso' and tipo = ?""",(i,))
            try:
                verifica_ingreso = sql_query.fetchone()[0]
            except TypeError:
                verifica_ingreso = None

            if verifica_ingreso == None:
                sql_insert.execute("""INSERT INTO parametros (grupo, tipo)
                                   VALUES ('Ingreso', ?)""",(i,)) 
                conector.commit()
            sql_query.close()
            sql_insert.close()

        for i in self.TIP_GASTO:
            
            sql_query = conector.cursor()
            sql_insert = conector.cursor()
            sql_query.execute("""SELECT tipo FROM parametros WHERE
                              grupo = 'Gastos' and tipo = ?""",(i,))
            
            try:
                verifica_gasto = sql_query.fetchone()[0]
            except TypeError:
                verifica_gasto = None

            if verifica_gasto == None:
                sql_insert.execute("""INSERT INTO parametros (grupo, tipo)
                                  VALUES ('Gastos', ?)""",(i,)) 
                conector.commit()
            sql_query.close()
            sql_insert.close()

        conector.close()


    
    def get_year(self):
        
        """
        Crea una lista con valores de tipo "año".
        Desde el 2000 hasta el año actual.
        """

        fecha = date.today()
        actual = fecha.year

        in_year = 2000
        end_year = actual
        
        years = []
    
        while in_year <= end_year:
            years.append(in_year)
            in_year = in_year + 1
        
        y = list(reversed(years))
        
        return y


    
    def show_par(self, grupo):
        
        """
        Obtiene los parametros de la tabla de mismo nombre.
        """

        resultado = []
        
        conector = connect('base.db')
        sql_query_1 = conector.cursor()

        sql_query_1.execute('SELECT tipo FROM parametros where grupo = ?',(grupo,))
    
        r = sql_query_1.fetchall()
        
        for x in range(0,len(r)):
            y = r[x]
            resultado.append(y[0])
            
        sql_query_1.close()
        conector.close()
    
        return resultado

    def crea_parametro(self, ventana, tipo, nombre):

        """
        Crea parametros de tipo "ingreso / gasto" para la tabla parametros.
        """

        conector = connect('base.db')

        sql_query = conector.cursor()
        sql_query.execute("""SELECT tipo FROM parametros WHERE
                          grupo = ? AND tipo = ?""",(tipo, nombre,))
    
        try:
            exist = sql_query.fetchone()[0]
        except TypeError:
            exist = None

        sql_query.close()

        try:
            if tipo == '':
                raise FaltaParametro

            if exist == None:

                formato = compile(r'[^a-zA-Z áéíóúÁÉÍÓÚ]')
                
                if formato.search(nombre) != None:
                    raise CaracterInvalido
                
                sql_insert = conector.cursor()
                sql_insert.execute("""INSERT INTO parametros (grupo, tipo)
                           VALUES (?, ?)""",(tipo, nombre,))
                
                conector.commit()
                sql_insert.close()
                conector.close()

                ventana.destroy()

                messagebox.showinfo(title='Información', message='Se creo el registro correctamente.')

            else:
                raise ExisteRegistro

        except ExisteRegistro:
            messagebox.showerror(title='Error', message='Ya existe el registro en la base de datos')
        
        except FaltaParametro:
            messagebox.showerror(title='Error', message='Falta definir el tipo del parametro.')

        except CaracterInvalido: 
            messagebox.showerror(title='Error', message='El campo nombre contiene caracteres invalidos.')


class CondFinanciera():

    """
    La clase CondFinanciera maneja el acceso a la base de datos.
    Asimismo, verifica la lógica de creación de cada uno de los registros.
    """

    dolarblue_venta = None
    dolarblue_compra = None
    euroblue_venta = None
    euroblue_compra = None
    total_ahorro = None
    total_ingreso = None 
    gasto_mensual = None
    
    def __init__(self):

        """
        Verifica que existan las tablas: contabilidad, tarjeta_credito, prestamo,
        ahorro y divisas. De ser necesario, las crea.
        Asimismo, llama a la funcion "ahorro_vencido", para verificar el estado de los ahorros.
        Como tambien, a la función estadisticas, para obtener valores generales. 
        """
        
        self.gastos = 0
        self.dinero_disp = 0
        self.ahorros = 0
        
        conector = connect('base.db')
        sql_cursor_1 = conector.cursor()
        sql_cursor_2 = conector.cursor()
        sql_cursor_3 = conector.cursor()
        sql_cursor_4 = conector.cursor()
        sql_cursor_5 = conector.cursor()

        sql_cursor_1.execute("""CREATE TABLE IF NOT EXISTS "contabilidad" (
                            "tipo"        TEXT(10),
                            "id"          INTEGER,
	                        "tip_cont" 	  TEXT(10),
                            "id_prest"    INTEGER,
                            "descrip"     TEXT(25),
                            "fecha"	      TIMESTAMP,
                            "importe"	  INTEGER
                            );""")

        sql_cursor_2.execute("""CREATE TABLE IF NOT EXISTS "tarjeta_credito" (
                            "id_tc"     INTEGER,
	                        "fecha"	    TIMESTAMP,
                            "tip_cont" 	TEXT(10),
	                        "descrip"	TEXT(25),
                            "cuota"     INTEGER,
                            "imp_cuota" INTEGER,
	                        "imp_tot"	INTEGER
                            );""")

        sql_cursor_3.execute("""CREATE TABLE IF NOT EXISTS "prestamo" (
                            "id"        INTEGER,
                            "fecha"	    TIMESTAMP,
                            "descrip"	TEXT,
                            "cuota"     INTEGER,
                            "imp_cuota" INTEGER,
                            "imp_tot"	INTEGER,
                            "imp_dev"   INTEGER
                            );""")

        sql_cursor_4.execute("""CREATE TABLE IF NOT EXISTS "ahorro" (
                            "id"        INTEGER,
                            "fec_venc"  TIMESTAMP,
                            "moneda"	TEXT,
                            "imp"       INTEGER,
                            "tasa"      INTEGER,
                            "imp_final"	INTEGER
                            );""")
        
        sql_cursor_5.execute("""CREATE TABLE IF NOT EXISTS "divisas" (
                                "tipo"        TEXT(25),
                                "importe"     INTEGER(10)
                                );""")
          
        conector.commit()
        sql_cursor_1.close()
        sql_cursor_2.close()
        sql_cursor_3.close()
        sql_cursor_4.close()
        sql_cursor_5.close()
        conector.close()

        self.estadisticas()
        self.ahorro_vencido()
        
        self.dolarblue_venta = self.obtiene_valor_divisa('dbventa')
        self.dolarblue_compra = self.obtiene_valor_divisa('dbcompra')
        self.euroblue_venta = self.obtiene_valor_divisa('ebventa')
        self.euroblue_compra = self.obtiene_valor_divisa('ebcompra')


    def valor_divisas_web(self):

        """
        Obtiene el valor de las divisas extranjeras desde la pagina de perfil.com
        """
        
        try:
            url = 'https://www.perfil.com/'

            pagina = get(url)

            sopa = BeautifulSoup(pagina.content, 'html.parser')

            valores = list()

            dolarblue_venta = sopa.find('div', class_='dbventa')
            dolarblue_compra = sopa.find('div', class_='dbcompra')
            euroblue_venta = sopa.find('div', class_='ebventa')
            euroblue_compra = sopa.find('div', class_='ebcompra')

            valores.append(float(dolarblue_venta.string))
            valores.append(float(dolarblue_compra.string))
            valores.append(float(euroblue_venta.string))
            valores.append(float(euroblue_compra.string))

            self.dolarblue_venta = valores[0]
            self.dolarblue_compra = valores[1]
            self.euroblue_venta = valores[2]
            self.euroblue_compra = valores[3]

            conector = connect ('base.db')

            #Busca el valor para dolar blue - venta
            sql_cursor_0 = conector.cursor()
            sql_cursor_0.execute("""SELECT tipo FROM divisas where tipo = 'dbventa'""")
           
            try:
                resultado = sql_cursor_0.fetchone()[0]
            except TypeError:
                resultado = None

            if resultado == None:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""INSERT INTO divisas (tipo, importe)
                                        VALUES ('dbventa', ?)""",(self.dolarblue_venta,))
                conector.commit()
                sql_cursor.close()
            else:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""UPDATE divisas SET importe = ? 
                                        WHERE tipo = 'dbventa'""",(self.dolarblue_venta,))    
                conector.commit()
                sql_cursor.close()
            
            sql_cursor_0.close()
            
            #Busca el valor para dolar blue - compra
            sql_cursor_0 = conector.cursor()
            sql_cursor_0.execute("""SELECT tipo FROM divisas where tipo = 'dbcompra'""")
            try:
                resultado = sql_cursor_0.fetchone()[0]
            except TypeError:
                resultado = None
       
            if resultado == None:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""INSERT INTO divisas (tipo, importe)
                                   VALUES ('dbcompra', ?)""",(self.dolarblue_compra,))
                conector.commit()
                sql_cursor.close()
            else:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""UPDATE divisas SET importe = ? 
                                  WHERE tipo = 'dbcompra'""",(self.dolarblue_compra,))    
                conector.commit()
                sql_cursor.close()

            sql_cursor_0.close()

            #Busca el valor para euro blue - venta
            sql_cursor_0 = conector.cursor()
            sql_cursor_0.execute("""SELECT tipo FROM divisas where tipo = 'ebventa'""")
            
            try:
                resultado = sql_cursor_0.fetchone()[0]
            except TypeError:
                resultado = None

            if resultado == None:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""INSERT INTO divisas (tipo, importe)
                                VALUES ('ebventa', ?)""",(self.euroblue_venta,))
                conector.commit()
                sql_cursor.close()
            else:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""UPDATE divisas SET importe = ? 
                                WHERE tipo = 'ebventa'""",(self.euroblue_venta,)) 
                conector.commit()
                sql_cursor.close()

            sql_cursor_0.close()

            #Busca el valor para euro blue - compra
            sql_cursor_0 = conector.cursor()
            sql_cursor_0.execute("""SELECT tipo FROM divisas where tipo = 'ebcompra'""")
            
            try:
                resultado = sql_cursor_0.fetchone()[0]
            except TypeError:
                resultado = None

            if resultado == None:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""INSERT INTO divisas (tipo, importe)
                                VALUES ('ebcompra', ?)""",(self.euroblue_compra,))
                conector.commit()
                sql_cursor.close()
            else:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""UPDATE divisas SET importe = ? 
                                WHERE tipo = 'ebcompra'""",(self.euroblue_compra,)) 
                conector.commit()
                sql_cursor.close()
            
            sql_cursor_0.close()
            conector.close()
            
        except ConnectionError:
            messagebox.showerror(title='Error', message='No hay conexión a internet.')
    

    def valor_divisas_manual(self, importe, tipo):
        
        """
        Le permite al usuario ingresar, de forma manual, el valor de las divisas.
        """
     
        importe = float(importe)

        conector = connect ('base.db')

        sql_cursor_0 = conector.cursor()
        sql_cursor_0.execute("""SELECT tipo FROM divisas where tipo = ?""", (tipo,))
        
        try:
            resultado = sql_cursor_0.fetchone()[0]

            if resultado == None:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""INSERT INTO divisas (tipo, importe)
                            VALUES (?, ?)""",(importe, tipo,))
                conector.commit()
                sql_cursor.close()
            else:
                sql_cursor = conector.cursor()
                sql_cursor.execute("""UPDATE divisas SET importe = ? 
                                WHERE tipo = ?""",(importe, tipo,))    
                conector.commit()
                sql_cursor.close()
        except TypeError:
            pass
            

    def obtiene_valor_divisa(cls, tipo):
        
        """
        Obtiene el valor de la divisa desde la base de datos.
        """
        try:
            conector = connect('base.db')
            sql_cursor = conector.cursor()

            sql_cursor.execute("""SELECT importe FROM divisas WHERE tipo = ?""",(tipo,))
            resultado = sql_cursor.fetchone()[0]

        except:
            resultado = None

        return resultado
        

    def estadisticas(self):
        
        """
        Brinda estadisticas de cuanto es el dinero disponible, el total de gastos 
        y el monto de los ahorros.
        """

        total_ahorro = 0
        total_ingreso = 0
        gasto_mensual = 0


        #Obtengo fechas.
        fecha = date.today()
        an_actual = fecha.year
        mes_actual = fecha.month
        
        try:
            
            if mes_actual < 10:
                fec_fin = f'{an_actual}-0{mes_actual}-31'
            elif mes_actual > 9:
                fec_fin = f'{an_actual}-{mes_actual}-31'
            
            fec_inicio = f'{an_actual}-01-01'
        
            conexion = connect('base.db')
            sql_cursor_0 = conexion.cursor()
    
            sql_cursor_0.execute("""SELECT SUM(importe) FROM contabilidad
                                WHERE fecha BETWEEN ? AND ?
                                AND tipo = 'Gasto';""",(fec_inicio, fec_fin,))

            gasto_mensual = sql_cursor_0.fetchone()[0]

            gasto_mensual = round(gasto_mensual,2)

            sql_cursor_0.close()

        except:
            pass

        try:
            fec_inicio = f'{an_actual}-01-01'
            fec_fin = f'{an_actual}-12-31'
        
            sql_cursor_1 = conexion.cursor()


            sql_cursor_1.execute("""SELECT SUM(importe) FROM contabilidad
                                    WHERE fecha BETWEEN ? AND ?
                                    AND tipo = 'Ingreso';""",(fec_inicio, fec_fin,))
        
            total_ingreso = sql_cursor_1.fetchone()[0]

            total_ingreso = round(total_ingreso,2)

            sql_cursor_1.close()

        except:
            pass

        try:
            sql_cursor_pesos = conexion.cursor()
            sql_cursor_pesos.execute("""SELECT SUM(imp_final) FROM ahorro
                                        WHERE moneda = 'Peso';""")
            pesos = sql_cursor_pesos.fetchone()[0]
            total_ahorro = total_ahorro + pesos
        except:
            pass
        
        try:
            sql_cursor_dolar = conexion.cursor()
            sql_cursor_dolar.execute("""SELECT SUM(imp_final) FROM ahorro
                                        WHERE moneda = 'Dolar';""")
            dolar = sql_cursor_dolar.fetchone()[0]
            total_ahorro = total_ahorro + dolar * self.dolarblue_compra
        except:
            pass

        try:
            sql_cursor_euro = conexion.cursor()
            sql_cursor_euro.execute("""SELECT SUM(imp_final) FROM ahorro
                                        WHERE moneda = 'Euro';""")
            euro = sql_cursor_euro.fetchone()[0]
            total_ahorro = total_ahorro + euro * self.euroblue_compra
        except:
            pass
  
        if total_ahorro == None:
            total_ahorro = 0
        if total_ingreso == None:
            total_ingreso = 0
        if gasto_mensual == None:
            gasto_mensual = 0

        conexion.close()

        self.gastos = gasto_mensual
        self.dinero_disp = total_ingreso - gasto_mensual
        self.ahorros = total_ahorro

    
    def crear_id (cls, base):
        
        """
        Función para obtener los id para la creación de nuevos registros (contabilidad).
        """
        
        conector = connect('base.db')
        sql_query = conector.cursor()
        
        if base == 'contabilidad':
            sql_query.execute('select max(id) from contabilidad')
        elif base == 'tarjeta_credito':
            sql_query.execute('select max(id_tc) from tarjeta_credito')
        elif base == 'prestamo':
            sql_query.execute('select max(id) from prestamo')
        elif base == 'ahorro':
            sql_query.execute('select max(id) from ahorro')
        
        resultado = sql_query.fetchone()

        if resultado[0] == None:
            valor = 0
        else:
            valor = resultado[0] + 1 
        
        sql_query.close()
        conector.close() 

        return valor


    def valida_fecha(cls, value):
        
        """
        Valida el campo fecha de los formularios. 
        """
        try:
            datetime.strptime(value,'%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            raise FechaInvalida


    def valida_nombre(cls, value):
        
        """
        Valida el campo nombre de los formularios.
        """
        formato = compile(r'[^a-zA-Z áéíóúÁÉÍÓÚ]')
        
        if formato.search(value) != None:
            raise CaracterInvalido

    
    def conta_fecha(cls, fecha, cant_cuotas):
            
        """
        Crea las fechas para las cuotas. Utilizado para la generación de registros
        de tipo "tarjeta de credito."
        """
        list_fecha = []

        mes = int(fecha[5:7])

        year = int(fecha[:4])

        inc = 1
    
        while inc <= cant_cuotas:
        
            day = 1
        
            fecha = datetime(year, mes, day).strftime('%Y-%m-%d')
        
            list_fecha.append(fecha)
        
            if int(mes) < 12:
                mes = mes + 1
            else:
                year = year + 1
                mes = 1  

            inc = inc + 1
           
        return list_fecha
    

    def vis_tv_prestamo(cls, tree):

        """
        Visualiza en un widget, de tkinter, la información de la tabla "prestamo".
        """
        
        conector = connect('base.db')
        sql_cursor_0 = conector.cursor()
        
        sql_cursor_0.execute('SELECT MAX(id) FROM prestamo;')
        try:
            id_max = sql_cursor_0.fetchone()[0]
        except TypeError:
            id_max = None
        id = 0
        
        if id_max != None:
        
            while id <= id_max:
            
                try:
                    sql_cursor_1 = conector.cursor()
                    sql_cursor_2 = conector.cursor()
                    sql_cursor_3 = conector.cursor()
                    sql_cursor_1.execute("""SELECT fecha FROM prestamo
                                            WHERE id = ?""", (id,))
                    sql_cursor_2.execute("""SELECT descrip FROM prestamo
                                            WHERE id = ?""", (id,))
                    sql_cursor_3.execute("""SELECT imp_tot FROM prestamo
                                            WHERE id = ?""", (id,))
                    
                    fecha = sql_cursor_1.fetchone()[0]
                    descripcion = sql_cursor_2.fetchone()[0]
                    importe = sql_cursor_3.fetchone()[0]
                    
                    tree.insert(parent='',
                                index='end',
                                iid = id,
                                values=(fecha, descripcion, importe)
                                )
                    
                    sql_cursor_1.close()
                    sql_cursor_2.close()
                    sql_cursor_3.close()
                    
                    id = id + 1
                except:
                    id = id + 1        
        
        sql_cursor_0.close()
        conector.close()
    
    
    def vis_tv_tarjeta(cls, tree):

        """
        Visualiza en un widget, de tkinter, la información de la tabla "tarjeta_credito".
        """
        
        conector = connect('base.db')
        sql_cursor_0 = conector.cursor()
        
        sql_cursor_0.execute('SELECT MAX(id_tc) FROM tarjeta_credito;')

        try:
            id_max = sql_cursor_0.fetchone()[0]
        except TypeError:
            id_max = None

        id = 0
        
        if id_max != None:
        
            while id <= id_max:
            
                try:
                    sql_cursor_1 = conector.cursor()
                    sql_cursor_2 = conector.cursor()
                    sql_cursor_3 = conector.cursor()

                    sql_cursor_1.execute("""SELECT fecha FROM tarjeta_credito
                                            WHERE id_tc = ?""", (id,))
                    sql_cursor_2.execute("""SELECT descrip FROM tarjeta_credito
                                            WHERE id_tc = ?""", (id,))
                    sql_cursor_3.execute("""SELECT imp_tot FROM tarjeta_credito
                                            WHERE id_tc = ?""", (id,))
                    
                    fecha = sql_cursor_1.fetchone()[0]
                    descripcion = sql_cursor_2.fetchone()[0]
                    importe = sql_cursor_3.fetchone()[0]
                    
                    tree.insert(parent='',
                                index='end',
                                iid = id,
                                values=(fecha, descripcion, importe)
                                )
                     
                    sql_cursor_1.close()
                    sql_cursor_2.close()
                    sql_cursor_3.close()
                    
                    id = id + 1

                except:   
                    id = id + 1
                
        sql_cursor_0.close()
        conector.close()
    

    def vis_tv_ahorro(cls, tree):
        
        """
        Visualiza en un widget, de tkinter, la información de la tabla "ahorro".
        """

        conector = connect('base.db')
        sql_cursor_0 = conector.cursor()
        
        sql_cursor_0.execute('SELECT MAX(id) FROM ahorro;')
        
        try:
            id_max = sql_cursor_0.fetchone()[0]
        except TypeError:
            id_max = None
        
        id = 0

        if id_max != None:
        
            while id <= id_max:
            
                try:
                    sql_cursor_1 = conector.cursor()
                    sql_cursor_2 = conector.cursor()
                    sql_cursor_3 = conector.cursor()
                    sql_cursor_4 = conector.cursor()
                    sql_cursor_5 = conector.cursor()

                    sql_cursor_1.execute("""SELECT fec_venc FROM ahorro
                                            WHERE id = ?""", (id,))
                    sql_cursor_2.execute("""SELECT moneda FROM ahorro
                                            WHERE id = ?""", (id,))
                    sql_cursor_3.execute("""SELECT imp FROM ahorro
                                            WHERE id = ?""", (id,))
                    sql_cursor_4.execute("""SELECT tasa FROM ahorro
                                            WHERE id = ?""", (id,))
                    sql_cursor_5.execute("""SELECT imp_final FROM ahorro
                                            WHERE id = ?""", (id,))
                    
                    fec_ven = sql_cursor_1.fetchone()[0]
                    moneda = sql_cursor_2.fetchone()[0]
                    imp = sql_cursor_3.fetchone()[0]
                    tasa = sql_cursor_4.fetchone()[0]
                    imp_final = sql_cursor_5.fetchone()[0]

                    
                    tree.insert(parent='',
                                index='end',
                                iid = id,
                                values=(fec_ven, moneda, imp, tasa, imp_final)
                                )
                    
                    sql_cursor_1.close()
                    sql_cursor_2.close()
                    sql_cursor_3.close()
                    sql_cursor_4.close()
                    sql_cursor_5.close()

                    id = id + 1
                except:
                    
                    id = id + 1
                
        sql_cursor_0.close()
        conector.close()

    
    def visualizar_treeview(cls, tree, tipo):
        
        """
        Visualiza en un widget, de tkinter, la información de la tabla "contabilidad".
        Esta función muestra la totalidad de los datos, ordenandolos por fecha. 
        """

        conector = connect('base.db')
        sql_cursor = conector.cursor()
        query_1 = conector.cursor()
        query_2 = conector.cursor()
        query_3 = conector.cursor()

        #Cuenta cantidad de registros

        sql_cursor.execute("""SELECT id FROM contabilidad WHERE tipo = ?
                           ORDER BY fecha""",(tipo,))

        try:
            ids = sql_cursor.fetchall()
        except TypeError:   
            ids = None

        if ids != None:

            lista = []
            
            for i in range(0, len(ids)):
                n = ids[i]
                lista.append(n[0])
            
            sql_cursor.close()

            for x in lista:

                try:

                    id = x
                    fecha = None
                    tip_ingreso = None
                    importe = None

                    query_1.execute("""SELECT fecha FROM contabilidad
                                    WHERE id = ? and tipo = ?""", (id, tipo,))
                    query_2.execute("""SELECT tip_cont FROM contabilidad
                                    WHERE id = ? and tipo = ?""", (id, tipo,))
                    query_3.execute("""SELECT importe FROM contabilidad
                                    WHERE id = ? and tipo = ?""", (id, tipo,))
                    
                    fecha = query_1.fetchone()[0]
                    tip_ingreso = query_2.fetchone()[0]
                    importe = query_3.fetchone()[0]

                    tree.insert(parent='',
                    index='end',
                    iid = id,
                    values=(fecha,tip_ingreso,importe))
                
                except:
                    pass
        
        sql_cursor.close()
        query_1.close()
        query_2.close()
        query_3.close()
        conector.close()


    def treeview_mensual(self, tree, tipo, mes, year):

            """
            Visualiza en un widget, de tkinter, la información de la tabla "contabilidad".
            Esta función filtra los datos por mes y año, ordenandolos por fecha. 
            """

            try:
                year = int(year)
            except ValueError:
                messagebox.showerror(title='Error',
                                     message='Formato de año invalido')
            
            conector = connect('base.db')
            sql_cursor = conector.cursor()
            query_0 = conector.cursor()
            query_1 = conector.cursor()
            query_2 = conector.cursor()
            query_3 = conector.cursor()

            #Cuenta cantidad de registros

            sql_cursor.execute("""SELECT id FROM contabilidad WHERE tipo = ?
                                ORDER BY fecha""",(tipo,))
            
            try:
                ids = sql_cursor.fetchall()
            except TypeError:   
                ids = None

            if mes == 1:
                fecinc = f'{year}-01-01'
                fecfin = f'{year}-01-31'
            elif mes == 2:
                fecinc = f'{year}-02-01'
                fecfin = f'{year}-02-29'
            elif mes == 3:
                fecinc = f'{year}-03-01'
                fecfin = f'{year}-03-31'
            elif mes == 4:
                fecinc = f'{year}-04-01'
                fecfin = f'{year}-04-30'
            elif mes == 5:
                fecinc = f'{year}-05-01'
                fecfin = f'{year}-05-31'
            elif mes == 6:
                fecinc = f'{year}-06-01'
                fecfin = f'{year}-06-30'
            elif mes == 7:
                fecinc = f'{year}-07-01'
                fecfin = f'{year}-07-31'
            elif mes == 8:
                fecinc = f'{year}-08-01'
                fecfin = f'{year}-08-31'
            elif mes == 9:
                fecinc = f'{year}-09-01'
                fecfin = f'{year}-09-31'
            elif mes == 10:
                fecinc = f'{year}-10-01'
                fecfin = f'{year}-10-31'
            elif mes == 11:
                fecinc = f'{year}-11-01'
                fecfin = f'{year}-11-30'
            elif mes == 12:
                fecinc = f'{year}-12-01'
                fecfin = f'{year}-12-31'

            if ids != None:

                largo = len(ids)
                
                lista = []
    
                for i in range(0, largo):
                    n = ids[i]
                    lista.append(n[0])
                sql_cursor.close()
                
                for x in lista:

                    try:

                        id = x
                    
                        fecha = None
                        tip_ingreso = None
                        importe = None

                        query_0.execute("""SELECT id FROM contabilidad
                                        WHERE id = ? 
                                        AND tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecinc, fecfin))
                        query_1.execute("""SELECT fecha FROM contabilidad
                                        WHERE id = ? 
                                        and tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecinc, fecfin))
                        query_2.execute("""SELECT tip_cont FROM contabilidad
                                        WHERE id = ? 
                                        AND tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecinc, fecfin))
                        query_3.execute("""SELECT importe FROM contabilidad
                                        WHERE id = ? 
                                        AND tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecinc, fecfin))
                    
                        identificador = query_0.fetchone()[0]
                        fecha = query_1.fetchone()[0]
                        tip_ingreso = query_2.fetchone()[0]
                        importe = query_3.fetchone()[0]
                    
                        tree.insert(parent='',
                                    index='end',
                                    iid = identificador,
                                    values=(fecha,tip_ingreso,importe))
            
                    except:           
                        pass

                sql_cursor.close()
                conector.close()


    
    def treeview_year(self, tree, tipo, year):
        
        """
        Visualiza en un widget, de tkinter, la información de la tabla "contabilidad".
        Esta función filtra los datos por año, ordenandolos por fecha. 
        """

        try:
            year = int(year)
        except ValueError:
            messagebox.showerror(title='Error',
                                 message='Formato de año invalido')

        conector = connect('base.db')
        sql_cursor = conector.cursor()
        query_0 = conector.cursor()
        query_1 = conector.cursor()
        query_2 = conector.cursor()
        query_3 = conector.cursor()

        #Cuenta cantidad de registros

        sql_cursor.execute("""SELECT id FROM contabilidad WHERE tipo = ?
                           ORDER BY fecha""",(tipo,))
        try:
            ids = sql_cursor.fetchall()
        except TypeError:
            ids = None

        fecin = f'{year}-01-01'
        fecfin = f'{year}-12-31'

        if ids != None:

            largo = len(ids)
            lista = []
    
            for i in range(0, largo):
                n = ids[i]
                lista.append(n[0])
    
            sql_cursor.close()

            for x in lista:

                try:

                    id = x
                
                    fecha = None
                    tip_ingreso = None
                    importe = None

                    query_0.execute("""SELECT id FROM contabilidad
                                        WHERE id = ? 
                                        AND tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecin, fecfin))
                    query_1.execute("""SELECT fecha FROM contabilidad
                                        WHERE id = ? 
                                        and tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecin, fecfin))
                    query_2.execute("""SELECT tip_cont FROM contabilidad
                                        WHERE id = ? 
                                        AND tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecin, fecfin))
                    query_3.execute("""SELECT importe FROM contabilidad
                                        WHERE id = ? 
                                        AND tipo = ?
                                        AND fecha between ? AND ?""", (id, tipo, fecin, fecfin))
                
                    identificador = query_0.fetchone()[0]
                    fecha = query_1.fetchone()[0]
                    tip_ingreso = query_2.fetchone()[0]
                    importe = query_3.fetchone()[0]
                
                    tree.insert(parent='',
                                index='end',
                                iid = identificador,
                                values=(fecha,tip_ingreso,importe))  
                except:
                    pass
            

        query_0.close()
        query_1.close()
        query_2.close()
        query_3.close()
        conector.close()


    def crear_registro(self, ventana, tipo, tip_cont, desc, fecha, importe):
        
        """
        Crea registros de tipo gasto/ingreso en la tabla contabilidad.
        """
        try:
            self.valida_nombre(tip_cont)
            self.valida_fecha(fecha)
            float(importe)

            id = self.crear_id('contabilidad')

            conector = connect('base.db')
            sql_cursor = conector.cursor()

            sql_cursor.execute("""INSERT INTO contabilidad 
                                (id, tipo, tip_cont, id_prest, descrip, fecha, importe)
                                VALUES (?,?,?,?,?,?,?);""",
                                (id, tipo, tip_cont, '', desc, fecha, importe,))

            conector.commit()
            sql_cursor.close() 
            conector.close()

            if ventana != None:
                ventana.destroy()
                messagebox.showinfo(title='Información', message='Se creo el registro correctamente.')

        except ValueError:
            messagebox.showerror(title='Advertencia', message='Se ingreso un importe con un formato erroneo.')

        except FechaInvalida:
            messagebox.showerror(title='Advertencia', message='Se ingreso una fecha con un formato erroneo (yyyy/mm/dd).')

        except CaracterInvalido:
            messagebox.showerror(title='Advertencia', message='El campo titulo contiene caracteres invalidos.')
    

    def act_registro(self, ventana, id, tip_cont, desc, fecha, importe):
        
        """
        Actualiza los registros de tipo gasto/ingreso, de la tabla contabilidad.
        """

        conector = connect('base.db')
        
        try:
            #Verifica errores.
            self.valida_nombre(tip_cont)
            self.valida_fecha(fecha)
            float(importe)

            sql_cursor_0 = conector.cursor()
        
            sql_cursor_0.execute("""SELECT tip_cont FROM contabilidad 
                                    WHERE id = ?""", (id,))
        
            resultado = sql_cursor_0.fetchone()[0]
            
            sql_cursor_0.close()
            
            if resultado == 'Tarjeta de credito': 
                raise TypeError
            elif resultado == 'Prestamo':
                raise TypeError
            elif resultado == 'Ahorro':
                raise TypeError
             
            #Proceso de actualización.
            sql_cursor_1 = conector.cursor()

            sql_cursor_1.execute("""UPDATE contabilidad SET 
                                  tip_cont = ?,
                                  descrip = ?,
                                  fecha = ?,
                                  importe = ?
                                  WHERE id = ?;""", (tip_cont, desc, fecha, importe, id,))

            conector.commit()
            sql_cursor_1.close() 
            
            ventana.destroy()

            messagebox.showinfo(title='Error', message='Se actualizo el registro correctamente.')

        except ValueError:
            messagebox.showerror(title='Error', message='Se ingreso un importe con un formato erroneo.')

        except FechaInvalida:
            messagebox.showerror(title='Error', message='Se ingreso una fecha con un formato erroneo.')

        except CaracterInvalido:
            messagebox.showerror(title='Error', message='El campo titulo contiene caracteres invalidos.')

        except TypeError:
            messagebox.showerror(title='Error', message='No se puede actualizar este tipo de registro.')
            ventana.destroy()
    
        finally:
            conector.close()


    def eliminar_registro (self, id):

        """
        Elimina los registros, de tipo gasto/ingreso, de la tabla contabilidad.
        """

        try:

            if id == '':
                raise NoExisteRegistro

            mensaje_1 = messagebox.askyesnocancel(title='Advertencia',
                                                message='Este procedimiento borrara el registro. ¿Quiere continuar?')
            
            conector = connect('base.db')
            sql_cursor_0 = conector.cursor()

            sql_cursor_0.execute("""SELECT tip_cont FROM contabilidad 
                                    WHERE id = ?""", (id,))

            resultado = sql_cursor_0.fetchone()[0]

            if resultado == 'Tarjeta de credito': 
                raise TypeError
            elif resultado == 'Prestamo':
                raise TypeError
            
            if mensaje_1 == True:

                conector = connect('base.db')
                sql_cursor = conector.cursor()

                sql_cursor.execute('DELETE FROM contabilidad WHERE id = ?;',(id,))

                conector.commit()
                sql_cursor.close()
                conector.close()

                messagebox.showinfo(title='Información', message='Se elimino el registro correctamente.')

        except NoExisteRegistro:
            messagebox.showwarning(title='Error', message='Debe seleccionar un registro primero.')
        except TypeError:
            messagebox.showwarning(title='Error', message='No se puede eliminar el tipo de registro seleccionado.')
    
    
    def visualizar_registro_tc(self, id, campo):

        """
        #Funcion para visualizar los datos de un tipo de registro (tarjeta de crédito).
        """

        conector = connect('base.db')
        sql_query = conector.cursor()
    
        if campo == 'fecha':
            sql_query.execute("""SELECT fecha FROM tarjeta_credito WHERE id_tc = ?""", (id,))
        elif campo == 'tip_cont':
            sql_query.execute("""SELECT tip_cont FROM tarjeta_credito WHERE id_tc = ?""", (id,))
        elif campo == 'descrip':
            sql_query.execute("""SELECT descrip FROM tarjeta_credito WHERE id_tc = ?""", (id,))
        elif campo == 'cuota':
            sql_query.execute("""SELECT max(cuota) FROM tarjeta_credito WHERE id_tc = ?""", (id,))
        elif campo == 'imp_cuota':
            sql_query.execute("""SELECT imp_cuota FROM tarjeta_credito WHERE id_tc = ?""", (id,))
        elif campo == 'imp_tot':
            sql_query.execute("""SELECT imp_tot FROM tarjeta_credito WHERE id_tc = ?""", (id,))
        
        resultado = sql_query.fetchone()[0]
        sql_query.close()
        conector.close()
        
        return resultado
    

    def vis_registro_prestamo(self, id, campo):
        
        """
        Funcion para visualizar los datos de un tipo de registro (prestamo).
        """
        conector = connect('base.db')
        sql_query = conector.cursor()

        if campo == 'fecha':
            sql_query.execute("""SELECT fecha FROM prestamo WHERE id = ?""", (id,))
        elif campo == 'descrip':
            sql_query.execute("""SELECT descrip FROM prestamo WHERE id = ?""", (id,))
        elif campo == 'cuota':
            sql_query.execute("""SELECT cuota FROM prestamo WHERE id = ?""", (id,))
        elif campo == 'imp_cuota':
            sql_query.execute("""SELECT imp_cuota FROM prestamo WHERE id = ?""", (id,))
        elif campo == 'imp_tot':
            sql_query.execute("""SELECT imp_tot FROM prestamo WHERE id = ?""", (id,))
        elif campo == 'imp_dev':
            sql_query.execute("""SELECT imp_dev FROM prestamo WHERE id = ?""", (id,))

    
        resultado = sql_query.fetchone()[0]
        sql_query.close()
        conector.close()
    
        return resultado
    
    
    def visualizar_registro(self, id, campo):

        """
        Funcion para visualizar los datos de un tipo de registro (contabilidad).
        """

        conector = connect('base.db')
        sql_query = conector.cursor()
        
        if campo == 'tip_cont':
            sql_query.execute("""SELECT tip_cont FROM contabilidad WHERE id = ?""", (id,))
        elif campo == 'descrip':
            sql_query.execute("""SELECT descrip FROM contabilidad WHERE id = ?""", (id,))
        elif campo == 'fecha':
            sql_query.execute("""SELECT fecha FROM contabilidad WHERE id = ?""", (id,))
        elif campo == 'importe':
            sql_query.execute("""SELECT importe FROM contabilidad WHERE id = ?""", (id,))
            
        resultado = sql_query.fetchone()[0]

        sql_query.close()
        conector.close()

        return resultado
    

    def tc_contabilidad(self):
        
        """
        Actualiza los registros tipo "tarjeta de crédito", de la tabla contabilidad.
        Si no existen registros en la tabla tarjeta de crédito, elimina los 
        existentes en la tabla contabilidad. 
        """
        fechas = []

        conector = connect('base.db')
        sql_cursor_0 = conector.cursor()
        
        #Crea una lista de fechas
        sql_cursor_0.execute("""SELECT fecha FROM tarjeta_credito
                                ORDER BY fecha;""")
        r = sql_cursor_0.fetchall()
        
        for i in range(len(r)):
            y = r[i]
            fechas.append(y[0])

        if len(fechas) == 0:
            
            ids = []
            
            sql_cursor_1 = conector.cursor()
            sql_cursor_1.execute("""SELECT id FROM contabilidad
                                    WHERE tip_cont = 'Tarjeta de credito'""")
            
            identificador = sql_cursor_1.fetchall()

            sql_cursor_1.close()

            for x in range(len(identificador)):
                n = identificador[x]
                ids.append(n[0])
            
            for l in ids:

                sql_cursor_2 = conector.cursor()
                sql_cursor_2.execute("""DELETE FROM contabilidad 
                                        WHERE id = ?""",(l,))
                conector.commit()
                sql_cursor_2.close()

        #Por cada fecha en la lista, se fija si existe un registro. 
        #De existir, lo actualiza. Caso contrario, lo crea.
        for f in fechas:

            sql_cursor_1 = conector.cursor()
            sql_cursor_2 = conector.cursor()
            sql_cursor_3 = conector.cursor()

            sql_cursor_1.execute("""select id FROM contabilidad WHERE 
                                    fecha = ? and 
                                    tip_cont = 'Tarjeta de credito';""", (f,))
            
            try:
                resultado = sql_cursor_1.fetchone()[0]
            except TypeError:
                resultado = None

            if resultado == None:

                id = self.crear_id('contabilidad')
                
                sql_cursor_2.execute("""SELECT SUM(imp_cuota) FROM tarjeta_credito 
                                        where fecha = ?;""", (f,))
                importe = sql_cursor_2.fetchone()[0]
                importe = float(importe)
                importe = round(importe, 2)

                sql_cursor_3.execute("""INSERT INTO contabilidad 
                                        (tipo, id, tip_cont, descrip, fecha, importe)
                                        VALUES ('Gasto', ?, 'Tarjeta de credito', '', ?, ?)""",
                                        (id, f, importe,))
                
            elif resultado != None:

                sql_cursor_2.execute("""SELECT SUM(imp_cuota) FROM tarjeta_credito 
                                        WHERE fecha = ?;""", (f,))
                
                importe = sql_cursor_2.fetchone()[0]
                importe = float(importe)
                importe = round(importe, 2)
                
                sql_cursor_3.execute("""UPDATE contabilidad SET importe = ?
                                        WHERE ID = ?""", (importe, resultado,))

            conector.commit()
            sql_cursor_1.close()
            sql_cursor_2.close()
            sql_cursor_3.close()
            
        sql_cursor_0.close()
        conector.close()
        

    
    def gasto_tarjeta(self, ventana, imp, tip_cont, descrip, fecha, cuotas, interes, tasa):
        
        """
        Crea un registro en la tabla "tarjeta_credito".
        """
        try:

            #Verifica errores
            self.valida_fecha(fecha)
            imp = float(imp)
            cuotas = float(cuotas)
            interes = int(interes)

            if interes == 0:
                tasa = float(tasa)

            if interes == 0 and tasa <= 0:
                raise ZeroDivisionError

            #Verifica condiciones
            if interes == 1:
                importe = round(imp / cuotas, 2)
            elif interes == 0:
                x = imp * tasa / 100
                importe = round((imp + x) / cuotas, 2)
            
            #Crea fechas de las cuotas
            fec_cuotas =  self.conta_fecha(fecha, cuotas)
            
            #Variables
            n_cuotas = 1
            id_tc = self.crear_id('tarjeta_credito')

            #Crea registro en tabla tarjeta de credito.
            for i in fec_cuotas:
                
                conector_0 = connect('base.db')
                sql_cursor_0 = conector_0.cursor()
            
                sql_cursor_0.execute("""INSERT INTO "tarjeta_credito" 
                                        (id_tc, fecha, tip_cont, descrip, cuota, imp_cuota, imp_tot)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                        (id_tc, i, tip_cont, descrip, n_cuotas, importe, imp))
                
                n_cuotas = n_cuotas + 1
                
                conector_0.commit()
                sql_cursor_0.close()
                conector_0.close()

            ventana.destroy()

            messagebox.showinfo(title='Información', message='Se creo el registro correctamente.') 

        except ValueError:
            messagebox.showerror(title='Advertencia', 
                                 message='Se ingreso un registro con un formato erroneo.')

        except FechaInvalida:
            messagebox.showerror(title='Advertencia', 
                                 message='Se ingreso una fecha con un formato erroneo.')

        except ZeroDivisionError:
            messagebox.showerror(title='Advertencia', 
                                 message='La tasa de interes no puede ser cero o menor a cero.')

        finally:
            self.tc_contabilidad()


    def del_tc(self, id, ventana):

        """
        Borra el registro seleccionado de la tabla "tarjeta_credito".
        """

        mensaje = messagebox.askyesno(title='Advertencia',
                                      message='¿Desea eliminar el registro seleccionado?')

        if mensaje == True:

            conector = connect('base.db')
            sql_cursor = conector.cursor()

            sql_cursor.execute("""DELETE FROM tarjeta_credito WHERE id_tc = ?""",
                              (id,))
            
            conector.commit()
            sql_cursor.close()
            conector.close()

            messagebox.showinfo(title='Información', message='Se elimino el registro seleccionado')

            self.tc_contabilidad()

            ventana.destroy()


    def genera_prestamo(self, ventana, fecha, descrip, cuota, imp_cuota, 
                        imp_tot, imp_dev):
        
        """
        Genera un registro en la tabla prestamo.
        """

        try:
            #Manejo de errores
            self.valida_fecha(fecha)
            cuota = int(cuota)
            
            if cuota > 99:
                raise MaximoPermitido
            if cuota <= 0:
                raise MinimoPermitido
            
            imp_cuota = float(imp_cuota)
            imp_tot = float(imp_tot)

            #Conexión a base de datos.
            conector = connect('base.db')
            sql_query_0 = conector.cursor()
            sql_query_1 = conector.cursor()
            sql_query_2 = conector.cursor()

            id_prestamo = self.crear_id('prestamo')
            id_conta = self.crear_id('contabilidad')

            fec_prestamo = self.conta_fecha(fecha, cuota)

            #Genera registro en tabla prestamo.
            sql_query_0.execute("""INSERT INTO prestamo 
                                (id, fecha, descrip, cuota, imp_cuota, imp_tot, imp_dev)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                (id_prestamo, fecha, descrip, cuota, imp_cuota, imp_tot, imp_dev,))
            conector.commit()
            sql_query_0.close()
            #Genera registro de tipo ingreso en tabla contabilidad.
            sql_query_1.execute("""INSERT INTO contabilidad 
                                (tipo, id, tip_cont, id_prest, descrip, fecha, importe)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                ('Ingreso', id_conta, 'Prestamo', id_prestamo, descrip, fecha, imp_tot,))
            conector.commit()
            sql_query_1.close()
            #Genera registro de tipo gasto (cuotas) en tabla contabilidad.
        
            n_cuota = 1

            for fec in fec_prestamo:
            
                id_conta = self.crear_id('contabilidad')

                sql_query_2.execute("""INSERT INTO contabilidad 
                                    (tipo, id, tip_cont, id_prest, descrip, fecha, importe)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                    ('Gasto', id_conta, 'Prestamo', id_prestamo, 
                                    f'Cuota n°{n_cuota} - {descrip}', fec, imp_cuota,))
                conector.commit()
            
                n_cuota = n_cuota +1

            sql_query_2.close()
            conector.close()

            messagebox.showinfo(title='Información', message='Se genero el registro correctamente.')
            
            ventana.destroy()

        except ValueError:
            messagebox.showerror(title='Advertencia', 
                                message='Se ingreso un importe con un formato erroneo.')
        except FechaInvalida:
            messagebox.showerror(title='Advertencia', 
                                message='Se ingreso una fecha con un formato erroneo.')
        except MaximoPermitido:
            messagebox.showerror(title='Advertencia', 
                        message='La cantidad de cuotas supera el máximo permitido.')
        except MinimoPermitido:
                messagebox.showerror(title='Advertencia', 
                message='La cantidad de cuotas no puede ser cero o menor a cero.')


    def del_prestamo(self, id, ventana):
        
        """
        Borra un registro de la tabla prestamo.
        """
        mensaje = messagebox.askyesno(title='Advertencia',
                                      message='¿Desea eliminar el registro seleccionado?')
                                          
        if mensaje == True:
            conector = connect('base.db')
            sql_cursor_0 = conector.cursor()
            sql_cursor_2 = conector.cursor()

            sql_cursor_0.execute("""SELECT id FROM contabilidad WHERE id_prest = ?""",
                                (id,))
            ids = sql_cursor_0.fetchall()
            sql_cursor_0.close()

            lista = []
            
            for x in range(0, len(ids)):
                y = ids[x]
                lista.append(y[0])

            for i in lista:
                sql_cursor_1 = conector.cursor()
                sql_cursor_1.execute("""DELETE FROM contabilidad WHERE id = ?""",(i,))
                conector.commit()
                sql_cursor_1.close()

            sql_cursor_2.execute("""DELETE FROM prestamo WHERE id = ?""",(id,))
            conector.commit()

            sql_cursor_2.close()
            messagebox.showinfo(title='Información', message='Se elimino correctamente el registro seleccionado.')
            ventana.destroy()    

            sql_cursor_2.close()
            conector.close()


    def crea_ahorro(self, ventana, fec_ven, moneda, imp, tasa, rdinero, tint, fven):
        
        """
        Crea un registro en la tabla ahorro.
        """

        conector = connect('base.db')
        
        try:
            
            #Verifica que este parametrizada el valor de las divisas
            if self.euroblue_compra == None:
                raise TypeError
            elif self.euroblue_venta == None:
                raise TypeError
            elif self.dolarblue_compra == None:
                raise TypeError
            elif self.dolarblue_venta == None:
                raise TypeError

            #Verifica errores
            if tint == 1:
                tasa = float(tasa)
            else:
                tasa = 0
            
            if fven == 1:
                self.valida_fecha(fec_ven)
            else:
                fec_ven = None

            #Valida formato de importe
            imp = float(imp)

            

            if tasa > 0:
                valor = imp * tasa / 100
                imp_fin = imp + valor
            else:
                imp_fin = imp

            id = self.crear_id('ahorro')

            sql_cursor_1 = conector.cursor()

            sql_cursor_1.execute("""INSERT INTO ahorro 
                                (id, fec_venc, moneda, imp, tasa, imp_final)
                                VALUES (?, ?, ?, ?, ?, ?);""",
                                (id, fec_ven, moneda, imp, tasa, imp_fin,))
            
            conector.commit()
            sql_cursor_1.close()

            fecha = date.today()
            an_actual = fecha.year
            mes_actual = fecha.month
            dia = fecha.day

            if mes_actual < 10 and dia < 10:
                fec_reg = f'{an_actual}-0{mes_actual}-0{dia}'
            elif mes_actual < 10 and dia > 9:
                fec_reg = f'{an_actual}-0{mes_actual}-{dia}'
            elif mes_actual > 9 and dia < 10:
                fec_reg = f'{an_actual}-{mes_actual}-0{dia}'
            elif mes_actual > 9 and dia > 9:
                fec_reg = f'{an_actual}-{mes_actual}-{dia}'
            
            if rdinero == 1 and moneda == 'Peso':
                
                id_conta = self.crear_id('contabilidad')
                sql_cursor_2 = conector.cursor()

                sql_cursor_2.execute("""INSERT INTO contabilidad
                                     (tipo, id, tip_cont, id_prest, descrip, fecha, importe)
                                     VALUES ('Gasto', ?, 'Ahorro', '', '', ?, ?)""",
                                     (id_conta, fec_reg, imp))

                conector.commit()
                sql_cursor_2.close()
        
            if rdinero == 1 and moneda == 'Dolar':
            
                id_conta = self.crear_id('contabilidad')
                imp = imp * self.dolarblue_venta
                imp = round(imp, 2)
                sql_cursor_2 = conector.cursor()
                sql_cursor_2.execute("""INSERT INTO contabilidad
                                    (tipo, id, tip_cont, id_prest, descrip, fecha, importe)
                                    VALUES ('Gasto', ?, 'Ahorro', '', 'Compra divisa extranjera', ?, ?)""",
                                    (id_conta, fec_reg, imp))
                conector.commit()
                sql_cursor_2.close()
        
            if rdinero == 1 and moneda == 'Euro':
    
                id_conta = self.crear_id('contabilidad')
                imp = imp * self.euroblue_venta
                imp = round(imp, 2)
                sql_cursor_2 = conector.cursor()
                sql_cursor_2.execute("""INSERT INTO contabilidad
                                    (tipo, id, tip_cont, id_prest, descrip, fecha, importe)
                                    VALUES ('Gasto', ?, 'Ahorro', '', 'Compra divisa extranjera', ?, ?)""",
                                    (id_conta, fec_reg, imp))
                conector.commit()
                sql_cursor_2.close()
        
            messagebox.showinfo(title='Información',
                                message='Se genero el registro correctamente.')

            ventana.destroy()
            
        except ValueError:
            messagebox.showerror(title='Advertencia', 
                        message='Se ingreso un valor con formato erroneo.')

        except FechaInvalida:
            messagebox.showerror(title='Advertencia', 
                        message='Se ingreso una fecha con un formato erroneo.')

        except TypeError:
            messagebox.showerror(title='Error', message='Falta parametrizar el valor de la divisa.')
        
        finally:
            conector.close()

    
    def del_ahorro(self, id):

        """
        Elimina registros tipo ahorro.
        """
        
        mensaje = messagebox.askyesno(title='Advertencia',
                                      message='Se eliminara el registro de la base de datos ¿desea continuar?')
        if mensaje == True:
            conector = connect('base.db')
            sql_cursor = conector.cursor()
            
            sql_cursor.execute('DELETE FROM ahorro WHERE id = ?;',(id,))

            conector.commit()
            sql_cursor.close()
            conector.close()

            messagebox.showinfo(title='Información',
                                message='Se elimino el registro seleccionado')


    def ahorro_vencido(self):
        
        """
        Función que verifica la fecha de vencimiento de los ahorros.
        Si esta vencido, genera un registro de tipo "Ingreso" con el valor final.
        El registro de la tabla ahorro se elimina.
        """
        #Variables
        fecha = date.today()
        ids = list()
    
        #Conexion a base
        conector = connect('base.db')
        sql_cursor = conector.cursor()
        sql_cursor.execute("""SELECT id FROM ahorro WHERE fec_venc <= ? and fec_venc !='';""", (fecha,))
        valores = sql_cursor.fetchall()
        sql_cursor.close()
    
        for i in range(0, len(valores)) :
            x = valores[i]
            ids.append(x[0])
        
        
        if len(ids) > 0:

            importe = 0
            sql_cursor = conector.cursor()

            for i in ids:
                sql_cursor.execute("""SELECT imp_final FROM ahorro WHERE id = ?;""", (i,))
                valor = sql_cursor.fetchone()[0]
                importe = importe + valor
                importe = round(importe, 2)
    
            sql_cursor.close()
    
            id = self.crear_id('contabilidad')
    
            sql_cursor_insert = conector.cursor()
            sql_cursor_insert.execute("""INSERT INTO contabilidad 
                                         (tipo, id, tip_cont, descrip, fecha, importe)
                                         VALUES ('Ingreso', ?, 'Ahorro', '', ?, ?)""",
                                         (id, fecha, importe,))

            conector.commit()
            sql_cursor_insert.close()

            sql_query_delete = conector.cursor()
        
            for i in ids:
                sql_query_delete.execute("""DELETE FROM ahorro WHERE id = ?""", (i,))
                conector.commit()
        
            sql_query_delete.close()
            conector.close()


#Excepciones propias.
class FechaInvalida(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Fecha invalida'
        self.informacion = 'El formato de la fecha ingresado es invalido'
        print(self.mensaje)
        print(self.informacion)

class CaracterInvalido(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Caracter invalido'
        self.informacion = 'El campo contiene caracteres invalidos'
        print(self.mensaje)
        print(self.informacion)

class NoExisteRegistro(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Sin selección de id'
        self.informacion = 'No se selecciono un campo con formato id'
        print(self.mensaje)
        print(self.informacion)

class ErrorFecha(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Mes erroneo.'
        self.informacion = 'Falta seleccionar el mes o año.'
        print(self.mensaje)
        print(self.informacion)

class MaximoPermitido(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Maximo de cuotas erroneo.'
        self.informacion = 'El maximo de cuotas supera el limite permitido.'
        print(self.mensaje)
        print(self.informacion)

class MinimoPermitido(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Minimo de cuotas erroneo.'
        self.informacion = 'Las cuotas no pueden ser cero o menor a cero.'
        print(self.mensaje)
        print(self.informacion)

class ExisteRegistro(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Existe registro.'
        self.informacion = 'Ya existe un registro con el mismo nombre en la base de datos.'
        print(self.mensaje)
        print(self.informacion)

class FaltaParametro(Exception):
    
    def __init__(self):
        super().__init__()
        self.mensaje = 'Falta parrametro.'
        self.informacion = 'No se puede generar registro por falta de datos.'
        print(self.mensaje)
        print(self.informacion)
