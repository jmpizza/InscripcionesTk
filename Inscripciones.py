# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import re
from tkinter import messagebox
from datetime import date
from pathlib import Path
import signal

PATH = str((Path(__file__).resolve()).parent)

class Inscripciones:
    def __init__(self, master=None):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        # Ventana principal
        self.db_name = PATH + '/db/Inscripciones.db'
        self.win = tk.Tk(master)
        self.win.configure(background='#f7f9fd', height=600, width=800)
        self.win.geometry('800x600')
        self.win.resizable(False, False)
        self.win.title('Inscripciones de Materias y Cursos')
        self.win.iconbitmap(PATH + '/img/penguin.ico')
        window_width = 800
        window_height = 600
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.win.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name='frm_1')
        self.frm_1.configure(background='#f7f9fd', height=600, width=800)
        self.lblNoInscripcion = ttk.Label(self.frm_1, name='lblnoinscripcion')
        self.lblNoInscripcion.configure(background='#f7f9fd',font='{Arial} 11 {bold}',
                                        justify='left',state='normal',
                                        takefocus=False,text='No.Inscripción')
        
        self.entryStyle = ttk.Style()
        self.entryStyle.configure('TEntry', background='#000000',font=('Arial', 11, 'bold'))
        self.entryStyle.map('TEntry',
                            foreground=[('disabled', '#000000'), ('!disabled', '#000000')], 
                            fieldbackground=[('disabled', '#ffffff'), ('!disabled', '#ffffff')])
        
        self.cmbStyle = ttk.Style()
        self.cmbStyle.configure('TCombobox', background='#ffffff',font=('Arial', 11, 'bold'))
        self.cmbStyle.map('TCombobox',
                          foreground=[('disabled', '#000000'), ('!disabled', '#000000')], 
                          fieldbackground=[('disabled', '#ffffff'), ('!disabled', '#ffffff')])
        
         #Label No. Inscripción
        self.lblNoInscripcion.place(anchor='nw', x=680, y=20)
        #Combobox No_Inscripción
        self.num_Inscripcion = ttk.Combobox(self.frm_1, name='num_inscripcion')
        self.num_Inscripcion.place(anchor='nw', width=100, x=682, y=42)
        self.num_Inscripcion.bind('<KeyRelease>', self.num_inscripcion_update)
        self.num_Inscripcion.bind('<Button-1>', self.num_inscripcion_update)
        self.num_Inscripcion.bind('<<ComboboxSelected>>', self.rellenar_id_alumno)
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name='lblfecha')
        self.lblFecha.configure(background='#f7f9fd', text='Fecha:')
        self.lblFecha.place(anchor='nw', x=630, y=80)
        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name='fecha')
        self.fecha.configure(justify='center')
        self.fecha.place(anchor='nw', width=100, x=680, y=80)
        self.fecha.bind('<KeyRelease>', self.date_verification)
        self.fecha.bind('<ButtonRelease-1>', self.date_verification)
        self.fecha.bind('<Button-1>', self.date_verification)
        
        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name='lblidalumno')
        self.lblIdAlumno.configure(background='#f7f9fd', text='Id Alumno:')
        self.lblIdAlumno.place(anchor='nw', x=20, y=80)
        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name='cmbx_id_alumno')
        self.cmbx_Id_Alumno.place(anchor='nw', width=112, x=100, y=80)
        self.cmbx_Id_Alumno.bind('<KeyRelease>', self.id_update)
        self.cmbx_Id_Alumno.bind('<Button-1>', self.id_update)
        self.cmbx_Id_Alumno.bind('<<ComboboxSelected>>', self.rellenar_num_inscripcion)
        
        #Label Alumno
        self.lblNombres = ttk.Label(self.frm_1, name='lblnombres')
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor='nw', x=20, y=130)
        #Entry Alumno
        self.nombres = ttk.Entry(self.frm_1, name='nombres')
        self.nombres.place(anchor='nw', width=200, x=100, y=130)
        self.nombres.config(state="disabled")
        self.nombres.bind('<Button-1>', self.entry_bloqueado)
        
        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name='lblapellidos')
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor='nw', x=400, y=130)
        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name='apellidos')
        self.apellidos.place(anchor='nw', width=200, x=485, y=130)
        self.apellidos.config(state="disabled")
        self.apellidos.bind('<Button-1>', self.entry_bloqueado)

        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name='lblidcurso')
        self.lblIdCurso.configure(background='#f7f9fd',state='normal',text='Id Curso:')
        self.lblIdCurso.place(anchor='nw', x=20, y=185)
        #Combobox Curso
        self.cmbx_Id_Curso = ttk.Combobox(self.frm_1, name='cmbx_id_curso')
        self.cmbx_Id_Curso.place(anchor='nw', width=166, x=100, y=185)
        self.cmbx_Id_Curso.bind('<KeyRelease>', self.combobox_curso_events)
        self.cmbx_Id_Curso.bind('<Button-1>', self.combobox_curso_events)
        self.cmbx_Id_Curso.bind('<<ComboboxSelected>>', self.rellenar_curso)
        
        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name='lbldsccurso')
        self.lblDscCurso.configure(background='#f7f9fd',state='normal',text='Curso:')
        self.lblDscCurso.place(anchor='nw', x=275, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name='descripc_curso')
        self.descripc_Curso.configure(justify='left', width=166)
        self.descripc_Curso.place(anchor='nw', width=300, x=325, y=185)
        self.descripc_Curso.config(state="disabled")
        self.descripc_Curso.bind('<Button-1>', self.entry_bloqueado)
        
        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name='label3')
        self.lblHorario.configure(background='#f7f9fd',state='normal',text='Hora:')
        self.lblHorario.place(anchor='nw', x=635, y=185)
        #Entry del Horario
        self.horario = ttk.Entry(self.frm_1, name='entry3')
        self.horario.configure(justify='left', width=166)
        self.horario.place(anchor='nw', width=100, x=680, y=185)

        ''' Botones  de la Aplicación'''
        #Botón Style
        self.btnStyle = ttk.Style()
        self.btnStyle.configure('TButton',
                                background='#f7f9fd',
                                font=('Arial', 11, 'bold'),
                                relief='raised',
                                padding=(2,5))
        self.btnStyle.map('TButton',
                        foreground=[('!disabled', '#0000ff'), ('active', '#00ffff'), ('disabled', '#a9a9a9')],  
                        background=[('!disabled', '#ffffff'), ('active', '#00ffff'), ('disabled', '#dcdcdc')], 
                        relief=[('disabled', 'flat')]) 
        
        #Boton Buscar
        self.btnBuscar = ttk.Button(self.frm_1, name='btnbuscar')
        self.btnBuscar.configure(text='Buscar')
        self.btnBuscar.place(anchor='nw', x=150, y=260)
        self.btnBuscar.bind('<Button-1>', self.mostrar_busqueda)
        
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name='btnguardar')
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor='nw', x=250, y=260)
        self.btnGuardar.bind('<Button-1>', self.guardar)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name='btneditar')
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor='nw', x=350, y=260)
        self.btnEditar.bind("<<TreeviewSelect>>", self.seleccion_treeview)
        self.btnEditar.bind('<Button-1>', self.editar)
        # Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name='btneliminar')
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor='nw', x=450, y=260)
        self.btnEliminar.bind('<Button-1>', self.eliminar_opciones)
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name='btncancelar')
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor='nw', x=550, y=260)
        self.btnCancelar.bind('<Button-1>', self.cancelar)
        
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient='horizontal')
        separator1.place(anchor='nw', width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name='tview')
        self.tView.configure(selectmode='extended')
        
        #Columnas del Treeview
        self.tView_cols = ['tV_alumno','tV_curso','tV_descripción','tV_horario']
        self.tView_dcols = ['tV_alumno','tV_curso','tV_descripción','tV_horario']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols, show='headings')
        self.tView.column('tV_alumno',anchor='w',stretch=True,width=200,minwidth=50)
        self.tView.column('tV_curso',anchor='w',stretch=True,width=200,minwidth=50)
        self.tView.column('tV_descripción',anchor='w',stretch=True,width=200,minwidth=50)
        self.tView.column('tV_horario',anchor='w',stretch=True,width=200,minwidth=50)
        
        
        #Cabeceras
        self.tView.heading('tV_alumno', anchor='w', text='Id_Alumno')
        self.tView.heading('tV_curso', anchor='w', text='Id_Curso')
        self.tView.heading('tV_descripción', anchor='w', text='Descripción')
        self.tView.heading('tV_horario', anchor='w', text='Hora')
        self.tView.place(anchor='nw', height=300, width=790, x=4, y=300)
        
        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.frm_1, name='scroll_h')
        self.scroll_H.configure(orient='horizontal')
        self.scroll_H.place(anchor='s', height=12, width=1534, x=15, y=595)
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name='scroll_y')
        self.scroll_Y.configure(orient='vertical')
        self.scroll_Y.place(anchor='s', height=275, width=12, x=790, y=582)
        
        self.frm_1.pack(side='top')
        self.frm_1.pack_propagate(0)

        # Main widget
        self.mainwindow = self.win

    def run(self):
        self.mainwindow.mainloop()

    #Metodos para el manejo de la base de datos
    def run_query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
            final = result.fetchall()
        return final if final else None
                
    def insert_query(self, tabla, filas, valores):
        insert = f'INSERT INTO {tabla} ({", ".join(filas)}) VALUES ({", ".join(map(str, valores))})'
        self.run_query(insert)
    
    def update_query(self, tabla, filas, valores, condicion=None):
        set_clause = ', '.join([f'{fila} = "{valor}"' for fila, valor in zip(filas, valores)])
        update = f'UPDATE {tabla} SET {set_clause} '
        if condicion:
            update += f' WHERE {condicion}'
        try:
            self.run_query(update)
            return True  # La actualización se realizó con éxito
        except Exception as e:
            return False  # La actualización falló

    def delete_query(self, tabla, condicion):
        delete = f'DELETE FROM {tabla} WHERE {condicion}'
        self.run_query(delete)

    def entry_bloqueado(self, _=''):
        messagebox.showinfo(title="Aviso", message="No se puede modificar este campo")

    def date_verification(self, event=''):
        if str(self.fecha['state']) == 'disabled':
            messagebox.showinfo('Aviso', 'No se puede modificar la fecha, para modificarla presione el boton "Cancelar" o termine el proceso')
            return
        fecha = self.fecha.get() 
        if len(fecha) > 10:
            messagebox.showerror('Error', 'La fecha debe tener maximo 10 caracteres')
            fecha = fecha[:10]

        if re.match(r'^([0-9]{3}|[0-9]{2}/[0-9]{3})$', fecha):
            fecha= re.sub(r'([0-9]{2})([0-9])', r'\1/\2', fecha)

        fecha = re.sub(r'[^0-9/]', '', fecha)

        self.fecha.delete(0, tk.END)
        self.fecha.insert(0, fecha)
        
        if len(fecha) == 10 and event == 'Guardar':
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
                messagebox.showerror('Error', 'La fecha debe tener el formato dd/mm/aaaa')
                return None

            day, month, year = map(int, fecha.split('/'))

            try:
                date(year, month, day)
                return f'{year}-{month}-{day}'
            except ValueError:
                messagebox.showerror('Error', 'La fecha ingresada no es valida')
                return None
        elif len(fecha) != 10 and event == 'Guardar':
            messagebox.showerror('Error', 'La fecha debe tener al menos 10 caracteres')
            return None
        
    def id_update(self, _=''):
        if str(self.cmbx_Id_Alumno['state']) == 'disabled':
            messagebox.showinfo('Aviso', 'No se puede modificar el Id_Alumno, para modificarlo presione el boton "Cancelar"')
            return
        id = self.cmbx_Id_Alumno.get().strip()
        id = f'%{id}%'
        ids = self.run_query('SELECT Id_Alumno FROM Alumnos WHERE Id_Alumno LIKE ? ORDER BY Id_Alumno ASC', (id,))
        self.cmbx_Id_Alumno['values'] = ids
        if ids and len(ids) == 1 and len(self.cmbx_Id_Alumno.get().strip()) == len(ids[0][0]):
            self.cmbx_Id_Alumno.set(ids[0][0])
            self.rellenar_num_inscripcion()
            
        else:
            self.num_Inscripcion.config(state="enabled")
            
    def num_inscripcion_update(self, _=''):
        if str(self.num_Inscripcion['state']) == 'disabled':
            messagebox.showinfo('Aviso', 'No se puede modificar el No_Inscripción, para modificarlo presione el boton "Cancelar"')
            return
        num_inscripcion = self.num_Inscripcion.get().strip()
        num_inscripcion = f'%{num_inscripcion}%'
        nums_inscripcion = self.run_query('SELECT DISTINCT No_Inscripción FROM Inscritos WHERE No_Inscripción LIKE ? ORDER BY No_Inscripción ASC', (num_inscripcion,))
        if nums_inscripcion:
            self.num_Inscripcion['values'] = nums_inscripcion
        else:
            self.num_Inscripcion['values'] = []
        if nums_inscripcion and len(nums_inscripcion) == 1 and len(self.num_Inscripcion.get().strip()) == len(str(nums_inscripcion[0][0])):
            self.num_Inscripcion.set(nums_inscripcion[0][0])
            self.rellenar_id_alumno()
        else:
            self.cmbx_Id_Alumno.config(state="enabled")
    
    def rellenar_num_inscripcion(self,_=""):
        id = self.cmbx_Id_Alumno.get().strip()
        num_inscripcion = f"SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?"
        resultado = self.run_query(num_inscripcion, (id,))
        if resultado:
            self.num_Inscripcion.config(state="enabled")
            self.num_Inscripcion.delete(0,"end")
            self.num_Inscripcion.insert(0,resultado[0][0])
            self.num_Inscripcion.config(state="disabled")
        else:
            self.num_Inscripcion.config(state="enabled")
            self.num_Inscripcion.delete(0,"end")
        self.rellenar_apellido()
        self.rellenar_nombre()
    
    def rellenar_id_alumno(self, _=''):
        num_inscripcion = self.num_Inscripcion.get().strip()
        id = f"SELECT Id_Alumno FROM Inscritos WHERE No_Inscripción = ?"
        resultado = self.run_query(id, (num_inscripcion,))
        if resultado:
            self.cmbx_Id_Alumno.config(state="enabled")
            self.cmbx_Id_Alumno.delete(0,"end")
            self.cmbx_Id_Alumno.insert(0,resultado[0][0])
            self.cmbx_Id_Alumno.config(state="disabled")
        self.rellenar_nombre()
        self.rellenar_apellido()
    
    def rellenar_nombre (self, _='',tabla='Alumnos',columna='Nombres',celda='Id_Alumno'):
        id = self.cmbx_Id_Alumno.get().strip()
        nombre = f"SELECT {columna} FROM {tabla} WHERE {celda} = ?"
        resultado = self.run_query(nombre, (id,))
        if resultado:
            self.nombres.config(state="enabled")
            self.nombres.delete(0,"end")
            self.nombres.insert(0,resultado[0][0])
            self.nombres.config(state="disabled")
    
    def rellenar_apellido(self, _='', tabla='Alumnos', columna='Apellidos', celda='Id_Alumno'):
        id = self.cmbx_Id_Alumno.get().strip()
        apellido = f"SELECT {columna} FROM {tabla} WHERE {celda} = ?"
        resultado = self.run_query(apellido, (id,))
        if resultado:
            self.apellidos.config(state="enabled")
            self.apellidos.delete(0, "end")
            self.apellidos.insert(0, resultado[0][0])
            self.apellidos.config(state="disabled")
        
    def combobox_curso_events(self, _=''):
        if str(self.cmbx_Id_Curso['state']) == 'disabled':
            messagebox.showinfo('Aviso', 'No se puede modificar el Id_Curso, para modificarlo presione el boton "Cancelar" o termine el proceso')
            return
        codigos_cursos = [codigo[0] for codigo in self.run_query("SELECT Código_Curso FROM Cursos")]
        self.cmbx_Id_Curso['values'] = codigos_cursos
        id = self.cmbx_Id_Curso.get().strip()
        id = f'%{id}%'
        ids = self.run_query('SELECT Código_Curso FROM Cursos WHERE Código_Curso LIKE ?', (id,))
        self.cmbx_Id_Curso['values'] = ids
        if ids and len(ids) == 1 and len(self.cmbx_Id_Curso.get().strip()) == 7:
            self.cmbx_Id_Curso.set(ids[0][0])
            self.rellenar_curso()
    
    def rellenar_curso(self, event=None):
        codigo_curso = self.cmbx_Id_Curso.get()
        descripcion_curso = self.run_query("SELECT Descrip_Curso FROM Cursos WHERE Código_Curso = ?", (codigo_curso,))
        if descripcion_curso:
            self.descripc_Curso.config(state="enabled")
            self.descripc_Curso.delete(0, "end")
            self.descripc_Curso.insert(0, descripcion_curso[0][0])
            self.descripc_Curso.config(state="disabled")
    
    def limpiar_campos_de_proceso(self):
        self.fecha.config(state="enabled")
        self.fecha.delete(0, tk.END)
        self.cmbx_Id_Curso.config(state="enabled")
        self.cmbx_Id_Curso.set('')
        self.descripc_Curso.config(state="enabled")
        self.descripc_Curso.delete(0, tk.END)
        self.descripc_Curso.config(state="disabled")
        self.horario.delete(0, tk.END)
        self.num_Inscripcion.config(state="enabled")
        self.btnBuscar.config(state="enabled")
        self.btnGuardar.config(state="enabled")
        self.btnEditar.config(state="enabled")
        self.btnEliminar.config(state="enabled")
    
    def guardar(self, _=''):
        if str(self.btnGuardar['state']) == 'disabled':
            messagebox.showinfo('Aviso', 'Se esta llevando a cabo un proceso, para salir presione el botón "Cancelar" o termine el proceso')
            return
        if str(self.fecha['state']) == 'disabled':
            self.cmbx_Id_Alumno.config(state="enabled")
            id = self.cmbx_Id_Alumno.get().strip()
            self.cmbx_Id_Alumno.config(state="disabled")
            self.cmbx_Id_Curso.config(state="enabled")
            codigo_curso = self.cmbx_Id_Curso.get().strip()
            nuevohorario = self.horario.get()
            self.update_query('Inscritos', ['Horario'], [nuevohorario], f'Id_Alumno = "{id}" AND Código_Curso = "{codigo_curso}"')
            self.limpiar_campos_de_proceso()
            messagebox.showinfo('Información', 'Cambios guardados con éxito')
            self.mostrar_busqueda()
            return
        
        fecha = self.date_verification('Guardar')
        if fecha is None:
            return
        fecha = "'" + fecha + "'" 
        codigo_curso = self.cmbx_Id_Curso.get()
        horas = self.horario.get()
        if not horas:
            horas = '""'
        id_alumno = self.cmbx_Id_Alumno.get().strip()
        if not id_alumno or not codigo_curso:
            messagebox.showerror('Error', 'Debe seleccionar un alumno y un curso')
            return
        no_inscripcion = self.run_query("SELECT No_Inscripción FROM Inscritos WHERE Id_Alumno = ?", (id_alumno,))
        if not no_inscripcion:
            no_inscripcion = self.run_query("SELECT Num_Actual FROM N_Inscrito")
            self.update_query('N_Inscrito', ['Num_Actual'], [no_inscripcion[0][0] + 1], 'Num_Actual = ' + str(no_inscripcion[0][0]))
        no_inscripcion = no_inscripcion[0][0]
        if self.run_query("SELECT Código_Curso FROM Inscritos WHERE No_Inscripción = ? AND Código_Curso = ?", (no_inscripcion, codigo_curso)):
            messagebox.showerror('Error', 'Ya existe una inscripción para este curso')
            self.limpiar_campos_de_proceso
            return
        resultado = self.run_query("SELECT Código_Curso FROM Cursos WHERE Código_Curso = ?", (codigo_curso,))
        if not resultado or len(resultado) > 1:
            messagebox.showerror('Error', 'El curso seleccionado no existe')
            return
        self.insert_query('Inscritos', ['No_Inscripción', 'Id_Alumno', 'Fecha_Inscripción', 'Código_Curso', 'Horario'],
                          [no_inscripcion, id_alumno, fecha, codigo_curso, horas])
        self.limpiar_campos_de_proceso()
        messagebox.showinfo('Información', 'Inscripción guardada con éxito')
        self.rellenar_num_inscripcion()
        self.mostrar_busqueda()

    def mostrar_busqueda(self, _=""):
        if str(self.btnBuscar['state']) == 'disabled' and _ == "":
            messagebox.showinfo('Aviso', 'Se esta llevando a cabo un proceso, para salir presione el botón "Cancelar" o termine el proceso')
            return
        id = self.cmbx_Id_Alumno.get().strip()
        N_Inscripcion = self.num_Inscripcion.get().strip()
        if id:
            consulta = "SELECT Id_Alumno, Código_Curso, Horario FROM Inscritos WHERE Id_Alumno = ?"
            resultado = self.run_query(consulta, (id,))
        elif N_Inscripcion:
            consulta = "SELECT Id_Alumno, Código_Curso, Horario FROM Inscritos WHERE No_Inscripción = ?"
            resultado = self.run_query(consulta, (N_Inscripcion,))
        else:
            messagebox.showinfo(title="Error", message="Debe proporcionar un Id_Alumno o No_Inscripción")
            return

        if resultado:
            if len(self.tView.get_children()) > 0:
                self.tView.delete(*self.tView.get_children())
            for i in resultado:
                descripcion_C = "SELECT Descrip_Curso FROM Cursos WHERE Código_Curso = ?"
                descripcion_Curso = self.run_query(descripcion_C, (i[1],))
                self.tView.insert("", "end", values=(i[0], i[1], descripcion_Curso[0][0], i[2]))
            return 1
        else:
            messagebox.showinfo(title="Error", message="No se encontraron coincidencias del Id_Alumno o No_Inscripción")
            return 
         
    def seleccion_treeview(self, _=""):
        consulta = self.tView.selection()
        if consulta:
            resultados = self.tView.item(consulta[0], option = "values")
            return resultados
        else:
            return None
        
    def editar(self, _=""):
        if str(self.btnEditar['state']) == 'disabled':
            messagebox.showinfo('Aviso', 'Se esta llevando a cabo un proceso, para salir presione el botón "Cancelar" o termine el proceso')
            return
        resultado = self.seleccion_treeview()
        if resultado is not None:
            self.cmbx_Id_Curso.delete(0,"end")
            self.cmbx_Id_Curso.insert(0,resultado[1])
            self.cmbx_Id_Alumno.delete(0,"end")
            self.cmbx_Id_Alumno.insert(0,resultado[0])
            self.descripc_Curso.config(state="enabled")
            self.descripc_Curso.delete(0,"end")
            self.rellenar_curso()
            self.cmbx_Id_Curso.config(state="disabled")
            self.horario.delete(0, "end")
            self.horario.insert(0,resultado[3])
            fecha = self.run_query('SELECT fecha_Inscripción FROM Inscritos WHERE Id_Alumno = ? AND Código_Curso = ?', (resultado[0],resultado[1]))[0][0]
            year, month, day = fecha.split('-')
            fecha = f'{day}/{month}/{year}'
            self.fecha.config(state="enabled")
            self.fecha.delete(0, "end")
            self.fecha.insert(0,fecha)
            self.fecha.config(state="disabled")
            messagebox.showinfo('Información', 'Una vez finalizada la ediciòn presione el botón "Guardar"')
            self.num_Inscripcion.config(state="disabled")
            self.cmbx_Id_Alumno.config(state="disabled")
            self.btnEditar.config(state="disabled")
            self.btnBuscar.config(state="disabled")
            self.btnEliminar.config(state="disabled")
        else: 
            messagebox.showinfo(title="Error", message="Debe seleccionar un curso a editar")

    def eliminar_opciones(self, _=''):
        if str(self.btnEliminar['state']) == 'disabled':
            messagebox.showinfo('Aviso', 'Se esta llevando a cabo un proceso, para salir presione el botón "Cancelar" o termine el proceso')
            return
        num_inscripcion = self.num_Inscripcion.get().strip()
        if str(self.btnGuardar['state']) == 'disabled':
            resultado = self.seleccion_treeview()
            if resultado is not None:
                self.delete_query('Inscritos', f'No_Inscripción = "{num_inscripcion}" AND Id_Alumno = "{resultado[0]}" AND Código_Curso = "{resultado[1]}"')
                if len(self.tView.get_children()) > 1:
                    self.mostrar_busqueda(1)
                else:
                    self.cancelar()
                messagebox.showinfo('Información', 'Curso eliminado con éxito')
            else:
                messagebox.showinfo('Aviso', 'Debe seleccionar un curso para eliminar')
                return
            self.limpiar_campos_de_proceso()
            return
        if not num_inscripcion:
            messagebox.showerror('Error', 'Debe seleccionar un número de inscripción')
            return
        if not self.mostrar_busqueda():
            return
        
        def opcion(opcion):
            if opcion == 'aceptar':
                if self.opcion_seleccionada.get() == 'inscripcion':
                    messagebox.showinfo('Información', 'Seleccione un curso y vuelva a presionar el botón "Eliminar"')
                    self.btnBuscar.config(state="disabled")
                    self.btnGuardar.config(state="disabled")
                    self.btnEditar.config(state="disabled")
                    self.cmbx_Id_Alumno.config(state="disabled")
                    self.num_Inscripcion.config(state="disabled")
                    self.cmbx_Id_Curso.config(state="disabled")
                elif self.opcion_seleccionada.get() == 'registro':
                    try:
                        self.delete_query('Inscritos', f'No_Inscripción = "{num_inscripcion}"')
                        messagebox.showinfo('Información', 'Inscripción eliminada con éxito')
                        self.cancelar() # Limpiar campos después de eliminar
                    except Exception as e:
                        messagebox.showerror('Error', f'Hubo un error al eliminar la inscripción: {e}')
                else:
                    messagebox.showerror('Error', 'Debe seleccionar una opción')
            self.eliminar_Opciones.destroy()

        self.eliminar_Opciones = tk.Toplevel()
        self.eliminar_Opciones.title('Eliminar')
        self.eliminar_Opciones.resizable(False, False)
        self.eliminar_Opciones.iconbitmap(PATH + '/img/antipenguin.ico')
        window_width = self.eliminar_Opciones.winfo_reqwidth()
        window_height = self.eliminar_Opciones.winfo_reqheight()
        position_right = int(self.eliminar_Opciones.winfo_screenwidth()/2 - window_width/2)
        position_down = int(self.eliminar_Opciones.winfo_screenheight()/2 - window_height/2)
        self.eliminar_Opciones.geometry("+{}+{}".format(position_right, position_down))
        try:
            self.eliminar_Opciones.grab_set()
        except:
            pass
        self.opcion_seleccionada = tk.StringVar()
        self.eliminar_Opciones.pack_propagate(0)
        self.rdbtneliminar_Inscripcion = tk.Radiobutton(self.eliminar_Opciones, text="Eliminar un curso", variable=self.opcion_seleccionada, value="inscripcion")
        self.rdbtneliminar_Inscripcion.pack()
        self.rdbtneliminar_Registro = tk.Radiobutton(self.eliminar_Opciones, text="Eliminar el registro", variable=self.opcion_seleccionada, value="registro")
        self.rdbtneliminar_Registro.pack()
        self.btnconfirmar_Eliminacion = ttk.Button(self.eliminar_Opciones, text="Confirmar", command=lambda:opcion('aceptar'))
        self.btnconfirmar_Eliminacion.pack(side='left')
        self.btneliminar_Cancelar = ttk.Button(self.eliminar_Opciones, text="Cancelar", command=lambda:opcion('cancelar'))
        self.btneliminar_Cancelar.pack(side='right')
        

    def cancelar(self, _=''):
        self.num_Inscripcion.config(state="enabled")
        self.num_Inscripcion.delete(0, tk.END)
        self.cmbx_Id_Alumno.config(state="enabled")
        self.cmbx_Id_Alumno.delete(0, tk.END)
        self.fecha.config(state="enabled")
        self.fecha.delete(0, tk.END)
        self.nombres.config(state="enabled")
        self.nombres.delete(0, tk.END)
        self.nombres.config(state="disabled")
        self.apellidos.config(state="enabled") 
        self.apellidos.delete(0, tk.END)
        self.apellidos.config(state="disabled")
        self.cmbx_Id_Curso.config(state="enabled")
        self.cmbx_Id_Curso.delete(0, tk.END)
        self.descripc_Curso.config(state="enabled")
        self.descripc_Curso.delete(0, tk.END)
        self.descripc_Curso.config(state="disabled")
        self.horario.delete(0, tk.END)
        self.btnBuscar.config(state="enabled")
        self.btnGuardar.config(state="enabled")
        self.btnEditar.config(state="enabled")
        self.btnEliminar.config(state="enabled")
        self.tView.delete(*self.tView.get_children())
        self.num_inscripcion_update()
        
if __name__ == '__main__':
    app = Inscripciones()
    app.run()
