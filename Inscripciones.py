# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import re
from tkinter import messagebox
from datetime import date


class Inscripciones:
    def __init__(self, master=None):
         # Ventana principal
        self.db_name = 'Inscripciones.db'    
        self.win = tk.Tk(master)
        self.win.configure(background='#f7f9fd', height=600, width=800)
        self.win.geometry('800x600')
        self.win.resizable(False, False)
        self.win.title('Inscripciones de Materias y Cursos')
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
                          foreground=[('disabled', '#000000'), ('!disabled', '#f7f9fd')], 
                          fieldbackground=[('disabled', '#ffffff'), ('!disabled', '#ffffff')])
        
         #Label No. Inscripción
        self.lblNoInscripcion.place(anchor='nw', x=680, y=20)
        #Combobox No_Inscripción
        self.num_Inscripcion = ttk.Combobox(self.frm_1, name='num_inscripcion')
        self.num_Inscripcion.place(anchor='nw', width=100, x=682, y=42)
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name='lblfecha')
        self.lblFecha.configure(background='#f7f9fd', text='Fecha:')
        self.lblFecha.place(anchor='nw', x=630, y=80)
        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name='fecha')
        self.fecha.configure(justify='center')
        self.fecha.place(anchor='nw', width=100, x=680, y=80)
        self.fecha.bind('<KeyRelease>', self.date_Verification)
        self.fecha.bind('<ButtonRelease-1>', self.date_Verification)
        self.fecha.bind('<Button-1>', self.date_Verification)
        
        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name='lblidalumno')
        self.lblIdAlumno.configure(background='#f7f9fd', text='Id Alumno:')
        self.lblIdAlumno.place(anchor='nw', x=20, y=80)
        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name='cmbx_id_alumno')
        self.cmbx_Id_Alumno.place(anchor='nw', width=112, x=100, y=80)
        
        #Label Alumno
        self.lblNombres = ttk.Label(self.frm_1, name='lblnombres')
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor='nw', x=20, y=130)
        #Entry Alumno
        self.nombres = ttk.Entry(self.frm_1, name='nombres')
        self.nombres.place(anchor='nw', width=200, x=100, y=130)
        
        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name='lblapellidos')
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor='nw', x=400, y=130)
        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name='apellidos')
        self.apellidos.place(anchor='nw', width=200, x=485, y=130)
        
        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name='lblidcurso')
        self.lblIdCurso.configure(background='#f7f9fd',state='normal',text='Id Curso:')
        self.lblIdCurso.place(anchor='nw', x=20, y=185)
        #Entry Curso
        self.id_Curso = ttk.Entry(self.frm_1, name='id_curso')
        self.id_Curso.configure(justify='left', width=166)
        self.id_Curso.place(anchor='nw', width=166, x=100, y=185)
        
        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name='lbldsccurso')
        self.lblDscCurso.configure(background='#f7f9fd',state='normal',text='Curso:')
        self.lblDscCurso.place(anchor='nw', x=275, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name='descripc_curso')
        self.descripc_Curso.configure(justify='left', width=166)
        self.descripc_Curso.place(anchor='nw', width=300, x=325, y=185)
        
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
        self.btnStyle.configure('TButton', background='#f7f9fd',font=('Arial', 11, 'bold'), relief='raised',padding=5)
        self.btnStyle.map('TButton',
                            foreground=[('!disabled', '#0000ff'), ('active', '#00ffff'), ('disabled', '#f7f9fe')], 
                            background=[('!disabled', '#ffffff'), ('active', '#00ffff'), ('disabled', '#000000')])
        
        #Boton Buscar
        self.btnGuardar = ttk.Button(self.frm_1, name='btnbuscar')
        self.btnGuardar.configure(text='Buscar')
        self.btnGuardar.place(anchor='nw', x=150, y=260)
        
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name='btnguardar')
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor='nw', x=250, y=260)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name='btneditar')
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor='nw', x=350, y=260)
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name='btneliminar')
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor='nw', x=450, y=260)
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name='btncancelar')
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor='nw', x=550, y=260)
        
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient='horizontal')
        separator1.place(anchor='nw', width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name='tview')
        self.tView.configure(selectmode='extended')
        
        #Columnas del Treeview
        self.tView_cols = ['tV_descripción']
        self.tView_dcols = ['tV_descripción']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column('#0',anchor='w',stretch=True,width=10,minwidth=10)
        self.tView.column('tV_descripción',anchor='w',stretch=True,width=200,minwidth=50)
        
        #Cabeceras
        self.tView.heading('#0', anchor='w', text='Curso')
        self.tView.heading('tV_descripción', anchor='w', text='Descripción')
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

    ''' A partir de este punto se deben incluir las funciones
     para el manejo de la base de datos '''
     
    def run_Query(self, query, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
            final = result.fetchall()
        return final if final else None
                
                

    def insert_Query(self, tabla, filas, valores):
        insert = f'INSERT INTO {tabla} ({', '.join(filas)}) VALUES ({', '.join(map(str, valores))})'
        self.run_Query(insert)

    '''

    def insert_query(self, tabla, filas, valores):
        insert = f'INSERT INTO {tabla} ({', '.join(filas)}) VALUES ({', '.join(['?' for _ in valores])})'
        self.run_Query(insert, valores)
    '''
    def select_Query(self, tabla):
        select =  f'SELECT * FROM {tabla}'
        return self.run_Query(select)
      
    
    def update_Query(self, tabla, filas, valores, condicion=None):
        set_clause = ', '.join([f'{fila} = "{valor}"' for fila, valor in zip(filas, valores)])
        update = f'UPDATE {tabla} SET {set_clause} '
        if condicion:
            update += f' WHERE {condicion}'
        try:
            self.run_Query(update)
            return True  # La actualización se realizó con éxito
        except Exception as e:
            print(f'Error al actualizar: {e}')
            return False  # La actualización falló
    '''      
    def update_query(self, tabla, filas, valores, condicion=None):
        set_clause = ', '.join([f'{fila} = ?' for fila in filas])
        update = f"UPDATE {tabla} SET {set_clause} "
        if condicion:
            update += f' WHERE {condicion}'
        try:
            self.run_Query(update, valores)
            return True  # La actualización se realizó con éxito
        except Exception as e:
            print(f'Error al actualizar: {e}')
            return False  # La actualización falló
    '''
    def delete_Query(self, tabla, condicion):
        delete = f'DELETE FROM {tabla} WHERE {condicion}'
        self.run_Query(delete)
        
    # Función para verificar la validez de una fecha ingresada en un campo de texto de una interfaz gráfica.
    def date_Verification(self, event=''):
        # Recuperar la fecha del widget correspondiente.
        fecha = self.fecha.get() 

        # Si la fecha excede los 10 caracteres permitidos, mostrar error y recortarla.
        if len(fecha) > 10:
            messagebox.showerror('Error', 'La fecha debe tener maximo 10 caracteres')
            fecha = fecha[:10]

        # Si la fecha parcialmente ingresada parece ser día y mes sin año, agregar el separador.
        if re.match(r'^([0-9]{2}|[0-9]{2}/[0-9]{2})$', fecha):
            fecha += '/'

        # Limpiar la fecha de cualquier carácter no numérico o barra.
        fecha = re.sub(r'[^0-9/]', '', fecha)

        # Limpiar el campo de texto y reinsertar la fecha procesada.
        self.fecha.delete(0, tk.END)
        self.fecha.insert(0, fecha)
        
        # Si la fecha es exactamente 10 caracteres y el evento es 'Guardar', validar formato.
        if len(fecha) == 10 and event == 'Guardar':
            # Validar que el formato de la fecha sea dd/mm/aaaa.
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
                messagebox.showerror('Error', 'La fecha debe tener el formato dd/mm/aaaa')
                return None
            # Descomponer la fecha en día, mes y año y convertirlos a enteros.
            day, month, year = map(int, fecha.split('/'))

            # Intentar crear un objeto de fecha para verificar su validez.
            try:
                date(year, month, day)
                # Si la fecha es válida, devolver en formato aaaa-mm-dd.
                return f'{year}-{month}-{day}'
            except ValueError:
                # Si la fecha es inválida, mostrar error.
                messagebox.showerror('Error', 'La fecha ingresada no es valida')
                return None
        #Si el evento es 'Guardar' pero la fecha tiene una longitud diferente de 10, mostrar error.
        elif len(fecha) != 10 and event == 'Guardar':
            messagebox.showerror('Error', 'La fecha debe tener al menos 10 caracteres')
            return None

                

if __name__ == '__main__':
    app = Inscripciones()
    app.run()
