# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import sqlite3


class Inscripciones_2:
    def __init__(self, master=None):
         # Ventana principal
        self.db_name = 'Inscripciones.db'    
        self.win = tk.Tk(master)
        self.win.configure(background="#f7f9fd", height=600, width=800)
        self.win.geometry("800x600")
        self.win.resizable(False, False)
        self.win.title("Inscripciones de Materias y Cursos")
        # Crea los frames
        self.frm_1 = tk.Frame(self.win, name="frm_1")
        self.frm_1.configure(background="#f7f9fd", height=600, width=800)
        self.lblNoInscripcion = ttk.Label(self.frm_1, name="lblnoinscripcion")
        self.lblNoInscripcion.configure(background="#f7f9fd",font="{Arial} 11 {bold}",
                                        justify="left",state="normal",
                                        takefocus=False,text='No.Inscripción')
         #Label No. Inscripción
        self.lblNoInscripcion.place(anchor="nw", x=680, y=20)
        #Entry No. Inscripción
        self.num_Inscripcion = ttk.Entry(self.frm_1, name="num_inscripcion")
        self.num_Inscripcion.configure(justify="right")
        self.num_Inscripcion.place(anchor="nw", width=100, x=682, y=42)
        
        #Label Fecha
        self.lblFecha = ttk.Label(self.frm_1, name="lblfecha")
        self.lblFecha.configure(background="#f7f9fd", text='Fecha:')
        self.lblFecha.place(anchor="nw", x=630, y=80)
        #Entry Fecha
        self.fecha = ttk.Entry(self.frm_1, name="fecha")
        self.fecha.configure(justify="center")
        self.fecha.place(anchor="nw", width=90, x=680, y=80)
        #Label Alumno
        self.lblIdAlumno = ttk.Label(self.frm_1, name="lblidalumno")
        self.lblIdAlumno.configure(background="#f7f9fd", text='Id Alumno:')
        self.lblIdAlumno.place(anchor="nw", x=20, y=80)
        #Combobox Alumno
        self.cmbx_Id_Alumno = ttk.Combobox(self.frm_1, name="cmbx_id_alumno")
        self.cmbx_Id_Alumno.place(anchor="nw", width=112, x=100, y=80)
        #Label Alumno
        self.lblNombres = ttk.Label(self.frm_1, name="lblnombres")
        self.lblNombres.configure(text='Nombre(s):')
        self.lblNombres.place(anchor="nw", x=20, y=130)
        #Entry Alumno
        self.nombres = ttk.Entry(self.frm_1, name="nombres")
        self.nombres.place(anchor="nw", width=200, x=100, y=130)
        #Label Apellidos
        self.lblApellidos = ttk.Label(self.frm_1, name="lblapellidos")
        self.lblApellidos.configure(text='Apellido(s):')
        self.lblApellidos.place(anchor="nw", x=400, y=130)
        #Entry Apellidos
        self.apellidos = ttk.Entry(self.frm_1, name="apellidos")
        self.apellidos.place(anchor="nw", width=200, x=485, y=130)
        #Label Curso
        self.lblIdCurso = ttk.Label(self.frm_1, name="lblidcurso")
        self.lblIdCurso.configure(background="#f7f9fd",state="normal",text='Id Curso:')
        self.lblIdCurso.place(anchor="nw", x=20, y=185)
        #Entry Curso
        self.id_Curso = ttk.Entry(self.frm_1, name="id_curso")
        self.id_Curso.configure(justify="left", width=166)
        self.id_Curso.place(anchor="nw", width=166, x=100, y=185)
        #Label Descripción del Curso
        self.lblDscCurso = ttk.Label(self.frm_1, name="lbldsccurso")
        self.lblDscCurso.configure(background="#f7f9fd",state="normal",text='Curso:')
        self.lblDscCurso.place(anchor="nw", x=275, y=185)
        #Entry de Descripción del Curso 
        self.descripc_Curso = ttk.Entry(self.frm_1, name="descripc_curso")
        self.descripc_Curso.configure(justify="left", width=166)
        self.descripc_Curso.place(anchor="nw", width=300, x=325, y=185)
        #Label Horario
        self.lblHorario = ttk.Label(self.frm_1, name="label3")
        self.lblHorario.configure(background="#f7f9fd",state="normal",text='Hora:')
        self.lblHorario.place(anchor="nw", x=635, y=185)
        #Entry del Horario
        self.horario = ttk.Entry(self.frm_1, name="entry3")
        self.horario.configure(justify="left", width=166)
        self.horario.place(anchor="nw", width=100, x=680, y=185)

        ''' Botones  de la Aplicación'''
        #Botón Guardar
        self.btnGuardar = ttk.Button(self.frm_1, name="btnguardar")
        self.btnGuardar.configure(text='Guardar')
        self.btnGuardar.place(anchor="nw", x=200, y=260)
        
        #Botón Editar
        self.btnEditar = ttk.Button(self.frm_1, name="btneditar")
        self.btnEditar.configure(text='Editar')
        self.btnEditar.place(anchor="nw", x=300, y=260)
        #Botón Eliminar
        self.btnEliminar = ttk.Button(self.frm_1, name="btneliminar")
        self.btnEliminar.configure(text='Eliminar')
        self.btnEliminar.place(anchor="nw", x=400, y=260)
        #Botón Cancelar
        self.btnCancelar = ttk.Button(self.frm_1, name="btncancelar")
        self.btnCancelar.configure(text='Cancelar')
        self.btnCancelar.place(anchor="nw", x=500, y=260)
        #Separador
        separator1 = ttk.Separator(self.frm_1)
        separator1.configure(orient="horizontal")
        separator1.place(anchor="nw", width=796, x=2, y=245)

        ''' Treeview de la Aplicación'''
        #Treeview
        self.tView = ttk.Treeview(self.frm_1, name="tview")
        self.tView.configure(selectmode="extended")
        #Columnas del Treeview
        self.tView_cols = ['tV_descripción']
        self.tView_dcols = ['tV_descripción']
        self.tView.configure(columns=self.tView_cols,displaycolumns=self.tView_dcols)
        self.tView.column("#0",anchor="w",stretch=True,width=10,minwidth=10)
        self.tView.column("tV_descripción",anchor="w",stretch=True,width=200,minwidth=50)
        #Cabeceras
        self.tView.heading("#0", anchor="w", text='Curso')
        self.tView.heading("tV_descripción", anchor="w", text='Descripción')
        self.tView.place(anchor="nw", height=300, width=790, x=4, y=300)
        #Scrollbars
        self.scroll_H = ttk.Scrollbar(self.frm_1, name="scroll_h")
        self.scroll_H.configure(orient="horizontal")
        self.scroll_H.place(anchor="s", height=12, width=1534, x=15, y=595)
        self.scroll_Y = ttk.Scrollbar(self.frm_1, name="scroll_y")
        self.scroll_Y.configure(orient="vertical")
        self.scroll_Y.place(anchor="s", height=275, width=12, x=790, y=582)
        self.frm_1.pack(side="top")
        self.frm_1.pack_propagate(0)

        # Main widget
        self.mainwindow = self.win

    def run(self):
        self.mainwindow.mainloop()


    ''' A partir de este punto se deben incluir las funciones
     para el manejo de la base de datos '''

if __name__ == "__main__":
    app = Inscripciones_2()
    app.run()
