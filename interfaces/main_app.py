import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar
from datetime import datetime
from service.item_service import ItemService
from datetime import timedelta

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reloj y Agenda Personal")
        self.service = ItemService()


        self.root.geometry("600x400")
        self.root.resizable(False, False)
        self.selected_date =datetime.now().strftime("%Y-%m-%d")

        #Mi Reloj
        self.clock_label =tk.Label(root, font=('Helvetica', 16), bg='black', fg='white')
        self.clock_label.pack(fill=tk.X)
        self.update_clock()

        #Frame para mi calendario y mi agenda
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Mi Calendario
        self.calendar = Calendar(self.main_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)
        self.calendar.pack(side=tk.LEFT, padx=(0,10))

        # Mi Agenda
        self.agenda_frame = tk.Frame(self.main_frame)
        self.agenda_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.toggle_button = tk.Button(root, text="Ocultar Agenda", command=self.toggle_agenda)
        self.toggle_button.pack(pady=(0,10))

        #Mis tareas
        self.task_listbox = tk.Listbox(self.main_frame)
        self.task_listbox.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.agenda_frame)
        btn_frame.pack(pady=5)

        add_btn = tk.Button(btn_frame, text= "Agregar", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = tk.Button(btn_frame, text="Modificar", command=self.edit_task)
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(btn_frame, text="Eliminar", command=self.delete_task)
        delete_btn.pack(side=tk.LEFT, padx=5)

        self.time_entry = tk.Entry(self.agenda_frame)
        self.time_entry.pack(pady=5)
        self.time_entry.insert(0, "HH:MM")

        self.check_pending_tasks()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def on_date_selected(self, event):
        self.selected_date = self.calendar.get_date()
        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0,tk.END)
        tasks = self.service.get_items(self.selected_date)
        for task in tasks:
            self.task_listbox.insert(tk.END, task)

    def add_task(self):
        task = simpledialog.askstring("Nueva Tarea", "Descripción de la tarea:")
        if task:
            self.service.add_item(self.selected_date, task)
            self.load_tasks()
        else:
            messagebox.showwarning("Advertencia", "El campo de tarea está vacío.")
    
    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            current_task = self.task_listbox.get(selected_index)
            new_task = simpledialog.askstring("Modificar Tarea", "Descripcion de la tarea: ", initialvalue=current_task)
            if new_task:
                self.service.update_item(self.selected_date, selected_index[0], new_task)
                self.load_tasks()
    
    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            confirm = messagebox.askyesno("Eliminar", "¿Estás seguro de eliminar la tarea seleccionada?")
            if confirm:
                self.service.delete_item(self.selected_date, selected_index[0])
                self.load_tasks()
        else:
            messagebox.showwarning("Seleccionar", "Selecciona una tarea para eliminar.")

    def toggle_agenda(self):
        if self.agenda_frame.winfo_viewable():
            self.agenda_frame.pack_forget()
            self.toggle_button.config(text="Mostrar Agenda")
        else:
            self.agenda_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.toggle_button.config(text="Ocultar Agenda")

    def check_pending_tasks(self):
        now = datetime.now()
        tasks = self.service.get_all_items()
        for task, date_str in tasks:
            try:
                task_time_str = task.split('|')[1] if '|' in task else ""
                task_datetime_str = f"{date_str} {task_time_str}"
                task_datetime = datetime.strptime(task_datetime_str, "%Y-%m-%d %H:%M")
                if task_datetime - timedelta(minutes=30) <= now < task_datetime:
                    messagebox.showinfo("Recordatorio", f"Tienes una tarea pendiente: {task.split('|')[0]}")
            except (IndexError, ValueError):
                pass