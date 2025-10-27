from tkinter import*
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import ttkbootstrap as tb
import os
import sqlite3
import tkinter as tk 
import shutil

class ventana(tb.Window):

    def __init__(self):
        super().__init__(themename="flatly")
        self.ventana_login()

    def ventana_login(self):

        #frame login
        self.frame_login = Frame(self, bg='white', padx=20, pady=20)  # Inicializar frame_login aquí
        self.frame_login.pack(fill=BOTH, expand=True)

        #cargar img fondo
        self.img_fondo = Image.open(r"C:\\Users\\Administrator\\Downloads\\pixelcut-export.png")  # Cambia la ruta a la ubicación de tu imagen
        self.img_fondo = self.img_fondo.resize((self.winfo_width(), self.winfo_height()), Image.LANCZOS)
        self.img_fondo_tk = ImageTk.PhotoImage(self.img_fondo)

        lbl_fondo = Label(self.frame_login, image=self.img_fondo_tk)
        lbl_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        #labelframe para form login
        self.lblframe_login=LabelFrame(self.frame_login,text='ACCESO',bg='white', fg='black')
        self.lblframe_login.pack(padx=10, pady=10)

        lbltitulo=Label(self.lblframe_login, text='INICIAR SESION', font=('Arial',30), bg='white', fg='black')
        lbltitulo.pack(padx=10,pady=35)

        self.txt_usuario=ttk.Entry(self.lblframe_login, width=40,justify=CENTER)
        self.txt_usuario.pack(padx=10, pady=10)

        self.txt_clave=ttk.Entry(self.lblframe_login, width=40,justify=CENTER)
        self.txt_clave.pack(padx=10, pady=10)
        self.txt_clave.configure(show='*')
        
        btn_acceso=ttk.Button(self.lblframe_login, text='ENTRAR',width=38, command=self.logueo)
        btn_acceso.pack(padx=10, pady=10)

    def ventana_menu(self):

        # Frame para el menú
        self.frame_menu = Frame(self, bg='white')
        self.frame_menu.grid(row=0, column=0, sticky='nsew')

        # Configurar la expansión de filas y columnas
        self.frame_menu.grid_rowconfigure(0, weight=1)
        self.frame_menu.grid_columnconfigure(0, weight=1)

        # Frame para los botones
        self.frame_left = Frame(self.frame_menu, bg='white')
        self.frame_left.grid(row=0, column=0, sticky='nsew')

        # Configurar la expansión de filas y columnas en frame_left
        for i in range(5):  # 5 filas para los botones
            self.frame_left.grid_rowconfigure(i, weight=1)
        self.frame_left.grid_columnconfigure(0, weight=1)

        # Frame para el logo
        self.frame_center = Frame(self)
        self.frame_center.grid(row=0, column=1, sticky=NSEW)

        # Mensaje de bienvenida
        lbl_bienvenida = Label(self.frame_center, text="BIENVENIDOS A", font=('Helvetica', 28, 'bold italic'), bg='white', fg='black')
        lbl_bienvenida.grid(row=0, column=0, pady=20)  # Añadir un poco de espacio arriba

        # Cargar y mostrar el logo
        self.img_logo = Image.open(r"C:\\Users\\Administrator\\Downloads\\pixelcut-export.png")  # Cambia la ruta a la ubicación de tu logo
        self.img_logo = self.img_logo.resize((400, 200), Image.LANCZOS)  # Redimensionar la imagen si es necesario
        self.img_logo_tk = ImageTk.PhotoImage(self.img_logo)

        lbl_logo = Label(self.frame_center, image=self.img_logo_tk)
        lbl_logo.grid(row=1, column=0, pady=20)  # Añadir un poco de espacio arriba

        #botones del menu
        btn_documentos=ttk.Button(self.frame_left, text='DOCUMENTOS', width=20, command=self.ventana_documentos)
        btn_documentos.grid(row=0, column=0,padx=10,pady=10, sticky='ew')
        
        btn_clientes=ttk.Button(self.frame_left, text='CLIENTES', width=20, command=self.gestion_clientes)
        btn_clientes.grid(row=1, column=0,padx=10,pady=10, sticky='ew')
        
        btn_usuarios=ttk.Button(self.frame_left, text='USUARIOS', width=20, command=self.ventana_usuarios)
        btn_usuarios.grid(row=2, column=0,padx=10,pady=10, sticky='ew')
       
        btn_reportes=ttk.Button(self.frame_left, text='REPORTES', width=20, command=self.ventana_reporte)
        btn_reportes.grid(row=3, column=0,padx=10,pady=10, sticky='ew')

        btn_cerrar_sesion = ttk.Button(self.frame_left, text='CERRAR SESIÓN', width=20, bootstyle='danger', command=self.confirmar_cierre_sesion)
        btn_cerrar_sesion.grid(row=5, column=0, padx=5, pady=5, sticky='ew')
       
        # Hacer que los botones se expandan
        self.frame_left.grid_rowconfigure(0, weight=1)
        self.frame_left.grid_rowconfigure(1, weight=1)
        self.frame_left.grid_rowconfigure(2, weight=1)
        self.frame_left.grid_rowconfigure(3, weight=1)
        self.frame_left.grid_rowconfigure(4, weight=1) 

    def confirmar_cierre_sesion(self):
        # Mostrar un mensaje de confirmación
        respuesta = messagebox.askyesno('Confirmar Cierre de Sesión', '¿Estás seguro de que deseas cerrar sesión?')

        if respuesta:

            self.volver_a_login()  # Llama a la función para volver a la ventana de login

    def volver_a_login(self):
          # Ocultar el menú
        for widget in self.winfo_children():
            widget.destroy()  # Eliminar todos los widgets existentes en la ventana principal

        self.ventana_login()  # Llama a la función que muestra la ventana de login

    def logueo(self):

        try:

            mi_conexion=sqlite3.connect('ventas.db')
            mi_cursor=mi_conexion.cursor()
            
            nombre_usuario=self.txt_usuario.get()
            clave_usuario=self.txt_clave.get()

            mi_cursor.execute('SELECT * FROM Usuarios WHERE Nombre=? AND Clave=?' , (nombre_usuario,clave_usuario))
            datos_logueo=mi_cursor.fetchall()
            if datos_logueo!='':

                for row in datos_logueo:
                   
                    nom_usu=row[1]
                    cla_usu=row[2]
                    

                if(nom_usu==self.txt_usuario.get() and cla_usu==self.txt_clave.get()):
                    self.frame_login.pack_forget()
                    self.ventana_menu()

            mi_conexion.commit()
            mi_conexion.close()

        except:

            messagebox.showerror('Acceso','Usuario o Clave son incorrectos')

    def ventana_documentos(self):

         # Limpiar el frame central
        for widget in self.frame_center.winfo_children():
            widget.destroy()

        # Título centrado para el Treeview
        lbl_titulo = tk.Label(self.frame_center, text="DOCUMENTOS", font=('Arial', 20))
        lbl_titulo.grid(row=0, column=0, pady=10)

        # Configuración del Treeview
        self.tree_documentos = ttk.Treeview(self.frame_center, columns=("ID", "Fecha", "Nombre", "Ruta"), show='headings')
        self.tree_documentos.grid(row=1, column=0, sticky='nsew')

        # Configuración de columnas
        self.tree_documentos.heading("ID", text="ID")
        self.tree_documentos.heading("Fecha", text="Fecha")
        self.tree_documentos.heading("Nombre", text="Nombre")
        self.tree_documentos.heading("Ruta", text="Ruta")

        # Centrar el texto en las columnas
        self.tree_documentos.column("ID", anchor='center')
        self.tree_documentos.column("Fecha", anchor='center')
        self.tree_documentos.column("Nombre", anchor='center')
        self.tree_documentos.column("Ruta", anchor='center')

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_center, orient=tk.VERTICAL, command=self.tree_documentos.yview)
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.tree_documentos.configure(yscrollcommand=self.scrollbar.set)

        # Cargar documentos al iniciar
        self.cargar_documentos()

        # Frame para los botones de gestión
        self.frame_botones = tk.Frame(self.frame_center)
        self.frame_botones.grid(row=2, column=0, pady=10)

        # Botones de gestión
        self.btn_agregar = ttk.Button(self.frame_botones, text="AGREGAR DOCUMENTO", bootstyle='succes',command=self.adjuntar_documento)
        self.btn_agregar.grid(row=0, column=0, padx=5, sticky='ew')

        self.btn_eliminar = ttk.Button(self.frame_botones, text="ELIMINAR DOCUMENTO",bootstyle='danger', command=self.eliminar_documento)
        self.btn_eliminar.grid(row=0, column=1, padx=5, sticky='ew')

        # Centrar los botones en el frame
        self.frame_botones.grid_columnconfigure(0, weight=1)  # Permitir que la columna 0 se expanda
        self.frame_botones.grid_columnconfigure(1, weight=1)  # Permitir que la columna 1 se expanda

        self.tree_documentos.bind("<Double-1>", self.abrir_documento)
        
        self.frame_center.grid_rowconfigure(1, weight=1)  # Permitir que la fila del Treeview se expanda
        self.frame_center.grid_columnconfigure(0, weight=1)  # Permitir que la columna del Treeview se expanda
        
    def subir_documento(self):
        import shutil
        from tkinter import simpledialog, filedialog, messagebox

        # Preguntar qué tipo de documento es
        tipo_documento = simpledialog.askstring('Tipo de Documento', '¿Qué tipo de documento es? (Factura, Contrato, Otro)')

        # Determinar la carpeta correspondiente
        if tipo_documento == 'Factura':
            carpeta = 'Documentos/Facturas'
        elif tipo_documento == 'Contrato':
            carpeta = 'Documentos/Contratos'
        else:
            carpeta = 'Documentos/Otros'

        # Seleccionar el archivo a subir
        archivo = filedialog.askopenfilename(title='Subir Documento', filetypes=(('Archivos PDF', '*.pdf'),))
        if archivo:
            shutil.copy(archivo, carpeta)
            messagebox.showinfo('Documento Subido', 'El documento ha sido subido correctamente.')


    def abrir_documento(self, event):

        selected_item = self.tree_documentos.selection()

        if selected_item:
                
            item_values = self.tree_documentos.item(selected_item, 'values')
            ruta_documento = item_values[3]  # Obtener la ruta del documento seleccionado

            print(f"Ruta del documento: {ruta_documento}")  # Verificar la ruta

            if os.path.exists(ruta_documento):  # Verificar si el archivo existe

                try:

                    os.startfile(ruta_documento)  # Abrir la ruta del documento

                except Exception as e:

                    messagebox.showerror('Error', f'Ocurrió un error al abrir el documento: {str(e)}')
        else:
            messagebox.showerror('Error', 'El documento no se encuentra en la ruta especificada.')

    def cargar_documentos(self):
        # Limpiar el Treeview
        for item in self.tree_documentos.get_children():
            self.tree_documentos.delete(item)

        # Conectar a la base de datos y obtener documentos
        try:
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('SELECT ID, Fecha, Nombre, Ruta FROM Documentos')  # Asegúrate de que la tabla y columnas existan
            documentos = mi_cursor.fetchall() 

            for documento in documentos:
                print(f"Cargando documento: {documento}")
                self.tree_documentos.insert('', 'end', values=documento)

            mi_conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar los documentos: {str(e)}")

    def ventana_nuevo_documento(self):

        # Crear un nuevo frame para el formulario
        self.frame_nuevo_documento = tk.Toplevel(self)
        self.frame_nuevo_documento.title("Nuevo Documento")
        self.frame_nuevo_documento.geometry("400x300")
        self.frame_nuevo_documento.resizable(False, False)

        # Etiquetas y campos de entrada
        tk.Label(self.frame_nuevo_documento, text="Nombre del documento").grid(row=0, column=0, padx=10, pady=10)
        self.txt_nombre_documento = tk.Entry(self.frame_nuevo_documento)
        self.txt_nombre_documento.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_documento, text="Carpeta destino").grid(row=1, column=0, padx=10, pady=10)
        self.cmb_carpeta_destino = ttk.Combobox(self.frame_nuevo_documento, values=["Facturas", "Contratos", "Otros"])
        self.cmb_carpeta_destino.grid(row=1, column=1, padx=10, pady=10)
        self.cmb_carpeta_destino.current(0)  # Seleccionar la primera opción por defecto

        tk.Label(self.frame_nuevo_documento, text="Archivo").grid(row=2, column=0, padx=10, pady=10)
        self.txt_archivo = tk.Entry(self.frame_nuevo_documento)
        self.txt_archivo.grid(row=2, column=1, padx=10, pady=10)

        # Botón para seleccionar el archivo
        btn_seleccionar_archivo = ttk.Button(self.frame_nuevo_documento, text="Seleccionar archivo", command=self.seleccionar_archivo)
        btn_seleccionar_archivo.grid(row=2, column=2, padx=10, pady=10)

        # Botón para guardar el nuevo documento
        btn_guardar_documento = ttk.Button(self.frame_nuevo_documento, text="Guardar", command=self.guardar_documento)
        btn_guardar_documento.grid(row=3, column=0, columnspan=3, pady=20)

    def seleccionar_archivo(self):

        # Abrir un diálogo para seleccionar el archivo
        archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos PDF", "*.pdf")])

        # Mostrar el nombre del archivo seleccionado
        self.txt_archivo.delete(0, tk.END)
        self.txt_archivo.insert(0, archivo)

    def guardar_documento(self):

        # Obtener los datos del formulario
        carpeta_destino = self.cmb_carpeta_destino.get()
        archivo = self.txt_archivo.get()

        # Verificar que se haya seleccionado un archivo
        if archivo == "":
            messagebox.showerror("Error", "Debes seleccionar un archivo")
            return

        # Verificar que se haya seleccionado una carpeta destino
        if carpeta_destino == "":
            messagebox.showerror("Error", "Debes seleccionar una carpeta destino")
            return

        # Configurar la carpeta destino
        ruta_destino = f"Documentos/{carpeta_destino}"

        # Verificar si la carpeta destino existe
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)

        # Copiar el archivo a la carpeta destino
        try:
            shutil.copy(archivo, f"Documentos/{carpeta_destino}")
            messagebox.showinfo("Guardar documento", "Documento guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el documento: {str(e)}")

    def adjuntar_documento(self):
        # Abrir un diálogo para seleccionar un archivo
        archivo = filedialog.askopenfilename(title="Seleccionar Documento", filetypes=(("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")))
        if archivo:
            nombre_documento = os.path.basename(archivo)  # Obtener solo el nombre del archivo
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtener la fecha actual en formato YYYY-MM-DD

            try:
                # Conectar a la base de datos y guardar el documento
                mi_conexion = sqlite3.connect('ventas.db')
                mi_cursor = mi_conexion.cursor()
                mi_cursor.execute('INSERT INTO Documentos (Nombre, Fecha, Ruta) VALUES (?, ?, ?)', (nombre_documento, fecha_actual, archivo))
                mi_conexion.commit()
                mi_conexion.close()

                messagebox.showinfo('Guardar Documento', 'Documento guardado correctamente.')
                self.cargar_documentos()  # Refrescar la lista de documentos

            except Exception as e:
                messagebox.showerror('Error', f'Ocurrió un error al guardar el documento: {str(e)}')

    def eliminar_documento(self):

        selected_item = self.tree_documentos.selection()

        if selected_item:

            item_values = self.tree_documentos.item(selected_item, 'values')
            print(f"Valores del documento seleccionado: {item_values}")
            id_documento = item_values[0]  # Obtener el ID del documento seleccionado

            if id_documento is None:

                messagebox.showwarning('Eliminar Documento', 'No se pudo obtener el ID del documento seleccionado.')
                return

            # Confirmar la eliminación
            respuesta = messagebox.askyesno('Eliminar Documento', f'¿Estás seguro de que deseas eliminar el documento con ID {id_documento}?')

            if respuesta:

                try:
                    mi_conexion = sqlite3.connect('ventas.db')
                    mi_cursor = mi_conexion.cursor()
                    mi_cursor.execute('DELETE FROM Documentos WHERE ID=?', (id_documento,))
                    mi_conexion.commit()
                    mi_conexion.close()

                    messagebox.showinfo('Eliminar Documento', 'Documento eliminado correctamente.')

                    print(f"Eliminando documento con ID: {id_documento}")
                    self.cargar_documentos()  # Refrescar la lista de documentos

                except Exception as e:

                    messagebox.showerror('Error', f'Ocurrió un error al eliminar el documento: {e}')
        else:
            messagebox.showwarning('Eliminar Documento', 'Por favor, selecciona un documento para eliminar.')

    def gestion_clientes(self):

        # Limpiar el frame central
        for widget in self.frame_center.winfo_children():
            widget.destroy()  # Eliminar todos los widgets existentes en el frame central

        # Título centrado para el Treeview
        lbl_titulo = tk.Label(self.frame_center, text="GESTIÓN DE CLIENTES", font=('Arial', 20))
        lbl_titulo.pack(pady=10)  # Añadir un poco de espacio arriba

        # Configuración del Treeview
        self.tree_clientes = ttk.Treeview(self.frame_center, columns=("Cedula", "Nombre", "Apellido", "Direccion"), show='headings')
        self.tree_clientes.pack(fill=tk.BOTH, expand=True)

        # Configuración de columnas
        self.tree_clientes.heading("Cedula", text="Cédula")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Apellido", text="Apellido")
        self.tree_clientes.heading("Direccion", text="Dirección")

        # Centrar el texto en las columnas
        self.tree_clientes.column("Cedula", anchor='center')
        self.tree_clientes.column("Nombre", anchor='center')
        self.tree_clientes.column("Apellido", anchor='center')
        self.tree_clientes.column("Direccion", anchor='center')

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_center, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_clientes.configure(yscrollcommand=self.scrollbar.set)

        # Cargar clientes al iniciar
        self.cargar_clientes()  

        # Frame para los botones de gestión
        self.frame_botones = tk.Frame(self.frame_center)
        self.frame_botones.pack(pady=10)

        # Botones de gestión
        self.btn_nuevo = ttk.Button(self.frame_botones, text="AGREGAR", bootstyle='succes', command=self.ventana_nuevo_cliente)
        self.btn_nuevo.pack(side=tk.LEFT, padx=5)

        self.btn_modificar = ttk.Button(self.frame_botones, text="MODIFICAR", bootstyle='warning', command=self.modificar_cliente)
        self.btn_modificar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="ELIMINAR", bootstyle='danger', command=self.eliminar_cliente)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

    def ventana_nuevo_cliente(self):

            # Crear un nuevo frame para el formulario
        self.frame_nuevo_cliente = tk.Toplevel(self)
        self.frame_nuevo_cliente.title("Nuevo Cliente")
        self.frame_nuevo_cliente.geometry("400x300")
        self.frame_nuevo_cliente.resizable(False, False)

        # Etiquetas y campos de entrada
        tk.Label(self.frame_nuevo_cliente, text="Cédula").grid(row=0, column=0, padx=10, pady=10)
        self.txt_cedula_nuevo_cliente = tk.Entry(self.frame_nuevo_cliente)
        self.txt_cedula_nuevo_cliente.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_cliente, text="Nombre").grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_nuevo_cliente = tk.Entry(self.frame_nuevo_cliente)
        self.txt_nombre_nuevo_cliente.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_cliente, text="Apellido").grid(row=2, column=0, padx=10, pady=10)
        self.txt_apellido_nuevo_cliente = tk.Entry(self.frame_nuevo_cliente)
        self.txt_apellido_nuevo_cliente.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_cliente, text="Dirección").grid(row=3, column=0, padx=10, pady=10)
        self.txt_direccion_nuevo_cliente = tk.Entry(self.frame_nuevo_cliente)
        self.txt_direccion_nuevo_cliente.grid(row=3, column=1, padx=10, pady=10)

        # Botón para guardar el nuevo cliente
        btn_guardar_nuevo_cliente = ttk.Button(self.frame_nuevo_cliente, text='Guardar', command=self.guardar_cliente)
        btn_guardar_nuevo_cliente.grid(row=4, column=0, columnspan=2, pady=20)

    def guardar_cliente(self):

        try:
        # Obtener los datos del formulario
            cedula = self.txt_cedula_nuevo_cliente.get()
            nombre = self.txt_nombre_nuevo_cliente.get()
            apellido = self.txt_apellido_nuevo_cliente.get()
            direccion = self.txt_direccion_nuevo_cliente.get()

            # Conectar a la base de datos y guardar el nuevo cliente
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('INSERT INTO Clientes (Cedula, Nombre, Apellido, Direccion) VALUES (?, ?, ?, ?)', 
                            (cedula, nombre, apellido, direccion))
            mi_conexion.commit()
            mi_conexion.close()

            messagebox.showinfo('Guardar Cliente', 'Cliente guardado correctamente.')
            self.cargar_clientes()  # Refrescar la lista de clientes
            self.frame_nuevo_cliente.destroy()  # Cerrar el formulario

        except Exception as e:
            messagebox.showerror('Error', f'Ocurrió un error al guardar el cliente: {str(e)}')

    def modificar_cliente(self):

        selected_item = self.tree_clientes.selection()

        if selected_item:

            item_values = self.tree_clientes.item(selected_item, 'values')
            self.ventana_modificar_cliente(item_values)

        else:
            messagebox.showwarning('Modificar Cliente', 'Por favor, selecciona un cliente para modificar.')

    def ventana_modificar_cliente(self, item_values):

        # Crear un nuevo frame para el formulario de modificación
        self.frame_modificar_cliente = tk.Toplevel(self)
        self.frame_modificar_cliente.title("Modificar Cliente")
        self.frame_modificar_cliente.geometry("400x300")
        self.frame_modificar_cliente.resizable(False, False)

        # Etiquetas y campos de entrada
        tk.Label(self.frame_modificar_cliente, text="Cédula").grid(row=0, column=0, padx=10, pady=10)
        self.txt_cedula_modificar = tk.Entry(self.frame_modificar_cliente)
        self.txt_cedula_modificar.grid(row=0, column=1, padx=10, pady=10)
        self.txt_cedula_modificar.insert(0, item_values[0])  # Cargar el valor existente

        tk.Label(self.frame_modificar_cliente, text="Nombre").grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_modificar = tk.Entry(self.frame_modificar_cliente)
        self.txt_nombre_modificar.grid(row=1, column=1, padx=10, pady=10)
        self.txt_nombre_modificar.insert(0, item_values[1])  # Cargar el valor existente

        tk.Label(self.frame_modificar_cliente, text="Apellido").grid(row=2, column=0, padx=10, pady=10)
        self.txt_apellido_modificar = tk.Entry(self.frame_modificar_cliente)
        self.txt_apellido_modificar.grid(row=2, column=1, padx=10, pady=10)
        self.txt_apellido_modificar.insert(0, item_values[2])  # Cargar el valor existente

        tk.Label(self.frame_modificar_cliente, text="Dirección").grid(row=3, column=0, padx=10, pady=10)
        self.txt_direccion_modificar = tk.Entry(self.frame_modificar_cliente)
        self.txt_direccion_modificar.grid(row=3, column=1, padx=10, pady=10)
        self.txt_direccion_modificar.insert(0, item_values[3])  # Cargar el valor existente

        # Botón para guardar los cambios
        btn_guardar_modificacion = ttk.Button(self.frame_modificar_cliente, text='Guardar Cambios', 
                                              command=self.guardar_modificacion_cliente)  # Usar la cédula como identificador
        btn_guardar_modificacion.grid(row=4, column=0, columnspan=2, pady=20)

    def guardar_modificacion_cliente(self):

        try:
            # Obtener los datos del formulario
            cedula = self.txt_cedula_modificar.get()
            nombre = self.txt_nombre_modificar.get()
            apellido = self.txt_apellido_modificar.get()
            direccion = self.txt_direccion_modificar.get()

            print(f"Modificando cliente con cédula: {cedula}")


            # Conectar a la base de datos y actualizar el cliente
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('UPDATE Clientes SET Nombre=?, Apellido=?, Direccion=? WHERE Cedula=?', 
                                (nombre, apellido, direccion, cedula))

            mi_conexion.commit()
            mi_conexion.close()

            messagebox.showinfo('Modificar Cliente', 'Cliente modificado correctamente.')
            self.cargar_clientes()  # Refrescar la lista de clientes
            self.frame_modificar_cliente.destroy()  # Cerrar el formulario

        except Exception as e:
                messagebox.showerror('Error', f'Ocurrió un error al modificar el cliente: {str(e)}')


    def cargar_clientes(self):

        # Limpiar el Treeview
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)


        try:
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()

            # Obtener los datos de los clientes
            mi_cursor.execute('SELECT Cedula, Nombre, Apellido, Direccion FROM Clientes')  # Asegúrate de que la tabla y columnas existan
            clientes = mi_cursor.fetchall()

            for cliente in clientes:
                self.tree_clientes.insert('', 'end', values=cliente)  # Insertar cada fila en el Treeview

            mi_conexion.close()


        except Exception as e:
            messagebox.showerror('Error', f'Ocurrió un error al cargar los clientes: {str(e)}')
    
    def eliminar_cliente(self):

        selected_item = self.tree_clientes.selection()

        if selected_item:

            item_values = self.tree_clientes.item(selected_item, 'values')
            cedula_cliente = item_values[0]  # Obtener la cédula del cliente seleccionado

            # Confirmar la eliminación
            respuesta = messagebox.askyesno('Eliminar Cliente', f'¿Estás seguro de que deseas eliminar al cliente con cédula {cedula_cliente}?')

            if respuesta:

                try:

                    mi_conexion = sqlite3.connect('ventas.db')
                    mi_cursor = mi_conexion.cursor()
                    mi_cursor.execute('DELETE FROM Clientes WHERE Cedula=?', (cedula_cliente,))
                    mi_conexion.commit()
                    mi_conexion.close()

                    messagebox.showinfo('Eliminar Cliente', 'Cliente eliminado correctamente.')
                    self.cargar_clientes()  # Refrescar la lista de clientes

                except Exception as e:

                    messagebox.showerror('Error', f'Ocurrió un error al eliminar el cliente: {str(e)}')
        else:
            messagebox.showwarning('Eliminar Cliente', 'Por favor, seleccionna un cliente para eliminar.')

    def ventana_usuarios(self):
     
       # Limpiar el frame central
        for widget in self.frame_center.winfo_children():
            widget.destroy()  # Eliminar todos los widgets existentes en el frame central


        # Frame central para el contenido
        self.frame_center = tk.Frame(self)
        self.frame_center.grid(row=0, column=1, sticky=tk.NSEW)

        # Título centrado para el Treeview
        lbl_titulo = tk.Label(self.frame_center, text="GESTIÓN DE USUARIOS", font=('Arial', 20))
        lbl_titulo.pack(pady=10)  # Añadir un poco de espacio arriba

        # Configuración del Treeview
        self.tree_lista_usuarios = ttk.Treeview(self.frame_center, columns=("Codigo", "Nombre", "Clave", "Rol"), show='headings')
        self.tree_lista_usuarios.pack(fill=tk.BOTH, expand=True)

        # Configuración de columnas
        self.tree_lista_usuarios.heading("Codigo", text="Código")
        self.tree_lista_usuarios.heading("Nombre", text="Nombre")
        self.tree_lista_usuarios.heading("Clave", text="Clave")
        self.tree_lista_usuarios.heading("Rol", text="Rol")

        self.tree_lista_usuarios.column("Codigo", anchor='center')
        self.tree_lista_usuarios.column("Nombre", anchor='center')
        self.tree_lista_usuarios.column("Clave", anchor='center')
        self.tree_lista_usuarios.column("Rol", anchor='center')

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_center, orient=tk.VERTICAL, command=self.tree_lista_usuarios.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_lista_usuarios.configure(yscrollcommand=self.scrollbar.set)

        # Frame para los botones de gestión
        self.frame_botones = tk.Frame(self.frame_center)
        self.frame_botones.pack(pady=10)

        # Botones de gestión
        self.btn_agregar = ttk.Button(self.frame_botones, text="AGREGAR", bootstyle='succes', command=self.ventana_nuevo_usuario)
        self.btn_agregar.pack(side=LEFT, padx=5)

        self.btn_modificar = ttk.Button(self.frame_botones, text="MODIFICAR", bootstyle='warning', command=self.modificar_usuario)
        self.btn_modificar.pack(side=LEFT,padx=5)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="ELIMINAR", bootstyle='danger',command=self.eliminar_usuario)
        self.btn_eliminar.pack(side=LEFT,padx=5)


        self.mostrar_usuarios()  # Cargar usuarios al iniciar

    def mostrar_usuarios(self):

        # Limpiar el Treeview
        for item in self.tree_lista_usuarios.get_children():
            self.tree_lista_usuarios.delete(item)

        # Conectar a la base de datos y obtener usuarios
        try:
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('SELECT * FROM Usuarios')
            usuarios = mi_cursor.fetchall()

            for usuario in usuarios:
                self.tree_lista_usuarios.insert('', 'end', values=usuario)

            mi_conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al mostrar los usuarios: {str(e)}")

    def ventana_nuevo_usuario(self):
        # Crear un nuevo frame para el formulario
        self.frame_nuevo_usuario = tk.Toplevel(self)
        self.frame_nuevo_usuario.title("Nuevo Usuario")
        self.frame_nuevo_usuario.geometry("400x300")
        self.frame_nuevo_usuario.resizable(False, False)

        # Etiquetas y campos de entrada
        tk.Label(self.frame_nuevo_usuario, text="Código").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.txt_codigo_nuevo_usuario = tk.Entry(self.frame_nuevo_usuario)
        self.txt_codigo_nuevo_usuario.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_usuario, text="Nombre").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.txt_nombre_nuevo_usuario = tk.Entry(self.frame_nuevo_usuario)
        self.txt_nombre_nuevo_usuario.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_usuario, text="Clave").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.txt_clave_nuevo_usuario = tk.Entry(self.frame_nuevo_usuario, show='*')
        self.txt_clave_nuevo_usuario.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_usuario, text="Rol").grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.txt_rol_nuevo_usuario = ttk.Combobox(self.frame_nuevo_usuario, values=('Administrador', 'Almacen', 'Vendedor'))
        self.txt_rol_nuevo_usuario.grid(row=3, column=1, padx=10, pady=10)
        self.txt_rol_nuevo_usuario.current(0)  # Seleccionar el primer rol por defecto

        # Botón para guardar el nuevo usuario
        btn_guardar_nuevo_usuario = ttk.Button(self.frame_nuevo_usuario, text='Guardar', command=self.guardar_usuario)
        btn_guardar_nuevo_usuario.grid(row=4, column=0, columnspan=2, pady=20)

    def guardar_usuario(self):

        try:
        # Obtener los datos del formulario
            codigo = self.txt_codigo_nuevo_usuario.get()
            nombre = self.txt_nombre_nuevo_usuario.get()
            clave = self.txt_clave_nuevo_usuario.get()
            rol = self.txt_rol_nuevo_usuario.get()

            # Conectar a la base de datos y guardar el nuevo usuario
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('INSERT INTO Usuarios (Codigo, Nombre, Clave, Rol) VALUES (?, ?, ?, ?)', (codigo, nombre, clave, rol))
            mi_conexion.commit()
            mi_conexion.close()

            messagebox.showinfo('Guardar Usuario', 'Usuario guardado correctamente.')
            self.mostrar_usuarios()  # Refrescar la lista de usuarios
            self.frame_nuevo_usuario.destroy()  # Cerrar el formulario

        except Exception as e:
            messagebox.showerror('Error', f'Ocurrió un error al guardar el usuario: {str(e)}')

    def modificar_usuario(self):
        
        selected_item = self.tree_lista_usuarios.selection()

        if selected_item:

            item_values = self.tree_lista_usuarios.item(selected_item, 'values')
            self.ventana_modificar_usuario(item_values)

        else:
            messagebox.showwarning('Modificar Usuario', 'Por favor, selecciona un usuario para modificar.')

    def ventana_modificar_usuario(self, item_values):

        # Crear un nuevo frame para el formulario de modificación
        self.frame_modificar_usuario = tk.Toplevel(self)
        self.frame_modificar_usuario.title("Modificar Usuario")
        self.frame_modificar_usuario.geometry("400x300")
        self.frame_modificar_usuario.resizable(False, False)

        # Etiquetas y campos de entrada
        tk.Label(self.frame_modificar_usuario, text="Código").grid(row=0, column=0, padx=10, pady=10)
        self.txt_codigo_modificar = tk.Entry(self.frame_modificar_usuario)
        self.txt_codigo_modificar.grid(row=0, column=1, padx=10, pady=10)
        self.txt_codigo_modificar.insert(0, item_values[0])  # Cargar el valor existente
        self.txt_codigo_modificar.config(state='readonly')  # Hacer el código de solo lectura

        tk.Label(self.frame_modificar_usuario, text="Nombre").grid(row=1, column=0, padx=10, pady=10)
        self.txt_nombre_modificar = tk.Entry(self.frame_modificar_usuario)
        self.txt_nombre_modificar.grid(row=1, column=1, padx=10, pady=10)
        self.txt_nombre_modificar.insert(0, item_values[1])  # Cargar el valor existente

        tk.Label(self.frame_modificar_usuario, text="Clave").grid(row=2, column=0, padx=10, pady=10)
        self.txt_clave_modificar = tk.Entry(self.frame_modificar_usuario, show='*')
        self.txt_clave_modificar.grid(row=2, column=1, padx=10, pady=10)
        self.txt_clave_modificar.insert(0, item_values[2])  # Cargar el valor existente

        tk.Label(self.frame_modificar_usuario, text="Rol").grid(row=3, column=0, padx=10, pady=10)
        self.txt_rol_modificar = ttk.Combobox(self.frame_modificar_usuario, values=('Administrador', 'Almacen', 'Vendedor'))
        self.txt_rol_modificar.grid(row=3, column=1, padx=10, pady=10)
        self.txt_rol_modificar.set(item_values[3])  # Cargar el rol existente

        # Botón para guardar los cambios
        btn_guardar_modificacion = ttk.Button(self.frame_modificar_usuario, text='Guardar Cambios', 
                                            command=self.guardar_modificacion_usuario)  # Usar el código como identificador
        btn_guardar_modificacion.grid(row=4, column=0, columnspan=2, pady=20)

    def guardar_modificacion_usuario(self):

        try:
            # Obtener los datos del formulario
            codigo = self.txt_codigo_modificar.get()
            nombre = self.txt_nombre_modificar.get()
            clave = self.txt_clave_modificar.get()
            rol = self.txt_rol_modificar.get()

            # Conectar a la base de datos y actualizar el usuario
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('UPDATE Usuarios SET Nombre=?, Clave=?, Rol=? WHERE Codigo=?', 
                            (nombre, clave, rol, codigo))
            mi_conexion.commit()
            mi_conexion.close()

            messagebox.showinfo('Modificar Usuario', 'Usuario modificado correctamente.')
            self.mostrar_usuarios()  # Refrescar la lista de usuarios
            self.frame_modificar_usuario.destroy()  # Cerrar el formulario

        except Exception as e:
            messagebox.showerror('Error', f'Ocurrió un error al modificar el usuario: {str(e)}')

    def eliminar_usuario(self):
        
        selected_item = self.tree_lista_usuarios.selection()
        if selected_item:
            item_values = self.tree_lista_usuarios.item(selected_item, 'values')
            codigo_usuario = item_values[0]  # Obtener el código del usuario seleccionado

            # Confirmar la eliminación
            respuesta = messagebox.askyesno('Eliminar Usuario', f'¿Estás seguro de que deseas eliminar al usuario con código {codigo_usuario}?')
            if respuesta:
                try:
                    mi_conexion = sqlite3.connect('ventas.db')
                    mi_cursor = mi_conexion.cursor()
                    mi_cursor.execute('DELETE FROM Usuarios WHERE Codigo=?', (codigo_usuario,))
                    mi_conexion.commit()
                    mi_conexion.close()

                    messagebox.showinfo('Eliminar Usuario', 'Usuario eliminado correctamente.')
                    self.mostrar_usuarios()  # Refrescar la lista de usuarios
                except Exception as e:
                    messagebox.showerror('Error', f'Ocurrió un error al eliminar el usuario: {e}')
        else:
            messagebox.showwarning('Eliminar Usuario ', 'Por favor, selecciona un usuario para eliminar.')

     
    def ventana_reporte (self):

         # Limpiar el frame central
        for widget in self.frame_center.winfo_children():
            widget.destroy()

        # Título centrado para el Treeview
        lbl_titulo = tk.Label(self.frame_center, text="REPORTE DE EQUIPOS", font=('Arial', 20))
        lbl_titulo.pack(pady=10)

        # Configuración del Treeview
        self.tree_equipos = ttk.Treeview(self.frame_center, columns=("Equipo", "Serial", "Estado", "Problema"), show='headings')
        self.tree_equipos.pack(fill=tk.BOTH, expand=True)

        # Configuración de columnas
        self.tree_equipos.heading("Equipo", text="Equipo")
        self.tree_equipos.heading("Serial", text="Serial")
        self.tree_equipos.heading("Estado", text="Estado")
        self.tree_equipos.heading("Problema", text="Problema")

        # Centrar el texto en las columnas
        self.tree_equipos.column("Equipo", anchor='center')
        self.tree_equipos.column("Serial", anchor='center')
        self.tree_equipos.column("Estado", anchor='center')
        self.tree_equipos.column("Problema", anchor='center')

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_center, orient=tk.VERTICAL, command=self.tree_equipos.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_equipos.configure(yscrollcommand=self.scrollbar.set)

        # Cargar equipos al iniciar
        self.cargar_equipos()

        # Frame para los botones de gestión
        self.frame_botones = tk.Frame(self.frame_center)
        self.frame_botones.pack(pady=10)

        # Botones de gestión
        self.btn_agregar = ttk.Button(self.frame_botones, text="AGREGAR", bootstyle='succes', command=self.ventana_nuevo_equipo)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_modificar = ttk.Button(self.frame_botones, text="MODIFICAR", bootstyle='warning',command=self.modificar_equipo)
        self.btn_modificar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="ELIMINAR", bootstyle='danger',command=self.eliminar_equipo)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)


    def cargar_equipos(self):
        # Limpiar el Treeview
        for item in self.tree_equipos.get_children():
            self.tree_equipos.delete(item)

        # Conectar a la base de datos y obtener equipos
        try:
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('SELECT Equipo, Serial, Estado, Problema FROM Equipos')
            equipos = mi_cursor.fetchall()

            for equipo in equipos:
                self.tree_equipos.insert('', 'end', values=equipo)

            mi_conexion.close()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar los equipos: {str(e)}")

    def ventana_nuevo_equipo(self):

        # Crear un nuevo frame para el formulario
        self.frame_nuevo_equipo = tk.Toplevel(self)
        self.frame_nuevo_equipo.title("Nuevo Equipo")
        self.frame_nuevo_equipo.geometry("400x300")
        self.frame_nuevo_equipo.resizable(False, False)

        tk.Label(self.frame_nuevo_equipo, text="Equipo").grid(row=0, column=0, padx=10, pady=10)
        self.txt_equipo_nuevo = tk.Entry(self.frame_nuevo_equipo)
        self.txt_equipo_nuevo.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_equipo, text="Serial").grid(row=1, column=0, padx=10, pady=10)
        self.txt_serial_nuevo = tk.Entry(self.frame_nuevo_equipo)
        self.txt_serial_nuevo.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_equipo, text="Estado").grid(row=2, column=0, padx=10, pady=10)
        self.txt_estado_nuevo = tk.Entry(self.frame_nuevo_equipo)
        self.txt_estado_nuevo.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_nuevo_equipo, text="Problema").grid(row=3, column=0, padx=10, pady=10)
        self.txt_problema_nuevo = tk.Entry(self.frame_nuevo_equipo)
        self.txt_problema_nuevo.grid(row=3, column=1, padx=10, pady=10)

        # Botón para guardar el nuevo equipo
        btn_guardar_nuevo_equipo = ttk.Button(self.frame_nuevo_equipo, text='Guardar', command=self.guardar_equipo)
        btn_guardar_nuevo_equipo.grid(row=4, column=0, columnspan=2, pady=20)

    def guardar_equipo(self):
        try:
            # Obtener los datos del formulario
            equipo = self.txt_equipo_nuevo.get()
            serial = self.txt_serial_nuevo.get()
            estado = self.txt_estado_nuevo.get()
            problema = self.txt_problema_nuevo.get()

            # Conectar a la base de datos y guardar el nuevo equipo
            mi_conexion = sqlite3.connect('ventas.db')
            mi_cursor = mi_conexion.cursor()
            mi_cursor.execute('INSERT INTO Equipos (Equipo, Serial, Estado, Problema) VALUES (?, ?, ?, ?)', 
                              (equipo, serial, estado, problema))
            mi_conexion.commit()
            mi_conexion.close()

            messagebox.showinfo('Guardar Equipo', 'Equipo guardado correctamente.')
            self.cargar_equipos()  # Refrescar la lista de equipos
            self.frame_nuevo_equipo.destroy()  # Cerrar el formulario

        except Exception as e:
            messagebox.showerror('Error', f'Ocurrió un error al guardar el equipo: {str(e)}')

    def modificar_equipo(self):

        selected_item = self.tree_equipos.selection()
        if selected_item:
            item_values = self.tree_equipos.item(selected_item, 'values')
            self.ventana_modificar_equipo(item_values)
        else:
            messagebox.showwarning('Modificar Equipo', 'Por favor, selecciona un equipo para modificar.')

    def ventana_modificar_equipo(self, item_values):

        # Crear un nuevo frame para el formulario de modificación
        self.frame_modificar_equipo = tk.Toplevel(self)
        self.frame_modificar_equipo.title("Modificar Equipo")
        self.frame_modificar_equipo.geometry("400x300")
        self.frame_modificar_equipo.resizable(False, False)

        # Etiquetas y campos de entrada
        tk.Label(self.frame_modificar_equipo, text="Equipo").grid(row=0, column=0, padx=10, pady=10)
        self.txt_equipo_modificar = tk.Entry(self.frame_modificar_equipo)
        self.txt_equipo_modificar.grid(row=0, column=1, padx=10, pady=10)
        self.txt_equipo_modificar.insert(0, item_values[0])  # Cargar el valor existente

        tk.Label(self.frame_modificar_equipo, text="Serial").grid(row=1, column=0, padx=10, pady=10)
        self.txt_serial_modificar = tk.Entry(self.frame_modificar_equipo)
        self.txt_serial_modificar.grid(row=1, column=1, padx=10, pady=10)
        self.txt_serial_modificar.insert(0, item_values[1])  # Cargar el valor existente

        tk.Label(self.frame_modificar_equipo, text="Estado").grid(row=2, column=0, padx=10, pady=10)
        self.txt_estado_modificar = tk.Entry(self.frame_modificar_equipo)
        self.txt_estado_modificar.grid(row=2, column=1, padx=10, pady=10)
        self.txt_estado_modificar.insert(0, item_values[2])

        tk.Label(self.frame_modificar_equipo, text="Problema").grid(row=3, column=0, padx=10, pady=10)
        self.txt_problema_modificar = tk.Entry(self.frame_modificar_equipo)
        self.txt_problema_modificar.grid(row=3, column=1, padx=10, pady=10)
        self.txt_problema_modificar.insert(0, item_values[3])  # Cargar el valor existente

        # Botón para guardar los cambios
        btn_guardar_modificacion = ttk.Button(self.frame_modificar_equipo, text='Guardar Cambios', command=lambda: self.guardar_modificacion(item_values[1]))  # Usar el serial como identificador
        btn_guardar_modificacion.grid(row=5, column=0, columnspan=2, pady=20)

    def guardar_modificacion(self, serial_original):
            
        try:
                
            # Obtener los datos del formulario
                equipo = self.txt_equipo_modificar.get()
                serial = self.txt_serial_modificar.get()
                estado = self.txt_estado_modificar.get()
                problema = self.txt_problema_modificar.get()

                # Conectar a la base de datos y actualizar el equipo
                mi_conexion = sqlite3.connect('ventas.db')
                mi_cursor = mi_conexion.cursor()
                mi_cursor.execute('UPDATE Equipos SET Equipo=?, Serial=?, Estado=?, Problema=? WHERE Serial=?', 
                                (equipo, serial, estado, problema, serial_original))
                mi_conexion.commit()
                mi_conexion.close()

                messagebox.showinfo('Modificar Equipo', 'Equipo modificado correctamente.')
                self.cargar_equipos()  # Refrescar la lista de equipos
                self.frame_modificar_equipo.destroy()  # Cerrar el formulario

        except Exception as e:
                messagebox.showerror('Error', f'Ocurrió un error al modificar el equipo: {str(e)}')

    def eliminar_equipo(self):
        selected_item = self.tree_equipos.selection()
        if selected_item:
            item_values = self.tree_equipos.item(selected_item, 'values')
            serial_equipo = item_values[1]  # Obtener el serial del equipo seleccionado

            # Confirmar la eliminación
            respuesta = messagebox.askyesno('Eliminar Equipo', f'¿Estás seguro de que deseas eliminar el equipo con serial {serial_equipo}?')
            if respuesta:
                try:
                    mi_conexion = sqlite3.connect('ventas.db')
                    mi_cursor = mi_conexion.cursor()
                    mi_cursor.execute('DELETE FROM Equipos WHERE Serial=?', (serial_equipo,))
                    mi_conexion.commit()
                    mi_conexion.close()

                    messagebox.showinfo('Eliminar Equipo', 'Equipo eliminado correctamente.')
                    self.cargar_equipos()  # Refrescar la lista de equipos
                except Exception as e:
                    messagebox.showerror('Error', f'Ocurrió un error al eliminar el equipo: {e}')
        else:
            messagebox.showwarning('Eliminar Equipo', 'Por favor, selecciona un equipo para eliminar.')

def main():

        app = ventana()
        app.title('BD VENTAS') 
        app.state('zoomed')
        app.mainloop()

if __name__=='__main__':
    main() 