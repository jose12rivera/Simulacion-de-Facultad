import tkinter as tk
from tkinter import ttk, messagebox
import math

class StudentFlowSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Simulador de Flujo de Estudiantes - Universidad")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f4f8")
        
        # Parámetros del sistema
        self.params = {
            'x': 100,  # Alumnos que entran por año
            'a1': 60,  # % pasan a segundo del primer año
            'b1': 20,  # % abandonan del primer año
            'c1': 20,  # % repiten del primer año
            'ai': 70,  # % pasan al siguiente del i-ésimo año
            'bi': 15,  # % abandonan del i-ésimo año
            'ci': 15,  # % repiten del i-ésimo año
            'total_years': 5  # Duración de la carrera
        }
        
        # Estado de la simulación
        self.reset_simulation()
        self.is_running = False
        self.animation_speed = 500
        self.show_config = False
        
        self.create_widgets()
        self.update_display()
        
    def reset_simulation(self):
        self.year = 0
        # Inicializar cada año con 0 estudiantes
        self.students_per_year = [0] * (self.params['total_years'] + 1)  # +1 para graduados
        self.total_enrolled = 0
        self.total_graduated = 0
        self.total_dropped = 0
        
        self.history = {
            'year': [],
            'year1': [],
            'year2': [],
            'year3': [],
            'year4': [],
            'year5': [],
            'graduated': [],
            'dropped': [],
            'total': []
        }
        
    def create_widgets(self):
        # Frame principal con scroll
        main_canvas = tk.Canvas(self.root, bg="#f0f4f8", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        
        main_frame = tk.Frame(main_canvas, bg="#f0f4f8")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        canvas_frame = main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        def configure_scroll(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            main_canvas.itemconfig(canvas_frame, width=event.width)
            
        main_frame.bind("<Configure>", configure_scroll)
        main_canvas.bind("<Configure>", configure_scroll)
        
        # Header
        self.create_header(main_frame)
        
        # Alertas
        self.alert_frame = tk.Frame(main_frame, bg="#fef2f2", relief=tk.RIDGE, bd=2)
        self.alert_label = tk.Label(self.alert_frame, text="", bg="#fef2f2", 
                                    fg="#991b1b", font=("Arial", 10, "bold"), 
                                    justify=tk.LEFT, wraplength=1300)
        self.alert_label.pack(padx=15, pady=10)
        
        # Estadísticas generales
        general_stats_frame = tk.Frame(main_frame, bg="#f0f4f8")
        general_stats_frame.pack(fill=tk.X, pady=10)
        self.create_general_stats(general_stats_frame)
        
        # Configuración
        self.config_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        self.create_config_panel()
        
        # Estadísticas por año
        year_stats_frame = tk.Frame(main_frame, bg="#f0f4f8")
        year_stats_frame.pack(fill=tk.X, pady=10)
        self.create_year_stats(year_stats_frame)
        
        # Gráfico de flujo
        flow_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        flow_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.create_flow_diagram(flow_frame)
        
        # Gráfico de evolución
        graph_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.create_evolution_graph(graph_frame)
        
        # Tabla de historial
        history_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.create_history_table(history_frame)
        
        # Análisis
        analysis_frame = tk.Frame(main_frame, bg="white", relief=tk.RIDGE, bd=2)
        analysis_frame.pack(fill=tk.X, pady=10)
        self.create_analysis_panel(analysis_frame)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_frame = tk.Frame(header_frame, bg="white")
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        title = tk.Label(title_frame, text="🎓 Simulador de Flujo de Estudiantes", 
                        bg="white", fg="#1e293b", font=("Arial", 20, "bold"))
        title.pack(anchor=tk.W)
        
        subtitle = tk.Label(title_frame, text="Planificación de Salas y Recursos Universitarios", 
                           bg="white", fg="#64748b", font=("Arial", 11))
        subtitle.pack(anchor=tk.W)
        
        self.year_label = tk.Label(title_frame, text="Año Académico: 0", 
                                  bg="white", fg="#2563eb", font=("Arial", 13, "bold"))
        self.year_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Botones
        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.play_button = tk.Button(button_frame, text="▶ Iniciar Simulación", 
                                     command=self.toggle_simulation,
                                     bg="#10b981", fg="white", font=("Arial", 11, "bold"),
                                     padx=25, pady=10, cursor="hand2", relief=tk.FLAT,
                                     borderwidth=0)
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = tk.Button(button_frame, text="↻ Reiniciar", 
                                command=self.reset_button_click,
                                bg="#6b7280", fg="white", font=("Arial", 11, "bold"),
                                padx=25, pady=10, cursor="hand2", relief=tk.FLAT,
                                borderwidth=0)
        reset_button.pack(side=tk.LEFT, padx=5)
        
        self.config_button = tk.Button(button_frame, text="⚙ Configurar", 
                                       command=self.toggle_config,
                                       bg="#3b82f6", fg="white", font=("Arial", 11, "bold"),
                                       padx=25, pady=10, cursor="hand2", relief=tk.FLAT,
                                       borderwidth=0)
        self.config_button.pack(side=tk.LEFT, padx=5)
        
    def create_general_stats(self, parent):
        # Total matriculados
        enrolled_frame = tk.Frame(parent, bg="#3b82f6", relief=tk.FLAT, bd=0)
        enrolled_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(enrolled_frame, text="📚 Total Matriculados", bg="#3b82f6", fg="white", 
                font=("Arial", 13, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.enrolled_value = tk.Label(enrolled_frame, text="0", bg="#3b82f6", fg="white", 
                                      font=("Arial", 36, "bold"))
        self.enrolled_value.pack(anchor=tk.W, padx=20)
        
        self.enrolled_detail = tk.Label(enrolled_frame, text="estudiantes activos", 
                                       bg="#3b82f6", fg="white", font=("Arial", 10))
        self.enrolled_detail.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Graduados
        graduated_frame = tk.Frame(parent, bg="#10b981", relief=tk.FLAT, bd=0)
        graduated_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(graduated_frame, text="🎉 Graduados", bg="#10b981", fg="white", 
                font=("Arial", 13, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.graduated_value = tk.Label(graduated_frame, text="0", bg="#10b981", fg="white", 
                                       font=("Arial", 36, "bold"))
        self.graduated_value.pack(anchor=tk.W, padx=20)
        
        self.graduated_detail = tk.Label(graduated_frame, text="completaron la carrera", 
                                        bg="#10b981", fg="white", font=("Arial", 10))
        self.graduated_detail.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Desertores
        dropped_frame = tk.Frame(parent, bg="#ef4444", relief=tk.FLAT, bd=0)
        dropped_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(dropped_frame, text="⚠️ Renunciados", bg="#ef4444", fg="white", 
                font=("Arial", 13, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.dropped_value = tk.Label(dropped_frame, text="0", bg="#ef4444", fg="white", 
                                     font=("Arial", 36, "bold"))
        self.dropped_value.pack(anchor=tk.W, padx=20)
        
        self.dropped_detail = tk.Label(dropped_frame, text="abandonaron los estudios", 
                                      bg="#ef4444", fg="white", font=("Arial", 10))
        self.dropped_detail.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Tasa de retención
        retention_frame = tk.Frame(parent, bg="#8b5cf6", relief=tk.FLAT, bd=0)
        retention_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(retention_frame, text="📊 Tasa de Retención", bg="#8b5cf6", fg="white", 
                font=("Arial", 13, "bold")).pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.retention_value = tk.Label(retention_frame, text="0%", bg="#8b5cf6", fg="white", 
                                       font=("Arial", 36, "bold"))
        self.retention_value.pack(anchor=tk.W, padx=20)
        
        self.retention_detail = tk.Label(retention_frame, text="estudiantes que continúan", 
                                        bg="#8b5cf6", fg="white", font=("Arial", 10))
        self.retention_detail.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
    def create_year_stats(self, parent):
        container = tk.Frame(parent, bg="#f0f4f8")
        container.pack(fill=tk.X)
        
        self.year_cards = []
        colors = ["#06b6d4", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"]
        
        for i in range(self.params['total_years']):
            frame = tk.Frame(container, bg=colors[i], relief=tk.FLAT, bd=0)
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            title = tk.Label(frame, text=f"📖 Año {i+1}", bg=colors[i], fg="white", 
                           font=("Arial", 12, "bold"))
            title.pack(anchor=tk.W, padx=15, pady=(12, 5))
            
            value = tk.Label(frame, text="0", bg=colors[i], fg="white", 
                           font=("Arial", 28, "bold"))
            value.pack(anchor=tk.W, padx=15)
            
            detail = tk.Label(frame, text="estudiantes", bg=colors[i], fg="white", 
                            font=("Arial", 9))
            detail.pack(anchor=tk.W, padx=15, pady=(0, 12))
            
            self.year_cards.append(value)
            
    def create_config_panel(self):
        title = tk.Label(self.config_frame, text="⚙️ Configuración de Parámetros", 
                        bg="white", fg="#1e293b", font=("Arial", 15, "bold"))
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        grid_frame = tk.Frame(self.config_frame, bg="white")
        grid_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        configs = [
            ("Estudiantes nuevos por año (x):", 'x', 0, 0),
            ("% Primer año → Segundo (a1):", 'a1', 0, 1),
            ("% Primer año abandona (b1):", 'b1', 0, 2),
            ("% Primer año repite (c1):", 'c1', 0, 3),
            ("% Año i → Siguiente (ai):", 'ai', 1, 0),
            ("% Año i abandona (bi):", 'bi', 1, 1),
            ("% Año i repite (ci):", 'ci', 1, 2),
            ("Duración de la carrera (años):", 'total_years', 1, 3),
        ]
        
        self.config_entries = {}
        
        for label_text, key, row, col in configs:
            frame = tk.Frame(grid_frame, bg="white")
            frame.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
            
            label = tk.Label(frame, text=label_text, bg="white", fg="#475569", 
                           font=("Arial", 9, "bold"))
            label.pack(anchor=tk.W)
            
            entry = tk.Entry(frame, font=("Arial", 11), relief=tk.SOLID, bd=1, 
                           bg="#f8fafc", fg="#1e293b")
            entry.insert(0, str(self.params[key]))
            entry.pack(fill=tk.X)
            
            self.config_entries[key] = entry
        
        for col in range(4):
            grid_frame.columnconfigure(col, weight=1)
            
        note = tk.Label(self.config_frame, 
                       text="💡 Nota: Los porcentajes a1+b1+c1 y ai+bi+ci deben sumar 100%", 
                       bg="white", fg="#64748b", font=("Arial", 9, "italic"))
        note.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
    def create_flow_diagram(self, parent):
        title = tk.Label(parent, text="🔄 Diagrama de Flujo de Estudiantes", 
                        bg="white", fg="#1e293b", font=("Arial", 15, "bold"))
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        self.flow_canvas = tk.Canvas(parent, bg="#f8fafc", height=300, 
                                     highlightthickness=1, highlightbackground="#e2e8f0")
        self.flow_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
    def create_evolution_graph(self, parent):
        title = tk.Label(parent, text="📈 Evolución de Estudiantes por Año", 
                        bg="white", fg="#1e293b", font=("Arial", 15, "bold"))
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        self.graph_canvas = tk.Canvas(parent, bg="#f8fafc", height=300, 
                                      highlightthickness=1, highlightbackground="#e2e8f0")
        self.graph_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
    def create_history_table(self, parent):
        title = tk.Label(parent, text="📋 Historial Detallado por Año Académico", 
                        bg="white", fg="#1e293b", font=("Arial", 15, "bold"))
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        table_frame = tk.Frame(parent, bg="white")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(table_frame, height=10, wrap=tk.NONE, 
                                   font=("Courier", 9), yscrollcommand=scrollbar.set,
                                   bg="#f8fafc", relief=tk.FLAT, fg="#1e293b")
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.history_text.yview)
        
        header = f"{'Año':>4} | {'1er':>5} | {'2do':>5} | {'3er':>5} | {'4to':>5} | {'5to':>5} | {'Grad':>6} | {'Desert':>7} | {'Total':>6}\n"
        header += "-" * 70 + "\n"
        self.history_text.insert(tk.END, header)
        
    def create_analysis_panel(self, parent):
        title = tk.Label(parent, text="💡 Análisis y Recomendaciones de Planificación", 
                        bg="white", fg="#1e293b", font=("Arial", 15, "bold"))
        title.pack(anchor=tk.W, padx=20, pady=(15, 10))
        
        self.analysis_text = tk.Text(parent, height=7, wrap=tk.WORD, 
                                    font=("Arial", 10), relief=tk.FLAT, bg="#f8fafc",
                                    fg="#334155")
        self.analysis_text.pack(fill=tk.X, padx=20, pady=(0, 15))
        
    def update_flow_diagram(self):
        self.flow_canvas.delete("all")
        
        width = self.flow_canvas.winfo_width()
        height = self.flow_canvas.winfo_height()
        
        if width <= 1:
            return
            
        # Configuración
        box_width = 120
        box_height = 80
        spacing = (width - box_width * self.params['total_years']) / (self.params['total_years'] + 1)
        y_center = height // 2
        
        colors = ["#06b6d4", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"]
        
        # Dibujar cajas de cada año
        for i in range(self.params['total_years']):
            x = spacing * (i + 1) + box_width * i
            
            # Caja principal
            self.flow_canvas.create_rectangle(x, y_center - box_height//2, 
                                             x + box_width, y_center + box_height//2,
                                             fill=colors[i], outline=colors[i], width=2)
            
            # Texto
            self.flow_canvas.create_text(x + box_width//2, y_center - 20,
                                        text=f"Año {i+1}", fill="white", 
                                        font=("Arial", 11, "bold"))
            
            self.flow_canvas.create_text(x + box_width//2, y_center + 5,
                                        text=f"{int(self.students_per_year[i])}", 
                                        fill="white", font=("Arial", 20, "bold"))
            
            self.flow_canvas.create_text(x + box_width//2, y_center + 25,
                                        text="estudiantes", fill="white", 
                                        font=("Arial", 8))
            
            # Flechas hacia el siguiente año
            if i < self.params['total_years'] - 1:
                arrow_start_x = x + box_width
                arrow_end_x = x + box_width + spacing
                
                # Flecha de avance
                self.flow_canvas.create_line(arrow_start_x, y_center - 15,
                                            arrow_end_x, y_center - 15,
                                            arrow=tk.LAST, fill="#10b981", width=3)
                
                percent = self.params['a1'] if i == 0 else self.params['ai']
                self.flow_canvas.create_text((arrow_start_x + arrow_end_x)//2, 
                                            y_center - 30,
                                            text=f"Pasan {percent}%", fill="#10b981", 
                                            font=("Arial", 8, "bold"))
                
                # Flecha de repetición (curva)
                self.flow_canvas.create_arc(x + 20, y_center + box_height//2,
                                           x + box_width - 20, y_center + box_height//2 + 40,
                                           start=0, extent=180, style=tk.ARC,
                                           outline="#f59e0b", width=2)
                
                percent_repeat = self.params['c1'] if i == 0 else self.params['ci']
                self.flow_canvas.create_text(x + box_width//2, y_center + box_height//2 + 50,
                                            text=f"Repiten {percent_repeat}%", 
                                            fill="#f59e0b", font=("Arial", 8, "bold"))
                
                # Flecha de abandono (hacia abajo)
                self.flow_canvas.create_line(x + box_width//2, y_center + box_height//2,
                                            x + box_width//2, height - 30,
                                            arrow=tk.LAST, fill="#ef4444", width=2)
                
                percent_drop = self.params['b1'] if i == 0 else self.params['bi']
                self.flow_canvas.create_text(x + box_width//2 + 40, height - 40,
                                            text=f"Abandonan {percent_drop}%", 
                                            fill="#ef4444", font=("Arial", 8, "bold"))
            else:
                # Flecha de graduación
                grad_x = x + box_width + 50
                self.flow_canvas.create_line(x + box_width, y_center,
                                            grad_x, y_center,
                                            arrow=tk.LAST, fill="#10b981", width=4)
                
                self.flow_canvas.create_text(grad_x + 50, y_center,
                                            text=f"🎓\n{int(self.total_graduated)}\nGraduados", 
                                            fill="#10b981", font=("Arial", 10, "bold"),
                                            justify=tk.CENTER)
        
    def update_evolution_graph(self):
        self.graph_canvas.delete("all")
        
        if len(self.history['year']) < 2:
            return
            
        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()
        
        if width <= 1:
            return
        
        padding = 50
        graph_width = width - 2 * padding
        graph_height = height - 2 * padding
        
        years_to_show = min(20, len(self.history['year']))
        years = self.history['year'][-years_to_show:]
        
        # Encontrar valores máximos
        max_students = max([max(self.history[f'year{i}'][-years_to_show:]) 
                           for i in range(1, 6)] + [1])
        
        # Ejes
        self.graph_canvas.create_line(padding, padding, padding, height - padding,
                                      fill="#475569", width=2)
        self.graph_canvas.create_line(padding, height - padding, width - padding,
                                      height - padding, fill="#475569", width=2)
        
        # Líneas para cada año
        colors = ["#06b6d4", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"]
        names = ["1er Año", "2do Año", "3er Año", "4to Año", "5to Año"]
        
        legend_x = width - 150
        legend_y = padding + 20
        
        for idx in range(1, 6):
            data = self.history[f'year{idx}'][-years_to_show:]
            points = []
            
            for i, val in enumerate(data):
                x = padding + (i / (years_to_show - 1)) * graph_width if years_to_show > 1 else padding
                y = height - padding - (val / max_students) * graph_height if max_students > 0 else height - padding
                points.extend([x, y])
            
            if len(points) >= 4:
                self.graph_canvas.create_line(points, fill=colors[idx-1], width=2, smooth=True)
            
            # Leyenda
            self.graph_canvas.create_line(legend_x, legend_y, legend_x + 30, legend_y,
                                         fill=colors[idx-1], width=3)
            self.graph_canvas.create_text(legend_x + 35, legend_y, text=names[idx-1],
                                         anchor=tk.W, fill=colors[idx-1], 
                                         font=("Arial", 9, "bold"))
            legend_y += 25
        
        # Etiquetas
        self.graph_canvas.create_text(padding - 25, padding, text=str(int(max_students)),
                                      anchor=tk.E, font=("Arial", 9))
        self.graph_canvas.create_text(padding - 25, height - padding, text="0",
                                      anchor=tk.E, font=("Arial", 9))
        
        if years:
            self.graph_canvas.create_text(padding, height - padding + 25, 
                                         text=f"Año {years[0]}",
                                         anchor=tk.W, font=("Arial", 9))
            self.graph_canvas.create_text(width - padding, height - padding + 25,
                                         text=f"Año {years[-1]}",
                                         anchor=tk.E, font=("Arial", 9))
        
    def simulate_year(self):
        # Guardar estado actual en historial
        self.history['year'].append(self.year)
        for i in range(1, 6):
            self.history[f'year{i}'].append(self.students_per_year[i-1])
        self.history['graduated'].append(self.total_graduated)
        self.history['dropped'].append(self.total_dropped)
        self.history['total'].append(self.total_enrolled)
        
        # Nuevo arreglo para el próximo año
        new_students = [0] * self.params['total_years']
        
        # Procesar cada año de estudio
        for i in range(self.params['total_years']):
            current = self.students_per_year[i]
            
            if i == 0:  # Primer año
                # Nuevos ingresos
                new_students[0] += self.params['x']
                
                # Estudiantes del año anterior
                pass_rate = self.params['a1'] / 100
                repeat_rate = self.params['c1'] / 100
                drop_rate = self.params['b1'] / 100
                
                if i + 1 < self.params['total_years']:
                    new_students[i + 1] += current * pass_rate
                else:
                    self.total_graduated += current * pass_rate
                    
                new_students[i] += current * repeat_rate
                self.total_dropped += current * drop_rate
                
            else:  # Años posteriores
                pass_rate = self.params['ai'] / 100
                repeat_rate = self.params['ci'] / 100
                drop_rate = self.params['bi'] / 100
                
                if i + 1 < self.params['total_years']:
                    new_students[i + 1] += current * pass_rate
                else:
                    self.total_graduated += current * pass_rate
                    
                new_students[i] += current * repeat_rate
                self.total_dropped += current * drop_rate
        
        # Actualizar estudiantes
        self.students_per_year = new_students
        self.total_enrolled = sum(new_students)
        self.year += 1
        
        # Agregar fila a la tabla
        row = f"{self.year:>4} |"
        for i in range(5):
            row += f" {int(self.students_per_year[i]):>5} |"
        row += f" {int(self.total_graduated):>6} | {int(self.total_dropped):>7} | {int(self.total_enrolled):>6}\n"
        self.history_text.insert(tk.END, row)
        self.history_text.see(tk.END)
        
    def check_alerts(self):
        alerts = []
        
        # Verificar capacidad por año
        for i in range(self.params['total_years']):
            if self.students_per_year[i] > self.params['x'] * 2:
                alerts.append(f"⚠️ SOBRECAPACIDAD en {i+1}° año: {int(self.students_per_year[i])} estudiantes")
        
        # Tasa de deserción alta
        if self.year > 0 and self.total_enrolled > 0:
            drop_rate = (self.total_dropped / (self.total_dropped + self.total_enrolled)) * 100
            if drop_rate > 30:
                alerts.append(f"🔴 ALTA DESERCIÓN: {drop_rate:.1f}% de estudiantes han abandonado")
        
        # Graduación baja
        if self.year >= self.params['total_years']:
            expected_grads = self.params['x'] * self.year / self.params['total_years']
            if self.total_graduated < expected_grads * 0.5:
                alerts.append(f"📉 BAJA GRADUACIÓN: Solo {int(self.total_graduated)} graduados vs {int(expected_grads)} esperados")
        
        if alerts:
            self.alert_frame.pack(fill=tk.X, pady=(0, 10), before=self.alert_frame.master.winfo_children()[2])
            self.alert_label.config(text="⚠️ ALERTAS DEL SISTEMA:\n" + "\n".join(alerts))
        else:
            self.alert_frame.pack_forget()
            
    def update_analysis(self):
        self.analysis_text.delete(1.0, tk.END)
        
        if self.year == 0:
            self.analysis_text.insert(tk.END, 
                "ℹ️ Presiona 'Iniciar Simulación' para comenzar a proyectar el flujo de estudiantes.\n\n"
                "Esta herramienta te ayudará a:\n"
                "• Planificar la cantidad de salas necesarias por año\n"
                "• Estimar recursos docentes y administrativos\n"
                "• Proyectar tasas de graduación y deserción\n"
                "• Optimizar la capacidad de la institución")
            return
        
        recommendations = []
        
        # Análisis de capacidad
        max_students = max(self.students_per_year[:self.params['total_years']])
        recommendations.append(f"📊 CAPACIDAD MÁXIMA: El año con más estudiantes tiene {int(max_students)} alumnos.")
        
        # Salas necesarias (asumiendo 30 estudiantes por sala)
        total_rooms_needed = sum([math.ceil(s / 30) for s in self.students_per_year[:self.params['total_years']]])
        recommendations.append(f"🏫 SALAS NECESARIAS: Se requieren aproximadamente {total_rooms_needed} salas simultáneas (30 estudiantes/sala).")
        
        # Análisis de deserción
        if self.total_enrolled + self.total_dropped > 0:
            retention_rate = (self.total_enrolled / (self.total_enrolled + self.total_dropped)) * 100
            if retention_rate < 60:
                recommendations.append(f"🚨 CRÍTICO: Tasa de retención del {retention_rate:.1f}%. Se requieren programas de apoyo estudiantil urgentes.")
            elif retention_rate < 75:
                recommendations.append(f"⚠️ ATENCIÓN: Tasa de retención del {retention_rate:.1f}%. Considere implementar tutorías y seguimiento.")
            else:
                recommendations.append(f"✅ BUENO: Tasa de retención del {retention_rate:.1f}%. El sistema mantiene a la mayoría de estudiantes.")
        
        # Proyección de graduados
        if self.year >= self.params['total_years']:
            grad_rate = (self.total_graduated / (self.params['x'] * (self.year - self.params['total_years'] + 1))) * 100
            if grad_rate > 50:
                recommendations.append(f"🎓 EXCELENTE: Tasa de graduación del {grad_rate:.1f}%. El sistema es efectivo.")
            else:
                recommendations.append(f"📉 MEJORABLE: Tasa de graduación del {grad_rate:.1f}%. Revisar factores que impiden la graduación.")
        
        # Tendencia de crecimiento
        if len(self.history['total']) > 5:
            recent_avg = sum(self.history['total'][-5:]) / 5
            old_avg = sum(self.history['total'][-10:-5]) / 5 if len(self.history['total']) >= 10 else recent_avg
            
            if recent_avg > old_avg * 1.1:
                recommendations.append(f"📈 CRECIMIENTO: La matrícula está aumentando. Planificar expansión de infraestructura.")
            elif recent_avg < old_avg * 0.9:
                recommendations.append(f"📉 DECRECIMIENTO: La matrícula está disminuyendo. Investigar causas y tomar medidas.")
        
        for rec in recommendations:
            self.analysis_text.insert(tk.END, rec + "\n\n")
            
    def update_display(self):
        self.year_label.config(text=f"Año Académico: {self.year}")
        
        # Estadísticas generales
        self.enrolled_value.config(text=str(int(self.total_enrolled)))
        self.graduated_value.config(text=str(int(self.total_graduated)))
        self.dropped_value.config(text=str(int(self.total_dropped)))
        
        # Tasa de retención
        if self.total_enrolled + self.total_dropped > 0:
            retention = (self.total_enrolled / (self.total_enrolled + self.total_dropped)) * 100
            self.retention_value.config(text=f"{retention:.1f}%")
        else:
            self.retention_value.config(text="0%")
        
        # Estadísticas por año
        for i in range(min(self.params['total_years'], len(self.year_cards))):
            self.year_cards[i].config(text=str(int(self.students_per_year[i])))
        
        self.check_alerts()
        self.update_flow_diagram()
        self.update_evolution_graph()
        self.update_analysis()
        
    def toggle_simulation(self):
        self.is_running = not self.is_running
        
        if self.is_running:
            self.play_button.config(text="⏸ Pausar", bg="#f59e0b")
            self.run_simulation()
        else:
            self.play_button.config(text="▶ Iniciar Simulación", bg="#10b981")
            
    def run_simulation(self):
        if self.is_running:
            self.simulate_year()
            self.update_display()
            self.root.after(self.animation_speed, self.run_simulation)
            
    def reset_button_click(self):
        self.is_running = False
        self.play_button.config(text="▶ Iniciar Simulación", bg="#10b981")
        
        # Actualizar parámetros
        try:
            for key, entry in self.config_entries.items():
                value = entry.get()
                self.params[key] = float(value) if '.' in value else int(value)
            
            # Validar porcentajes
            if abs((self.params['a1'] + self.params['b1'] + self.params['c1']) - 100) > 0.1:
                messagebox.showwarning("Advertencia", 
                    "Los porcentajes del primer año (a1+b1+c1) deben sumar 100%")
            
            if abs((self.params['ai'] + self.params['bi'] + self.params['ci']) - 100) > 0.1:
                messagebox.showwarning("Advertencia", 
                    "Los porcentajes de años siguientes (ai+bi+ci) deben sumar 100%")
                
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
            return
            
        self.reset_simulation()
        
        # Limpiar historial
        self.history_text.delete(1.0, tk.END)
        header = f"{'Año':>4} | {'1er':>5} | {'2do':>5} | {'3er':>5} | {'4to':>5} | {'5to':>5} | {'Grad':>6} | {'Desert':>7} | {'Total':>6}\n"
        header += "-" * 70 + "\n"
        self.history_text.insert(tk.END, header)
        
        # Recrear cards si cambia duración
        self.update_display()
        
    def toggle_config(self):
        if self.show_config:
            self.config_frame.pack_forget()
            self.config_button.config(text="⚙ Configurar")
            self.show_config = False
        else:
            self.config_frame.pack(fill=tk.X, pady=10, before=self.config_frame.master.winfo_children()[3])
            self.config_button.config(text="⚙ Ocultar Config")
            self.show_config = True

def main():
    root = tk.Tk()
    app = StudentFlowSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
