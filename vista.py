from tkinter import Checkbutton 
from tkinter import Entry
from tkinter import messagebox
from tkinter import Tk
from tkinter import Toplevel
from tkinter import Menu
from tkinter import Frame
from tkinter import Label
from tkinter import Radiobutton
from tkinter import PanedWindow
from tkinter import Button
from tkinter import IntVar
from tkinter import Scrollbar
from tkinter import Spinbox
from tkinter import TclError
from tkinter.ttk import Notebook
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
from tkinter.ttk import Separator
from tkinter.ttk import Style
from tkinter.constants import BOTH
from tkinter.constants import END
from tkinter.constants import DISABLED
from tkinter.constants import NORMAL
from tkinter.constants import VERTICAL
from tkinter.constants import TOP
from tkinter.constants import X
from tkinter.constants import RAISED
from PIL import Image
from PIL import ImageTk
from modelo import ConfigApp 
from modelo import CondFinanciera
from modelo import ErrorFecha
from webbrowser import open

class MainWindow():
        
    contabilidad = CondFinanciera()
    configuracion = ConfigApp()

    id_contabilidad = None
    id_tc = None
    id_prestamo = None
    id_ahorro = None

    def __init__(self):

        """
        Crea el formulario principal de la aplicación Financiera Versión 1.0
        """

        #Verifica la tabla tarjeta de crédito para actualizar 
        #registros en contabilidad
        self.contabilidad.tc_contabilidad()
        
        year = self.configuracion.get_year()
        
        #Formulario principal.
        root = Tk()

        #Estilo para el treeview
        estilo = Style()
        estilo.theme_use('alt')
        
        #Menu
        mainmenu  = Menu(root)
        root.config(menu=mainmenu)
        #Menu archivo
        archivo = Menu(mainmenu, tearoff=0)
        archivo.add_command(label='Salir', 
                            command= lambda: self.verifica_cierre(root))
        #Menu ver
        ver = Menu(mainmenu, tearoff=0)
        ver.add_command(label='Ahorros', command=self.visualiza_ahorro)
        ver.add_separator()
        ver.add_command(label='Prestamos', command=self.frm_vis_prestamo)
        ver.add_command(label='Tarjeta de crédito', command=self.visua_tc)
        
        
        #Menu insertar
        insertar = Menu(mainmenu, tearoff=0)
        insertar.add_command(label='Ingreso', 
                             command= lambda: self.form_ingreso('Ingreso'))
        insertar.add_command(label='Ahorro', command=self.form_ahorro)
        insertar.add_command(label='Credito', command=self.form_prestamo)
        insertar.add_separator()
        insertar.add_command(label='Gasto', 
                             command= lambda: self.form_ingreso('Gasto'))
        insertar.add_command(label='Tarjeta de credito', command=self.form_tarjeta)
        #Menu parametros
        parametros = Menu(mainmenu, tearoff=0)
        parametros.add_command(label='Divisas', command=self.par_divisa)
        parametros.add_separator()
        parametros.add_command(label='Parametros', command=self.frm_parametros)
        #Menu ayuda
        ayuda = Menu(mainmenu, tearoff=0)
        ayuda.add_command(label='Ayuda', command= lambda: open('ayuda.html'))
        ayuda.add_separator()
        ayuda.add_command(label='Acerca de', command=self.acerca_de)

        mainmenu.add_cascade(label='Archivo', menu=archivo)
        mainmenu.add_cascade(label='Ver', menu=ver)
        mainmenu.add_cascade(label='Ingresar', menu=insertar)
        mainmenu.add_cascade(label='Configuración', menu=parametros)
        mainmenu.add_cascade(label='Ayuda', menu=ayuda)        

        #Barra acceso directo a funciones.
        frm_frspanel = PanedWindow(root, height=40, relief=RAISED)
        frm_frspanel.pack(fill=X, side=TOP)  
        
        ruta = Image.open('recursos/imagenes/ingresos.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_ingreso = ImageTk.PhotoImage(ruta)
        btn_ingreso = Button(frm_frspanel, 
                             image=img_ingreso, 
                             command=lambda: self.form_ingreso('Ingreso'))
        btn_ingreso.place(x=4, y=3, width=30, height=30)

        ruta = Image.open('recursos/imagenes/gastos.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_gasto = ImageTk.PhotoImage(ruta)
        btn_gasto = Button(frm_frspanel, 
                           image=img_gasto, 
                           command=lambda: self.form_ingreso('Gasto'))
        btn_gasto.place(x=42, y=3, width=30, height=30)

        ruta = Image.open('recursos/imagenes/ahorro.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_ahorro = ImageTk.PhotoImage(ruta)
        btn_ahorro = Button(frm_frspanel, 
                            image=img_ahorro, 
                            command=self.form_ahorro)
        btn_ahorro.place(x=80, y=3, width=30, height=30)

        ruta = Image.open('recursos/imagenes/tarjeta de credito.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_credito = ImageTk.PhotoImage(ruta)
        btn_credito = Button(frm_frspanel, 
                             image=img_credito, 
                             command=self.form_tarjeta)
        btn_credito.place(x=118, y=3, width=30, height=30)

        ruta = Image.open('recursos/imagenes/prestamos.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_prestamo = ImageTk.PhotoImage(ruta)
        btn_prestamo = Button(frm_frspanel, 
                              image=img_prestamo, 
                              command=self.form_prestamo)
        btn_prestamo.place(x=156, y=3, width=30, height=30)

        sep1 = Separator(frm_frspanel, orient=VERTICAL)
        sep1.place(x=194, y=3, height=30)
    
        ruta = Image.open('recursos/imagenes/información.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_info = ImageTk.PhotoImage(ruta)
        btn_info = Button(frm_frspanel, image=img_info, command=self.frm_totales)
        btn_info.place(x=202, y=3, width=30, height=30)

        ruta = Image.open('recursos/imagenes/configuración.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_conf = ImageTk.PhotoImage(ruta)
        btn_conf = Button(frm_frspanel, image=img_conf, command=self.frm_parametros)
        btn_conf.place(x=240, y=3, width=30, height=30)

        frm_secpanel = PanedWindow(root, height=35, relief=RAISED)
        frm_secpanel.pack(fill=X, side=TOP)  
        
        lb0 = Label(frm_secpanel, text='Visualizar')
        lb0.place(x=2, y=2)
        sep2 = Separator(frm_secpanel, orient=VERTICAL)
        sep2.place(x=60, y=3, height=25)
        
        result_main = IntVar()
        result_main.set(1)

        rd_mes = Radiobutton(frm_secpanel, text='Mensual', 
                             variable=result_main, value=1)
        rd_mes.place(x=65, y=2)
        rd_year = Radiobutton(frm_secpanel, text='Anual', 
                              variable=result_main, value=2)
        rd_year.place(x=140, y=2)
        rd_todo = Radiobutton(frm_secpanel, text='Todo', 
                              variable=result_main, value=3)
        rd_todo.place(x=205, y=2)

        sep3 = Separator(frm_secpanel, orient=VERTICAL)
        sep3.place(x=270, y=3, height=25)

        lb1 = Label(frm_secpanel, text='Mes')
        lb1.place(x=280, y=2)
        lb2 = Label(frm_secpanel, text='Año')
        lb2.place(x=450, y=2)
        self.cb_mes = Combobox(frm_secpanel, 
                               values=ConfigApp.MES,
                               state='readonly')
        self.cb_mes.place(x=320, y=2, width=120, height=25)
        self.cb_year = Combobox(frm_secpanel, 
                                values=year)
        self.cb_year.place(x=490, y=2, width=120, height=25)
        
        sep4 = Separator(frm_secpanel, orient=VERTICAL)
        sep4.place(x=630, y=3, height=25)

        bt_ver = Button(frm_secpanel, text='Ver',
                        command= lambda: self.show_data(result_main.get()))
        bt_ver.place(x=650, y=2, width=60, height=25)

        #Pestaña
        self.pestana = Notebook(root)
        self.pestana.pack(fill=BOTH, expand=1)
        
        #Pestaña gastos
        self.frm_ingresos = Frame(self.pestana) 
        self.ing_scroll_v = Scrollbar(self.frm_ingresos, orient= VERTICAL)
        self.ing_scroll_v.place(x=750, y=1, height=180)
        
        self.tv_ingresos = Treeview(self.frm_ingresos, 
                                    selectmode='browse',
                                    yscrollcommand=self.ing_scroll_v.set)
        self.tv_ingresos.place(x=1, y=1, width=750, height=180)
        self.tv_ingresos['columns'] = ('fecha', 'tipo', 'importe')
        
        self.tv_ingresos.column('#0', width=0, minwidth=0, stretch=False)
        self.tv_ingresos.column('fecha', width=90, minwidth=60)
        self.tv_ingresos.column('tipo', width=90, minwidth=60)
        self.tv_ingresos.column('importe', width=90, minwidth=60)
        
        self.tv_ingresos.heading('#0', text='')
        self.tv_ingresos.heading('fecha', text='Fecha')
        self.tv_ingresos.heading('tipo', text='Tipo ingreso')
        self.tv_ingresos.heading('importe', text='Importe')

        
        self.ing_scroll_v.config(command=self.tv_ingresos.yview)
        
        self.tv_ingresos.bind("<<TreeviewSelect>>", self.identificar_id_ingresos)

        self.contabilidad.visualizar_treeview(self.tv_ingresos, 'Ingreso')

        #Botones
        self.btn_nuevo_ing = Button(self.frm_ingresos, text='Nuevo',
                                    command= lambda: self.form_ingreso('Ingreso'))
        self.btn_nuevo_ing.place(x=680, y=210, width=80, height=25)

        self.btn_modificar_ing  = Button(self.frm_ingresos, 
                                         text='Modificar', command=self.frm_visual_ingreso)
        self.btn_modificar_ing.place(x=580, y=210, width=80, height=25)

        self.btn_eliminar_ing  = Button(self.frm_ingresos, 
                                        text='Eliminar', command = self.del_ingreso)
        self.btn_eliminar_ing.place(x=480, y=210, width=80, height=25)

        #Pestaña gastos
        self.frm_gastos = Frame(self.pestana) 
        self.gst_scroll_v = Scrollbar(self.frm_gastos, orient=VERTICAL)
        self.gst_scroll_v.place(x=750, y=1, height=180)
        self.tv_gastos = Treeview(self.frm_gastos,
                                  selectmode='browse',
                                  yscrollcommand=self.gst_scroll_v.set)
        self.tv_gastos.place(x=1, y=1, width=750, height=180)
        self.tv_gastos['columns'] = ('fecha', 'tipo', 'importe')
        
        self.tv_gastos.column('#0', width=0, minwidth=0, stretch=False)
        self.tv_gastos.column('fecha', width=90, minwidth=60)
        self.tv_gastos.column('tipo', width=90, minwidth=60)
        self.tv_gastos.column('importe', width=90, minwidth=60)
        
        self.tv_gastos.heading('#0', text='')
        self.tv_gastos.heading('fecha', text='Fecha')
        self.tv_gastos.heading('tipo', text='Tipo gasto')
        self.tv_gastos.heading('importe', text='Importe')
        
        self.gst_scroll_v.config(command=self.tv_gastos.yview)

        self.contabilidad.visualizar_treeview(self.tv_gastos, 'Gasto')

        self.tv_gastos.bind("<<TreeviewSelect>>", self.identificar_id_gastos)

        #Botones
        btn_nuevo_gst = Button(self.frm_gastos, 
                               text='Nuevo',
                               command=lambda: self.form_ingreso('Gasto'))
        btn_nuevo_gst.place(x=680, y=210, width=80, height=25)

        btn_modificar_gst  = Button(self.frm_gastos, 
                                    text='Modificar', command=self.frm_visual_ingreso)
        btn_modificar_gst.place(x=580, y=210, width=80, height=25)

        btn_eliminar_gst  = Button(self.frm_gastos, 
                                   text='Eliminar', 
                                   command= lambda: self.del_gasto())
        btn_eliminar_gst.place(x=480, y=210, width=80, height=25)
        
        self.pestana.add(self.frm_ingresos, text='Ingresos')
        self.pestana.add(self.frm_gastos, text='Gastos')

        self.pestana.bind('<<NotebookTabChanged>>',self.limpia_id)

        root.protocol("WM_DELETE_WINDOW", lambda: self.verifica_cierre(root))

        #Centra formulario.
        app_width = 770
        app_height = 345 
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        root.resizable(0,0)
        root.title('Libreta')
        root.mainloop()


    def verifica_cierre(self, ventana):
        
        """
        Verifica el cierre de la aplicación.
        """

        if messagebox.askyesno(title='Advertencia',
                                  message='¿Seguro quiere salir del programa?'):
            ventana.destroy()


    def show_data(self, op):

        """
        Visualiza los datos en el treeview.
        """

        month_name = self.cb_mes.get()
        year = self.cb_year.get()
        name_tab = self.pestana.index(self.pestana.select())     

        #Visualización de datos por año y mes
        try:

            if op == 1 and (month_name == '' or year == ''):
                raise ErrorFecha

            if month_name == 'Enero':
                mes = 1
            elif month_name == 'Febrero':
                mes = 2
            elif month_name == 'Marzo':
                mes = 3    
            elif month_name == 'Abril':
                mes = 4
            elif month_name == 'Mayo':
                mes = 5
            elif month_name == 'Junio':
                mes = 6
            elif month_name == 'Julio':
                mes = 7
            elif month_name == 'Agosto':
                mes = 8
            elif month_name == 'Septiembre':
                mes = 9
            elif month_name == 'Octubre':
                mes = 10
            elif month_name == 'Noviembre':
                mes = 11
            elif month_name == 'Diciembre':
                mes = 12

            if op == 1 and name_tab == 0:
                for row in self.tv_ingresos.get_children():
                    self.tv_ingresos.delete(row)
                self.contabilidad.treeview_mensual(self.tv_ingresos,
                                                   'Ingreso', mes, year)
            elif op == 1 and name_tab == 1:
                for row in self.tv_gastos.get_children():
                    self.tv_gastos.delete(row)
                self.contabilidad.treeview_mensual(self.tv_gastos, 
                                                   'Gasto', mes, year)
        except ErrorFecha:
            messagebox.showerror(title='Error', message='Falta seleccionar año o mes.') 
        
        #Visualización de datos por año
        try:
            if op == 2 and year == '':
                raise ErrorFecha

            if op == 2 and name_tab == 0:
                for row in self.tv_ingresos.get_children():
                    self.tv_ingresos.delete(row)
                self.contabilidad.treeview_year(self.tv_ingresos,
                                                 'Ingreso',
                                                 year)
            elif op == 2 and name_tab == 1:
                for row in self.tv_gastos.get_children():
                    self.tv_gastos.delete(row)
                self.contabilidad.treeview_year(self.tv_gastos,
                                                'Gasto',
                                                year)            
        except ErrorFecha:
            messagebox.showerror(title='Error', message='Falta seleccionar año.')

        #Visualización de todos los datos en tabla
        if op == 3 and name_tab == 0:
            for row in self.tv_ingresos.get_children():
                self.tv_ingresos.delete(row)
            self.contabilidad.visualizar_treeview(self.tv_ingresos, 'Ingreso')
        elif op == 3 and name_tab == 1:
            for row in self.tv_gastos.get_children():
                self.tv_gastos.delete(row)
            self.contabilidad.visualizar_treeview(self.tv_gastos, 'Gasto')

    
    def del_ingreso(self):

        """
        Elimina un registro de tipo ingreso y actualiza el widget treeview(tkinter).
        """
        
        self.contabilidad.eliminar_registro(self.id_contabilidad)
        for row in self.tv_ingresos.get_children():
            self.tv_ingresos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_ingresos,'Ingreso')


    
    def del_gasto(self):
        
        """
        Elimina un registro de tipo gasto y actualiza el widget treeview(tkinter).
        """
        self.contabilidad.eliminar_registro(self.id_contabilidad)
        for row in self.tv_gastos.get_children():
            self.tv_gastos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_gastos,'Gasto')


    
    def identificar_id_ingresos (self, event):

        """
        Identifica el id (sql) para realizar una acción - Ingresos.
        """
        
        self.id_contabilidad = self.tv_ingresos.selection()[0]
        return self.id_contabilidad


    def identificar_id_gastos (self, event):
        
        """
        #Identifica el id (sql) para realizar una acción - Gastos.
        """
        self.id_contabilidad = self.tv_gastos.selection()[0]          
        return self.id_contabilidad

    
    def identificar_tc(self, event):
        
        """
        Identifica el id (sql) para el formulario de tarjeta de crédito.
        """

        self.id_tc = self.tv_tarjeta.selection()[0]
        return self.id_tc


    
    def limpia_id(self, event):
        
        """
        Función limpia id cuando cambia de pestaña
        """
        self.id_contabilidad = None

    
    def identificar_prestamo(self, event):

        """
        Identifica el id (sql) para el formulario de prestamo.
        """

        self.id_prestamo = self.tv_prestamo.selection()[0]
        return self.id_prestamo

   
    def identificar_ahorro(self, event):

        """
        Identifica el id (sql) para el formulario de ahorro.
        """
        self.id_ahorro = self.tv_ahorro.selection()[0]
        return self.id_ahorro


    def acerca_de(self):

        """
        Crea el formulario "Acerca de..."
        """
        
        acercade = Toplevel()
        lbl1 = Label(acercade, text = 'Finanzas - Versión 1.0')
        lbl1.place(x= 1, y= 1)
        lbl2 = Label(acercade, text = 'UTN.BA Centro de e-learning')
        lbl2.place(x= 1, y= 21)
        lbl3 = Label(acercade, text = 'Desarrollado por: Jorge Eduardo Arrieta')
        lbl3.place(x= 1, y= 41)
        lbl4 = Label(acercade, text = 'Año, 2021 - Buenos Aires, Argentina')
        lbl4.place(x= 1, y= 61)
        btnCerrar = Button(acercade,text='Cerrar',command=acercade.destroy)
        btnCerrar.place(x= 190, y= 95)
        

        app_width = 250
        app_height = 130 
        screen_width = acercade.winfo_screenwidth()
        screen_height = acercade.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        acercade.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        
        acercade.attributes('-toolwindow',-1)
        acercade.resizable(0,0)
        acercade.title('Acerca de...')
        acercade.grab_set()
        acercade.focus_set()
        acercade.wait_window() 

        
    def form_ingreso(self, tipo):

        """
        Crea el formulario de ingresos o gastos.
        """
        
        self.win_ingreso = Toplevel()
        
        lb0 = Label(self.win_ingreso)
        lb0.place(x=17, y=15)
        if tipo == 'Ingreso':
            lb0['text'] = 'Tipo de ingreso:'
        elif tipo == 'Gasto':
            lb0['text'] = 'Tipo de gasto:'   

        lb1 = Label(self.win_ingreso, text='Descripción:')
        lb1.place(x=17, y=54)
        lb2 = Label(self.win_ingreso, text='Fecha:')
        lb2.place(x=17, y=93)
        lb3 = Label(self.win_ingreso, text='Importe:')
        lb3.place(x=17, y=132)
        
        self.cb_ing_tipo = Combobox(self.win_ingreso, state='readonly')
        self.cb_ing_tipo.place(x= 108, y=15, width=180)
        if tipo == 'Ingreso':
            self.cb_ing_tipo['values'] = self.configuracion.show_par('Ingreso')
        elif tipo == 'Gasto':
            self.cb_ing_tipo['values'] = self.configuracion.show_par('Gastos')

        self.tx_ing_descripcion = Entry(self.win_ingreso)
        self.tx_ing_descripcion.place(x= 108, y=54, width=180)
        self.tx_ing_fecha = Entry(self.win_ingreso)
        self.tx_ing_fecha.place(x= 108, y=93, width=180)
        self.tx_ing_importe = Entry(self.win_ingreso)
        self.tx_ing_importe.place(x= 108, y=132, width=180)
        btn_ing_cerrar = Button(self.win_ingreso, text='Cerrar',
                                command=self.win_ingreso.destroy)
        btn_ing_cerrar.place(x= 120, y=165, width=80)
        
        btn_ing_guardar = Button(self.win_ingreso, text='Guardar')
        if tipo == 'Ingreso':
            btn_ing_guardar['command'] = lambda: self.crear_registro('Ingreso')
        elif tipo == 'Gasto':
            btn_ing_guardar['command'] = lambda: self.crear_registro('Gasto')
        btn_ing_guardar.place(x= 209, y=165, width=80)

        app_width = 300
        app_height = 200 
        screen_width = self.win_ingreso.winfo_screenwidth()
        screen_height = self.win_ingreso.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        self.win_ingreso.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        if tipo == 'Ingreso':
            self.win_ingreso.title('Alta de ingreso')
        elif tipo == 'Gasto':  
            self.win_ingreso.title('Alta de gasto')

        self.win_ingreso.resizable(0,0)
        self.win_ingreso.attributes('-toolwindow',-1)
        self.win_ingreso.grab_set()
        self.win_ingreso.focus_set()
        self.win_ingreso.wait_window()


    def crear_registro(self, tipo):

        """
        Genera un registro de tipo ingreso/gasto.
        """

        self.contabilidad.crear_registro(self.win_ingreso,
                                         tipo,
                                         self.cb_ing_tipo.get(),
                                         self.tx_ing_descripcion.get(),
                                         self.tx_ing_fecha.get(),
                                         self.tx_ing_importe.get())

        for row in self.tv_ingresos.get_children():
            self.tv_ingresos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_ingresos, 'Ingreso')

        for row in self.tv_gastos.get_children():
            self.tv_gastos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_gastos, 'Gasto')


    
    def frm_visual_ingreso(self):

        """
        Formulario para modificar la información completa de un item,
        de la tabla contabilidad.
        """
        
        try:
            
            if self.id_contabilidad != None:

                self.wn_visua_ingreso = Toplevel()
        
                lb0 = Label(self.wn_visua_ingreso, text='Tipo:')
                lb0.place(x=17, y=15)
                lb1 = Label(self.wn_visua_ingreso, text='Descripción:')
                lb1.place(x=17, y=54)
                lb2 = Label(self.wn_visua_ingreso, text='Fecha:')
                lb2.place(x=17, y=93)
                lb3 = Label(self.wn_visua_ingreso, text='Importe:')
                lb3.place(x=17, y=132)
        
                self.tx_ing_v_tipo = Entry(self.wn_visua_ingreso)
                self.tx_ing_v_tipo.place(x= 108, y=15, width=180)
                self.tx_ing_v_tipo.insert(0, 
                                        self.contabilidad.visualizar_registro(self.id_contabilidad, 
                                        'tip_cont'))
                     
                self.tx_ing_v_descripcion = Entry(self.wn_visua_ingreso)
                self.tx_ing_v_descripcion.place(x= 108, y=54, width=180)
                self.tx_ing_v_descripcion.insert(0, 
                                                self.contabilidad.visualizar_registro(self.id_contabilidad,
                                                'descrip'))
           
                self.tx_ing_v_fecha = Entry(self.wn_visua_ingreso)
                self.tx_ing_v_fecha.place(x= 108, y=93, width=180)
                self.tx_ing_v_fecha.insert(0, 
                                        self.contabilidad.visualizar_registro(self.id_contabilidad,
                                        'fecha'))
            
                self.tx_ing_v_importe = Entry(self.wn_visua_ingreso)
                self.tx_ing_v_importe.place(x= 108, y=132, width=180)
                self.tx_ing_v_importe.insert(0, 
                                            self.contabilidad.visualizar_registro(self.id_contabilidad,
                                            'importe'))
           
                btn_ing_cerrar = Button(self.wn_visua_ingreso, 
                                        text='Cerrar', 
                                        command=self.wn_visua_ingreso.destroy)
                btn_ing_cerrar.place(x= 120, y=165, width=80)
            
                btn_ing_guardar = Button(self.wn_visua_ingreso, 
                                        text='Guardar',
                                        command=self.actualizar_registro)
                btn_ing_guardar.place(x= 209, y=165, width=80)

                app_width = 300
                app_height = 200 
                screen_width = self.wn_visua_ingreso.winfo_screenwidth()
                screen_height = self.wn_visua_ingreso.winfo_screenheight()
                x = (screen_width / 2) - (app_width / 2)
                y = (screen_height / 2) - (app_height / 2)
                self.wn_visua_ingreso.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

                self.wn_visua_ingreso.title('Modificar')
                self.wn_visua_ingreso.attributes('-toolwindow',-1)
                self.wn_visua_ingreso.resizable(0,0)
                self.wn_visua_ingreso.grab_set()
                self.wn_visua_ingreso.focus_set()
                self.wn_visua_ingreso.wait_window()

            if self.id_contabilidad == None:
                messagebox.showinfo(title='Error', message='Falta seleccionar el item a visualizar.')
        
        except TclError:

            messagebox.showinfo(title='Error', message='Falta seleccionar el item a visualizar.')

        except AttributeError:

            messagebox.showinfo(title='Error', message='Falta seleccionar el item a visualizar.')


    def actualizar_registro(self):

        """
        Función para actualizar registros.
        Se excluye registros de tipo "tarjeta de credito", "ahorro" y/o "prestamo". 
        """
        
        self.contabilidad.act_registro(self.wn_visua_ingreso,
                                       self.id_contabilidad,
                                       self.tx_ing_v_tipo.get(),
                                       self.tx_ing_v_descripcion.get(),
                                       self.tx_ing_v_fecha.get(),
                                       self.tx_ing_v_importe.get()
                                      )
        
        name_tab = self.pestana.index(self.pestana.select())

        if name_tab == 0:
            for row in self.tv_ingresos.get_children():
                self.tv_ingresos.delete(row)
            self.contabilidad.visualizar_treeview(self.tv_ingresos, 'Ingreso')
        elif name_tab == 1:
            for row in self.tv_gastos.get_children():
                    self.tv_gastos.delete(row)
            self.contabilidad.visualizar_treeview(self.tv_gastos, 'Gasto')

    
    def form_ahorro(self):

        """
        Crea el formulario para dar de alta un registro de tipo ahorro.
        """
        
        self.result_ahorro = IntVar()
        self.result_ahorro.set(1)

        self.resta_dinero = IntVar()
        self.resta_dinero.set(1)

        self.vencimiento = IntVar()
        self.vencimiento.set(1)

        self.win_ahorro = Toplevel()

        lb0 = Label(self.win_ahorro, text='Moneda:')
        lb0.place(x=17, y=15)
        self.cb_ah_tipmoneda = Combobox(self.win_ahorro, values=ConfigApp.MONEDA, 
                                        state='readonly')
        self.cb_ah_tipmoneda.place(x=138, y=15, width=100)

        lb1 = Label(self.win_ahorro, text='Importe depositado:')
        lb1.place(x=17, y=56)
        self.tx_ah_importe = Entry(self.win_ahorro)
        self.tx_ah_importe.place(x=138, y=56, width=180)
        chk_si_rest = Checkbutton(self.win_ahorro, text='Resta a dinero disponible?', 
                                  variable=self.resta_dinero)
        chk_si_rest.place(x=341, y=56)

        chk_genera = Checkbutton(self.win_ahorro, text='Genera tasa de interés?', 
                                 variable=self.result_ahorro, command=self.entry_tasaint)
        chk_genera.place(x=17, y=97)
        lb2 = Label(self.win_ahorro, text='Tasa de interés:')
        lb2.place(x=200, y=97)
        self.tx_ah_tasa = Entry(self.win_ahorro)
        self.tx_ah_tasa.place(x=318, y=97, width=82)

        chk_vencimiento = Checkbutton(self.win_ahorro, text='Tiene fecha de vencimiento?', 
                         variable=self.vencimiento, command=self.entry_vencimiento)
        chk_vencimiento.place(x=17, y=138)

        lb3 = Label(self.win_ahorro, text='Fecha vencimiento:')
        lb3.place(x=200, y=138)
        self.tx_ah_fecven = Entry(self.win_ahorro)
        self.tx_ah_fecven.place(x=320, y=138, width=173)
         
        btn_cerrar = Button(self.win_ahorro, text='Cerrar', command=self.win_ahorro.destroy)
        btn_cerrar.place(x=320, y=177, width=80)
        btn_guardar = Button(self.win_ahorro, text='Generar',
                             command= self.crea_ahorro) 
        btn_guardar.place(x=413, y=177, width=80)

        app_width = 520
        app_height = 220 
        screen_width = self.win_ahorro.winfo_screenwidth()
        screen_height = self.win_ahorro.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.win_ahorro.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.win_ahorro.resizable(0,0)
        self.win_ahorro.attributes('-toolwindow',-1)
        self.win_ahorro.title('Cuenta de ahorro')
        self.win_ahorro.grab_set()
        self.win_ahorro.focus_set()
        self.win_ahorro.wait_window()
    
    def crea_ahorro(self):

        """
        Función para crear registros de tipo ahorro. 
        Actualiza los datos en el treeview.
        """
        
        self.contabilidad.crea_ahorro(self.win_ahorro,self.tx_ah_fecven.get(),
                                      self.cb_ah_tipmoneda.get(), self.tx_ah_importe.get(),
                                      self.tx_ah_tasa.get(), self.resta_dinero.get(),
                                      self.result_ahorro.get(), self.vencimiento.get())
            
        for row in self.tv_gastos.get_children():
            self.tv_gastos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_gastos, 'Gasto')


    
    def entry_tasaint(self):

        """
        Habilita o deshabilita el entry 'tasa de interés' del formulario ahorro.
        """

        if self.result_ahorro.get() == 1:
            self.tx_ah_tasa['state'] = NORMAL
        elif self.result_ahorro.get() == 0:
            self.tx_ah_tasa.delete(0, END)
            self.tx_ah_tasa['state'] = DISABLED
            

    def entry_vencimiento(self):

        """
        Habilita o deshabilita el entry 'fecha de vencimiento' del formulario ahorro.
        """
        if self.vencimiento.get() == 1:
            self.tx_ah_fecven['state'] = NORMAL
        elif self.vencimiento.get() == 0:
            self.tx_ah_fecven.delete(0, END)
            self.tx_ah_fecven['state'] = DISABLED
            

    def visualiza_ahorro(self):
        
        """
        Genera el formulario para visualizar los registros de la tabla ahorro.
        """

        self.win_vis_ahorro = Toplevel()

        marco = Frame(self.win_vis_ahorro)
        marco.place(x=1, y=1, width=550, height=200)

        scroll_ahorro = Scrollbar(marco, orient=VERTICAL)
        scroll_ahorro.place(x=530, y=1, height=200)

        self.tv_ahorro = Treeview(marco, yscrollcommand=scroll_ahorro.set)

        self.tv_ahorro['columns'] = ('fec_venc', 'moneda', 'imp', 'tasa', 'imp_final')

        self.tv_ahorro.column('#0', width=0, minwidth=0, stretch=False)
        self.tv_ahorro.column('fec_venc', width=90, minwidth=60)
        self.tv_ahorro.column('moneda', width=90, minwidth=60)
        self.tv_ahorro.column('imp', width=90, minwidth=60)
        self.tv_ahorro.column('tasa', width=90, minwidth=60)
        self.tv_ahorro.column('imp_final', width=90, minwidth=60)
        self.tv_ahorro.heading('#0', text='')
        self.tv_ahorro.heading('fec_venc', text='Fecha vencimiento')
        self.tv_ahorro.heading('moneda', text='Tipo de moneda')
        self.tv_ahorro.heading('imp', text='Importe depositado')
        self.tv_ahorro.heading('tasa', text='tasa de interes')
        self.tv_ahorro.heading('imp_final', text='Importe final')

        self.tv_ahorro.place(x=1, y=1, width=530, height=200)
        scroll_ahorro.config(command=self.tv_ahorro.yview)

        self.contabilidad.vis_tv_ahorro(self.tv_ahorro)

        self.tv_ahorro.bind('<<TreeviewSelect>>',self.identificar_ahorro)
        
        btn_eliminar = Button(self.win_vis_ahorro, text='Eliminar',
                             command=self.elimina_ahorro)
        btn_eliminar.place(x=370, y=210, width=80)

        btn_cerrar = Button(self.win_vis_ahorro, text='Cerrar', 
                            command=self.win_vis_ahorro.destroy)
        btn_cerrar.place(x=460, y=210, width=80)

        app_width = 550
        app_height = 250 
        screen_width = self.win_vis_ahorro.winfo_screenwidth()
        screen_height = self.win_vis_ahorro.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.win_vis_ahorro.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        
        self.win_vis_ahorro.resizable(0,0)
        self.win_vis_ahorro.attributes('-toolwindow',-1)
        self.win_vis_ahorro.title('Visualizar ahorros')

        self.win_vis_ahorro.grab_set()
        self.win_vis_ahorro.focus_set()
        self.win_vis_ahorro.wait_window()

    def elimina_ahorro(self):

        """
        Función que llama a la función para eliminar un registro ahorro, y actualiza el treeview.
        """

        print(self.id_ahorro)
        if self.id_ahorro != None:
            self.contabilidad.del_ahorro(self.id_ahorro)

            for row in self.tv_ahorro.get_children():
                self.tv_ahorro.delete(row)
            self.contabilidad.vis_tv_ahorro(self.tv_ahorro)

            self.id_ahorro = None

        else:
            messagebox.showerror(title='Error', message='Falta seleccionar un registro.')


    
    def form_prestamo(self):

        """
        Crea el formulario de prestamo / credito.
        """
    
        self.result_cred = IntVar()
        self.result_cred.set(1)

        window_pres = Toplevel()
        
        lb0 = Label(window_pres, text='Fecha:')
        lb0.place(x=17, y=15)
        self.tx_pres_fecha = Entry(window_pres)
        self.tx_pres_fecha.place(x=140, y=15, width=180)
        lb1 = Label(window_pres, text="Descripción:")
        lb1.place(x=17, y=53)
        self.tx_pres_descrip = Entry(window_pres)
        self.tx_pres_descrip.place(x=140, y=53, width=180)
        lb2 = Label(window_pres, text='Importe crédito:')
        lb2.place(x=17, y=91)
        self.tx_pres_imp_total = Entry(window_pres)
        self.tx_pres_imp_total.place(x=140, y=91, width=180)
        lb3 = Label(window_pres, text='Cantidad de cuotas:')
        lb3.place(x=17, y=129)
        self.spn_pres_cant_cuota = Spinbox(window_pres, from_=1, to=99)
        self.spn_pres_cant_cuota.place(x=140, y=129, width=50)
        lb4 = Label(window_pres, text='Cuotas fijas?:')
        lb4.place(x=17, y=167)
        rd_si = Radiobutton(window_pres, text='Si', variable=self.result_cred, value=1,
                    command= lambda: self.visible_cred(self.result_cred.get(),
                                     lb5, lb6, 
                                     self.tx_pres_cuota, self.tx_pres_tasa))
        rd_si.place(x=140, y=167)
        rd_no = Radiobutton(window_pres, text='No', variable=self.result_cred, value=2,
                    command= lambda: self.visible_cred(self.result_cred.get(),
                                     lb5, lb6, 
                                     self.tx_pres_cuota, self.tx_pres_tasa))
        rd_no.place(x=185, y=167)
        lb5 = Label(window_pres, text='Importe cuota:')
        lb5.place(x=17, y=205)
        lb6 = Label(window_pres, text='Tasa de interes:')
        self.tx_pres_cuota = Entry(window_pres)
        self.tx_pres_cuota.place(x=140, y=205, width=180)
        
        self.tx_pres_tasa = Entry(window_pres)
        
        btn_cerrar = Button(window_pres, text='Cerrar', command=window_pres.destroy)
        btn_cerrar.place(x=240, y=243, width=80)
        btn_generar = Button(window_pres, text='Generar', 
                            command=lambda: self.nuevo_prestamo(window_pres))
        btn_generar.place(x=140, y=243, width=80)

        app_width = 330
        app_height = 280 
        screen_width = window_pres.winfo_screenwidth()
        screen_height = window_pres.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        window_pres.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        window_pres.attributes('-toolwindow',-1)
        window_pres.resizable(0,0)    
        window_pres.title('Credito - prestamo')
        window_pres.grab_set()
        window_pres.focus_set()
        window_pres.wait_window()
    

    
    def nuevo_prestamo(self, ventana):
        
        """
        Función que genera prestamo.
        """

        try:
            
            if self.result_cred.get() == 1:

                cant_cuotas = int(self.spn_pres_cant_cuota.get())
                valor_cuota = float(self.tx_pres_cuota.get())
            
            
                valor_total = cant_cuotas * valor_cuota 
            

                self.contabilidad.genera_prestamo(ventana,
                                                self.tx_pres_fecha.get(),
                                                self.tx_pres_descrip.get(),
                                                self.spn_pres_cant_cuota.get(),
                                                self.tx_pres_cuota.get(),
                                                self.tx_pres_imp_total.get(),
                                                valor_total)
                for row in self.tv_ingresos.get_children():
                    self.tv_ingresos.delete(row)
                self.contabilidad.visualizar_treeview(self.tv_ingresos, 'Ingreso')
                for row in self.tv_gastos.get_children():
                    self.tv_gastos.delete(row)
                self.contabilidad.visualizar_treeview(self.tv_gastos, 'Gasto')
            
            else:
                #Genera tasa de interes.
                importe_prestamo = float(self.tx_pres_imp_total.get())
                tasa_interes = float(self.tx_pres_tasa.get())
                interes = importe_prestamo * tasa_interes / 100
                importe_prestamo = importe_prestamo + interes
                #Genera importe cuotas.
                cantidad_cuotas = int(self.spn_pres_cant_cuota.get())
                valor_cuota = importe_prestamo / cantidad_cuotas
                valor_cuota = round(valor_cuota, 2)
                #Llama a función.
                self.contabilidad.genera_prestamo(ventana,
                                                self.tx_pres_fecha.get(),
                                                self.tx_pres_descrip.get(),
                                                self.spn_pres_cant_cuota.get(),
                                                valor_cuota,
                                                self.tx_pres_imp_total.get(),
                                                importe_prestamo)
                for row in self.tv_ingresos.get_children():
                    self.tv_ingresos.delete(row)
                self.contabilidad.visualizar_treeview(self.tv_ingresos, 'Ingreso')
                for row in self.tv_gastos.get_children():
                    self.tv_gastos.delete(row)
                self.contabilidad.visualizar_treeview(self.tv_gastos, 'Gasto')

        except ZeroDivisionError:
            messagebox.showerror(title='Error', message='Cuotas no pueden ser igual a cero.')

        except ValueError:
            messagebox.showerror(title='Error', message='Se ingreso un valor con formato incorrecto.')
        

    def visible_cred(cls, value, obj1, obj2, obj3, obj4):

        """
        Funcion que permite al formulario prestamo, distinguir entre
        cuotas con tasa de interes y fijas
        """
        if value == 1:
            obj1.place(x=17, y=205)
            obj3.place(x=140, y=205, width=180)
            obj2.place_forget()
            obj4.place_forget()
        elif value == 2:
            obj1.place_forget()
            obj3.place_forget()
            obj2.place(x=17, y=205)
            obj4.place(x=140, y=205, width=180)


    def frm_vis_prestamo(self):
        
        """
        Formulario para visualizar registros tipo prestamo. 
        """

        self.window_vpre = Toplevel()
        self.window_vpre.title('Prestamo')

        lb0 = Label(self.window_vpre, text='Fecha:')
        lb0.place(x=17, y=15)
        self.tx_vp_fecha = Entry(self.window_vpre)
        self.tx_vp_fecha.place(x=67, y=15, width= 80)
        
        ruta = Image.open('recursos/imagenes/busca.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_busca = ImageTk.PhotoImage(ruta)
        btn_vp_busca = Button(self.window_vpre, 
                              image=img_busca,
                              command=self.bsc_prestamo)
        btn_vp_busca.place(x=168, y=10, width=30, height=30)

        ruta = Image.open('recursos/imagenes/borrar.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_borra = ImageTk.PhotoImage(ruta)
        btn_vp_del = Button(self.window_vpre, image=img_borra,
                            command=self.borra_prestamo)
        btn_vp_del.place(x=212, y=10, width=30, height=30)

        lb1 = Label(self.window_vpre, text='Descripción:')
        lb1.place(x=17, y=53)
        self.tx_vp_descrip = Entry(self.window_vpre)
        self.tx_vp_descrip.place(x=96, y=53, width=344)

        lb2 = Label(self.window_vpre, text='Cant. Cuotas:')
        lb2.place(x=17, y=91)
        self.tx_vp_ccuota = Entry(self.window_vpre)
        self.tx_vp_ccuota.place(x=96, y=91, width=50)
        lb3 = Label(self.window_vpre, text='Importe cuotas:')
        lb3.place(x=160, y=91)
        self.tx_vp_impcuota = Entry(self.window_vpre)
        self.tx_vp_impcuota.place(x=260, y=91, width=180)

        lb4 = Label(self.window_vpre, text='Importe solicitado:')
        lb4.place(x=17, y=129)
        self.tx_vp_impsol = Entry(self.window_vpre)
        self.tx_vp_impsol.place(x=130, y=129, width=310)

        lb5 = Label(self.window_vpre, text='Importe a devolver:')
        lb5.place(x=17, y=167)
        self.tx_vp_impdev = Entry(self.window_vpre)
        self.tx_vp_impdev.place(x=130, y=167, width=310)

        btn_cerrar = Button(self.window_vpre, text='Cerrar', 
                            command=self.window_vpre.destroy)
        btn_cerrar.place(x=360, y=205, width=80)

        app_width = 450
        app_height = 240 
        screen_width = self.window_vpre.winfo_screenwidth()
        screen_height = self.window_vpre.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.window_vpre.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.window_vpre.attributes('-toolwindow',-1)
        self.window_vpre.resizable(0, 0)
        self.window_vpre.grab_set()
        self.window_vpre.focus_set()
        self.window_vpre.wait_window()


    
    def borra_prestamo(self):

        """
        Elimina un registro de tipo prestamo.
        """

        self.contabilidad.del_prestamo(self.id_prestamo, self.window_vpre)
        
        for row in self.tv_ingresos.get_children():
            self.tv_ingresos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_ingresos,'Ingreso')
        for row in self.tv_gastos.get_children():
                self.tv_gastos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_gastos,'Gasto')


    def bsc_prestamo(self):

        """
        Ventana de busqueda para registros de tipo prestamo.
        """

        #Ventana
        window_bscpres = Toplevel()
        frm_tv = Frame(window_bscpres)
        frm_tv.place(x=1, y=1, width=300, height=100)
        #Barra lateral
        scr_v_pres = Scrollbar(frm_tv, orient=VERTICAL)
        scr_v_pres.place(x=280, y=1, height=100)
        #Treeview
        self.tv_prestamo = Treeview(frm_tv, 
                                   selectmode='browse',
                                   yscrollcommand=scr_v_pres.set)
        self.tv_prestamo.place(x=1, y=1, width=280, height=100)
        self.tv_prestamo['columns'] = ('fecha', 'descripcion', 'importe')
        self.tv_prestamo.column('#0', width=0, stretch=False)
        self.tv_prestamo.column('fecha', width=90, minwidth=60)
        self.tv_prestamo.column('descripcion', width=90, minwidth=60)
        self.tv_prestamo.column('importe', width=90, minwidth=60)
        self.tv_prestamo.heading('#0', text='')
        self.tv_prestamo.heading('fecha', text='Fecha')
        self.tv_prestamo.heading('descripcion', text='Descripción')
        self.tv_prestamo.heading('importe', text='Importe')
        
        scr_v_pres.config(command=self.tv_prestamo.yview)
        
        self.contabilidad.vis_tv_prestamo(self.tv_prestamo)
        self.tv_prestamo.bind("<<TreeviewSelect>>", self.identificar_prestamo)
        
        btn_aceptar = Button(window_bscpres, 
                            text='Aceptar', 
                            command= lambda: self.vis_pres(window_bscpres))
        btn_aceptar.place(x=210, y=110, width=80)
        
        app_width = 300
        app_height = 150 
        screen_width = window_bscpres.winfo_screenwidth()
        screen_height = window_bscpres.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        window_bscpres.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        window_bscpres.attributes('-toolwindow',-1)
        window_bscpres.resizable(0,0)
        window_bscpres.title('Buscar')
        
        window_bscpres.grab_set()
        window_bscpres.focus_set()
        window_bscpres.wait_window()


    
    def vis_pres(self, ventana):
        
        """
        Visualiza los registros de un prestamo.

        """
        try:
            self.tx_vp_fecha.delete(0,END)
            self.tx_vp_fecha.insert(0, self.contabilidad.vis_registro_prestamo(
                                    self.id_prestamo, 
                                    'fecha'))  

            self.tx_vp_descrip.delete(0, END)
            self.tx_vp_descrip.insert(0, self.contabilidad.vis_registro_prestamo(
                                     self.id_prestamo, 
                                     'descrip'))    

            self.tx_vp_ccuota.delete(0, END)
            self.tx_vp_ccuota.insert(0, self.contabilidad.vis_registro_prestamo(
                                     self.id_prestamo, 
                                     'cuota'))    

            self.tx_vp_impcuota.delete(0, END)
            self.tx_vp_impcuota.insert(0, self.contabilidad.vis_registro_prestamo(
                                    self.id_prestamo, 
                                    'imp_cuota'))                      
            self.tx_vp_impsol.delete(0, END)
            self.tx_vp_impsol.insert(0, self.contabilidad.vis_registro_prestamo(
                                    self.id_prestamo, 
                                    'imp_tot'))  

            self.tx_vp_impdev.delete(0, END)
            self.tx_vp_impdev.insert(0, self.contabilidad.vis_registro_prestamo(
                                    self.id_prestamo, 
                                    'imp_dev')) 

            ventana.destroy()     

        except TypeError:
            pass                                                                                  


    def form_tarjeta(self):

        """
        #Formulario para crear gastos con tarjeta de credito.
        """
    
        self.window_tc = Toplevel()

        self.window_tc.resizable(0,0)
        self.window_tc.title('Gasto tarjeta de credito')

        self.radio_variable = IntVar()
        self.radio_variable.set(0)

        lb0 = Label(self.window_tc, text='Fecha')
        lb0.place(x=17, y=15)
        self.tx_tc_fecha = Entry(self.window_tc)
        self.tx_tc_fecha.place(x=101, y=15, width=121)
        
        lb1 = Label(self.window_tc, text='Tipo de gasto:')
        lb1.place(x=17, y=58)
        valores = self.configuracion.show_par('Gastos')
        self.cb_tc_tipo = Combobox(self.window_tc, values=valores, state='readonly')
        self.cb_tc_tipo.place(x=101, y=58, width=120)
        lb2 = Label(self.window_tc, text='Descripción:')
        lb2.place(x=243, y=58)
        self.tx_tc_descrip = Entry(self.window_tc)
        self.tx_tc_descrip.place(x=321, y=58, width=180)

        lb3 = Label(self.window_tc, text='Importe:')
        lb3.place(x=17, y=99)
        self.tx_tc_importe = Entry(self.window_tc)
        self.tx_tc_importe.place(x=101, y=99, width=180)
        lb4 = Label(self.window_tc, text='Cant. Cuotas')
        lb4.place(x=322, y=99)
        self.cb_tc_cuotas = Combobox(self.window_tc, values=ConfigApp.CUOTAS,
                                     state='readonly')
        self.cb_tc_cuotas.place(x=438, y =99, width=62)
        
        lb5 = Label(self.window_tc, text='Con interes?')
        lb5.place(x=17, y=144)
        rd_si = Radiobutton(self.window_tc, text='Si', variable=self.radio_variable, 
                            value=0, command= lambda: self.inhabilita_entry(self.tx_tc_tasa))
        rd_si.place(x=101, y=144)
        rd_no = Radiobutton(self.window_tc, text='No', variable=self.radio_variable, 
                            value=1, command= lambda: self.inhabilita_entry(self.tx_tc_tasa))
        rd_no.place(x=101, y=168)
        lb6 = Label(self.window_tc, text='Tasa de interes:')
        lb6.place(x=158, y=144)
        self.tx_tc_tasa = Entry(self.window_tc)
        self.tx_tc_tasa.place(x=260, y=144)
        
        btn_guardar = Button(self.window_tc, text='Guardar', command=self.crea_tcredito)
        btn_guardar.place(x=423, y=187, width=80)
        btn_cerrar = Button(self.window_tc, text='Cerrar', command=self.window_tc.destroy)
        btn_cerrar.place(x=322, y=187, width=80)

        app_width = 520
        app_height = 230 
        screen_width = self.window_tc.winfo_screenwidth()
        screen_height = self.window_tc.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.window_tc.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.window_tc.attributes('-toolwindow',-1)
        self.window_tc.grab_set()
        self.window_tc.focus_set()
        self.window_tc.wait_window()


    def inhabilita_entry(self, obj1):

        """
        Inhabilita el entry tasa de interes, del formulario tarjeta de crédito.
        """
        var = self.radio_variable.get()

        if var == 0:
            obj1['state'] = NORMAL
        elif var == 1:
            obj1.delete(0, END)
            obj1['state'] = DISABLED


    def crea_tcredito(self):

        """
        Crea un registro de tipo "tarjeta de crédito".
        """
        
        self.contabilidad.gasto_tarjeta(self.window_tc,
                                        self.tx_tc_importe.get(),
                                        self.cb_tc_tipo.get(),
                                        self.tx_tc_descrip.get(),
                                        self.tx_tc_fecha.get(),
                                        self.cb_tc_cuotas.get(),
                                        self.radio_variable.get(),
                                        self.tx_tc_tasa.get()
                                        )

        for row in self.tv_gastos.get_children():
            self.tv_gastos.delete(row)   

        self.contabilidad.visualizar_treeview(self.tv_gastos,'Gasto')
    

    def visua_tc(self):
        
        """
        Formulario vara visualizar gastos en tarjeta de credito.
        """

        self.window_vtc = Toplevel()

        lb0 = Label(self.window_vtc, text='Fecha:')
        lb0.place(x=17, y=15)
        self.tx_vstc_fecha = Entry(self.window_vtc)
        self.tx_vstc_fecha.place(x=62, y=15, width=96)
        
        ruta = Image.open('recursos/imagenes/busca.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_buscar = ImageTk.PhotoImage(ruta)
        btn_buscar = Button(self.window_vtc, 
                            image=img_buscar, 
                            command=self.bsc_tc)
        btn_buscar.place(x=176, y=10, width=30, height=30)

        ruta = Image.open('recursos/imagenes/borrar.jpg')
        ruta = ruta.resize((25,25), Image.ANTIALIAS)
        img_borra = ImageTk.PhotoImage(ruta)
        btn_del = Button(self.window_vtc, image=img_borra,
                         command=self.borra_tc)
        btn_del.place(x=212, y=10, width=30, height=30)
        
        lb1 = Label(self.window_vtc,text='Descripción')
        lb1.place(x=17, y=58)
        self.tx_vstc_descrip = Entry(self.window_vtc)
        self.tx_vstc_descrip.place(x=112, y=58, width=283)
        lb2 = Label(self.window_vtc,text='Cant. Cuotas:')
        lb2.place(x=17, y=99)
        self.tx_vstc_cuota = Entry(self.window_vtc)
        self.tx_vstc_cuota.place(x=112, y=99, width=56)
        lb3 = Label(self.window_vtc,text='Imp. Cuota:')
        lb3.place(x=192, y=99)
        self.tx_vstc_valcuota = Entry(self.window_vtc)
        self.tx_vstc_valcuota.place(x=279, y=99, width=116)
        lb4 = Label(self.window_vtc,text='Importe Total:')
        lb4.place(x=17, y=140)
        self.tx_vstc_imp = Entry(self.window_vtc)
        self.tx_vstc_imp.place(x=112, y=140, width=140)
        btn_cerrar = Button(self.window_vtc, text='Cerrar', command=self.window_vtc.destroy)
        btn_cerrar.place(x=315, y=181, width=80)

        app_width = 410
        app_height = 220 
        screen_width = self.window_vtc.winfo_screenwidth()
        screen_height = self.window_vtc.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        self.window_vtc.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        self.window_vtc.attributes('-toolwindow',-1)
        self.window_vtc.resizable(0,0)
        self.window_vtc.title('Tarjeta de crédito')
        self.window_vtc.grab_set()
        self.window_vtc.focus_set()
        self.window_vtc.wait_window()


    def borra_tc(self):

        """
        Elimina un registro de tarjeta de credito
        """

        self.contabilidad.del_tc(self.id_tc, self.window_vtc)
    
        for row in self.tv_ingresos.get_children():
            self.tv_ingresos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_ingresos,'Ingreso')
        for row in self.tv_gastos.get_children():
            self.tv_gastos.delete(row)
        self.contabilidad.visualizar_treeview(self.tv_gastos,'Gasto')


    def vis_tc(self, ventana):

        """
        Función que permite seleccionar el gasto en tarjeta de crédito.
        """
        try:
            self.tx_vstc_fecha.delete(0,END)
            self.tx_vstc_fecha.insert(0, 
                                      self.contabilidad.visualizar_registro_tc(self.id_tc, 'fecha'))  
            self.tx_vstc_descrip.delete(0,END)
            self.tx_vstc_descrip.insert(0, 
                                    self.contabilidad.visualizar_registro_tc(self.id_tc, 'descrip')) 
            self.tx_vstc_cuota.delete(0,END)
            self.tx_vstc_cuota.insert(0, 
                                      self.contabilidad.visualizar_registro_tc(self.id_tc, 'cuota'))
            self.tx_vstc_valcuota.delete(0,END)
            self.tx_vstc_valcuota.insert(0, 
                                         self.contabilidad.visualizar_registro_tc(self.id_tc, 'imp_cuota'))
            self.tx_vstc_imp.delete(0,END)
            self.tx_vstc_imp.insert(0, 
                                    self.contabilidad.visualizar_registro_tc(self.id_tc, 'imp_tot'))  

            ventana.destroy()  

        except TypeError:
            pass     


    def bsc_tc(self):

        """
        Formulario de busqueda para tarjeta de credito.
        """

        #Ventana
        window_bsc = Toplevel()
        frm_tv = Frame(window_bsc)
        frm_tv.place(x=1, y=1, width=300, height=100)
        #Barra lateral
        scr_v_tc = Scrollbar(frm_tv, orient=VERTICAL)
        scr_v_tc.place(x=280, y=1, height=100)
        #Treeview
        self.tv_tarjeta = Treeview(frm_tv, 
                              selectmode='browse',
                              yscrollcommand=scr_v_tc.set)
        self.tv_tarjeta.place(x=1, y=1, width=280, height=100)
        self.tv_tarjeta['columns'] = ('fecha', 'descripcion', 'importe')
        self.tv_tarjeta.column('#0', width=0, stretch=False)
        self.tv_tarjeta.column('fecha', width=90, minwidth=60)
        self.tv_tarjeta.column('descripcion', width=90, minwidth=60)
        self.tv_tarjeta.column('importe', width=90, minwidth=60)

        self.tv_tarjeta.heading('#0', text='')
        self.tv_tarjeta.heading('fecha', text='Fecha')
        self.tv_tarjeta.heading('descripcion', text='Descripción')
        self.tv_tarjeta.heading('importe', text='Importe')

        scr_v_tc.config(command=self.tv_tarjeta.yview)

        self.contabilidad.vis_tv_tarjeta(self.tv_tarjeta)

        self.tv_tarjeta.bind("<<TreeviewSelect>>", self.identificar_tc)

        btn_aceptar = Button(window_bsc, 
                            text='Aceptar', 
                            command= lambda: self.vis_tc(window_bsc))
        btn_aceptar.place(x=210, y=110, width=80)

        app_width = 300
        app_height = 150 
        screen_width = window_bsc.winfo_screenwidth()
        screen_height = window_bsc.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        window_bsc.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        window_bsc.attributes('-toolwindow',-1)
        window_bsc.resizable(0,0)
        window_bsc.title('Buscar')
        window_bsc.grab_set()
        window_bsc.focus_set()
        window_bsc.wait_window()


    def frm_totales(self):

        """
        Formulario que trae las estadisticas: dinero disponible, total ahorro, gastos mensuales.
        """

        self.contabilidad.estadisticas()

        total_ahorros = self.contabilidad.ahorros
        total_ingresos = self.contabilidad.dinero_disp
        total_gastos = self.contabilidad.gastos

        win_totales = Toplevel()

        lb0 = Label(win_totales, text='Dinero disponible:')
        lb0.place(x=17, y=15)
        lb_ingreso = Label(win_totales, text=f'${total_ingresos}')
        lb_ingreso.place(x=130, y=15)
        lb1 = Label(win_totales, text = 'Total ahorros:')
        lb1.place(x=17, y=45)
        lb_ahorro = Label(win_totales, text=f'${total_ahorros}')
        lb_ahorro.place(x=130, y=45)
        lb2 = Label(win_totales, text='Gastos mensuales:')
        lb2.place(x=17, y=75)
        lb_gastos = Label(win_totales, text=f'${total_gastos}')
        lb_gastos.place(x=130, y= 75)

        btn_cerrar = Button(win_totales, text='Cerrar', command=win_totales.destroy)
        btn_cerrar.place(x=118, y= 105, width=80)
        
        app_width = 210
        app_height = 140 
        screen_width = win_totales.winfo_screenwidth()
        screen_height = win_totales.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        win_totales.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        win_totales.attributes('-toolwindow',-1)
        win_totales.resizable(0,0)
        win_totales.title('Estadisticas')
        win_totales.grab_set()
        win_totales.focus_set()
        win_totales.wait_window()


    def par_divisa(self):

        """
        Formulario para visualizar el valor de las divisas extrajeras.
        """
    
        window = Toplevel()
        window.title('Divisas extranjeras.')

        self.contabilidad.dolarblue_venta = self.contabilidad.obtiene_valor_divisa('dbventa')
        self.contabilidad.dolarblue_compra = self.contabilidad.obtiene_valor_divisa('dbcompra')
        self.contabilidad.euroblue_venta = self.contabilidad.obtiene_valor_divisa('ebventa')
        self.contabilidad.euroblue_compra = self.contabilidad.obtiene_valor_divisa('ebcompra')

        if self.contabilidad.dolarblue_venta == None:
            dbventa = 0
        else:
            dbventa = self.contabilidad.dolarblue_venta
        if self.contabilidad.dolarblue_compra == None:
            dbcompra = 0
        else:
            dbcompra = self.contabilidad.dolarblue_compra
        if self.contabilidad.euroblue_venta == None:
            ebventa = 0
        else:
            ebventa = self.contabilidad.euroblue_venta
        if self.contabilidad.euroblue_compra == None:
            ebcompra = 0
        else:
            ebcompra = self.contabilidad.euroblue_compra
        
        lb0 = Label(window, text='Dólar compra:')
        lb0.place(x=17, y=15)
        self.tx_dolar_comp = Entry(window)
        self.tx_dolar_comp.place(x=109, y=15, width=92)
        self.tx_dolar_comp.insert(0, dbcompra)
        lb1 = Label(window, text='Dólar venta:')
        lb1.place(x=228, y=15)
        self.tx_dolar_venta = Entry(window)
        self.tx_dolar_venta.place(x=320, y=15, width=92)
        self.tx_dolar_venta.insert(0, dbventa)

        lb2 = Label(window, text='Euro compra:')
        lb2.place(x=17, y=56)
        self.tx_euro_comp = Entry(window)
        self.tx_euro_comp.place(x=109, y=56, width=92)
        self.tx_euro_comp.insert(0, ebcompra)
        lb3 = Label(window, text='Euro venta:')
        lb3.place(x=228, y=56)
        self.tx_euro_venta = Entry(window)
        self.tx_euro_venta.place(x=320, y=56, width=92)
        self.tx_euro_venta.insert(0, ebventa)

        btn_cerrar = Button(window, text='Cerrar', command=window.destroy)
        btn_cerrar.place(x=122, y=97, width=90)
        btn_actualizar = Button(window, text='Obtener valores', command=self.actualiza_divisa)
        btn_actualizar.place(x=227, y=97, width=90)
        btn_guardar = Button(window, text='Guardar',
                            command=lambda: self.guardar_divisa(window))
        btn_guardar.place(x=332, y=97, width=90)

        app_width = 435
        app_height = 135 
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        window.attributes('-toolwindow',-1)
        window.resizable(0,0)
        window.grab_set()
        window.focus_set()
        window.wait_window()


    def guardar_divisa(self, ventana):

        """
        Guarda el valor de la divisa extranjera y cierra el formulario.
        """
        try:
            dolar_compra = float(self.tx_dolar_comp.get())
            dolar_venta = float(self.tx_dolar_venta.get())
            euro_compra = float(self.tx_euro_comp.get())
            euro_venta = float(self.tx_euro_venta.get())

            self.contabilidad.valor_divisas_manual(dolar_compra,'dbcompra')
            self.contabilidad.valor_divisas_manual(dolar_venta,'dbventa')
            self.contabilidad.valor_divisas_manual(euro_compra,'ebcompra')
            self.contabilidad.valor_divisas_manual(euro_venta,'ebventa')

            messagebox.showinfo(title='Información', message='Se actualizaron los valores correctamente.')

        except ValueError:

            messagebox.showerror(title='Error', message='Formato de divisa incorrecto.')

    def actualiza_divisa(self):

        """
        Actualiza el valor de las divisas en el formulario.
        """
        self.contabilidad.valor_divisas_web()

        self.tx_dolar_comp.delete(0, END)
        self.tx_dolar_comp.insert(0, self.contabilidad.dolarblue_compra)
        self.tx_dolar_venta.delete(0, END)
        self.tx_dolar_venta.insert(0, self.contabilidad.dolarblue_venta)
        self.tx_euro_comp.delete(0, END)
        self.tx_euro_comp.insert(0, self.contabilidad.euroblue_compra)
        self.tx_euro_venta.delete(0, END)
        self.tx_euro_venta.insert(0, self.contabilidad.euroblue_venta)

        messagebox.showinfo(title='Información', message='Se actualizaron los valores correctamente.')

    
    def frm_parametros (self):

        """
        Formulario para crear parametros para los registros de tipo 'Ingreso / Gasto'.
        """

        ventana = Toplevel()
        ventana.title('Alta parametro')

        lista = ['Ingreso', 'Gastos']

        lb0 = Label(ventana, text='Tipo de parametro:')
        lb0.place(x=17, y=15)
        cmb_tipo = Combobox(ventana, values=lista, state='readonly')
        cmb_tipo.place(x=127, y=15, width=180)

        lb1 = Label(ventana, text='Nombre')
        lb1.place(x=17, y=54)
        txt_nombre = Entry(ventana)
        txt_nombre.place(x=127, y=54, width=180)           

        btn_guardar = Button(ventana, text='Guardar', 
                             command = lambda: self.configuracion.crea_parametro(
                                ventana, cmb_tipo.get(),txt_nombre.get()))
        btn_guardar.place(x=228, y=93, width=80)
        btn_cerrar = Button(ventana, text='Cerrar', command=ventana.destroy)
        btn_cerrar.place(x=127, y=93, width=80)

        app_width = 320
        app_height = 130 
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)
        ventana.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        ventana.attributes('-toolwindow',-1)
        ventana.resizable(0,0)
        ventana.grab_set()
        ventana.focus_set()
        ventana.wait_window()