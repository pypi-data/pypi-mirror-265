import dearpygui.dearpygui as dpg
from types import NoneType
from typing import List, Tuple
from collections import deque

from electrode_visualizer.Parser import Parser

class NeuroVisor:
  def __init__(self) -> None:
    # Determina si se ha abierto un archivo
    self.is_file_open: bool = False
    # Determina que función se debe ejecutar después de seleccionar un archivo
    # True:   Abrir archivo
    # False:  Salvar archivo
    self.open: bool = True
    # Nombre de archivo seleccionado por un filedialog
    self.file:str
    # Determina los segundos mínimos para que un periodo con Umbral activo se considere valido
    self.seconds: float = 3.0
    # Lectura de los datos
    self.data: NoneType | Parser = None

    # Marca el inicio para las gráficas con zoom 
    self.start_time: float = 0
    # Marca el medio para las gráficas con zoom
    self.middle: float
    # Marca la ditancia entre el medio y los extremos
    self.difference: float
    # Marca el final para las gráficas con zoom 
    self.end_time: float
    # Marca el valor máximo de los graficos
    self.max_time:float
    # Lleva rastro de todos los ejes en el tiempo
    self.time_axis: deque[int] = deque()

    # Establecer seguimiento de vistas en la ventana
    self.visible_summary:bool = True
    self.visible_graphs:bool = True

    # Combinaciones de teclas
    self.shortcuts = deque()
    # Acciones a realizar cuando se detecta una combinación de teclas
    self.actions = deque()
    # Los dos atributos están relacionados
    # self.shortcuts[0] => self.actions[0]

    # Un stack al cual se le van a ir empujando las teclas presionadas (para detectar cuando se usa un shortcut)
    self.pressed_keys = deque(maxlen=2)

    self.setup_view()

  def setup_view(self) -> None:
    """
      Configura la vista de las ventanas basicas
    """

    # Configurar la ventana
    dpg.create_context()
    dpg.create_viewport(title="Neuro Visor", small_icon="./inteligencia.ico", large_icon="./inteligencia.ico")
    dpg.setup_dearpygui()

    # Activa los shortcuts
    self.configure_shortcuts()

    # Crear ventana para advertencias
    with dpg.window(
      label="Message",
      tag="popup",
      popup=True,
      modal=True,
      show=False,
      no_open_over_existing_popup=False,
    ):
      dpg.add_text("Advertencia",tag="popup_message")

    # Crear ventana para preguntar 
    with dpg.window(label="User input", tag="ask_minimum_filter_noise", modal=True, popup=True, no_close=True, show=False, no_open_over_existing_popup=False):
      dpg.add_input_float(
        label="Tiempo mínimo de activación",
        width=0,
        default_value=self.seconds,
        step=Parser.DELTA_TIME,
        callback=lambda _, app_data: setattr(self,"seconds",app_data)
      )
      dpg.add_button(label="Confirmar", callback=lambda: (dpg.hide_item("ask_minimum_filter_noise"), self.open_file()))
    
    # Ventana para añadir etiquetas
    with dpg.window(label="Añadir etiqueta", tag="add_tag_window", show=False, no_open_over_existing_popup=False):
      dpg.add_combo([], label="Electrodo", tag="add_tag_location")
      with dpg.group() as inputs:
        dpg.add_input_float(label="Inicio", tag="add_tag_start", step=Parser.DELTA_TIME, min_clamped=True, max_clamped=True)
        dpg.add_input_float(label="Fin", tag="add_tag_end", step=Parser.DELTA_TIME, min_clamped=True, max_clamped=True)
        dpg.add_checkbox(label="Etiqueta en periodo", before=inputs, tag="add_tag_as_period", default_value=True, callback=lambda s,a: dpg.configure_item("add_tag_end", enabled=a))
      dpg.add_input_text(label="Etiqueta", tag="add_tag_tag")
      dpg.add_button(label="Confirmar", callback=self.add_tag)

    # Ventana para eliminar etiquetas
    with dpg.window(label="Eliminar etiqueta", tag="delete_tag_window", show=False, no_open_over_existing_popup=False):
      confirm_button = dpg.add_button(label="Confirmar", callback=self.delete_tag, enabled=False)
      dpg.add_combo([], label="time", tag="delete_tag_time", before=confirm_button, callback=lambda *_: dpg.enable_item(confirm_button))
      dpg.add_combo([], label="Electrodo", tag="delete_tag_location", before="delete_tag_time", callback=lambda s,a,u: (dpg.configure_item("delete_tag_time", items=list(self.data.tags[a].keys())), dpg.set_value("delete_tag_time", ""), dpg.disable_item(confirm_button)) if a in self.data.tags else ())

    # Crear la ventana principal
    with dpg.window(label="Mi Ventana", tag="main"):
      # Menu mide 35 de height
      self.configure_menu()
      self.configure_file_selector()
      with dpg.table(tag="table_view",resizable=True, reorderable=True, hideable=True, policy=dpg.mvTable_SizingStretchProp):
        dpg.add_table_column(label="Resumen",tag="summary_column",init_width_or_weight=1.0)
        dpg.add_table_column(label="Gráficas",tag="graphs_column",init_width_or_weight=3.0)
        with dpg.table_row(tag="row_view", height=-1):
          with dpg.group(tag="summary"):
            dpg.add_text("Por favor abre un archivo")
          with dpg.group(tag="graphs"):
            dpg.add_text("Por favor abre un archivo")

    # Ejecutar la aplicación
    dpg.show_viewport()
    dpg.set_primary_window("main", True)
    dpg.set_viewport_resizable(True)
    dpg.start_dearpygui()

  def configure_menu(self) -> None:
    """
      Configura el menu de la parte superior de la ventana
    """
    with dpg.menu_bar():
      with dpg.menu(label="Archivos"):
        dpg.add_menu_item(
          label="Abrir archivo",
          callback=lambda: (dpg.show_item("file_dialog"), setattr(self, "open", True)),
          shortcut="ctrl+o"
        )
        dpg.add_menu_item(
          label="Guardar",
          callback=lambda: (dpg.show_item("file_dialog"), setattr(self, "open", False)),
          enabled=False,
          tag="menu_save",
          shortcut="ctrl+s"
        )
      with dpg.menu(label="Ventana"):
        dpg.add_menu_item(
          label="Modo ventana completa",
          callback=lambda: dpg.toggle_viewport_fullscreen(),
          shortcut="F10"
        )
        dpg.add_menu_item(
          label="Toggle Resumen",
          callback=lambda: (dpg.delete_item("summary_column"), setattr(self, "visible_summary", False), dpg.delete_item("summary")) if self.visible_summary else self.add_summary(),
          shortcut="ctrl+r"
        )
        dpg.add_menu_item(
          label="Toggle gráficas",
          callback=lambda: (dpg.delete_item("graphs_column"), setattr(self, "visible_graphs", False), setattr(self, "time_axis", deque()), dpg.delete_item("graphs")) if self.visible_graphs else self.add_graphs(),
          shortcut="ctrl+g"
        )
      with dpg.menu(label="Edición"):
        dpg.add_menu_item(
          enabled=False,
          label="Añadir etiqueta",
          tag="menu_add_tag",
          callback=lambda: dpg.configure_item("add_tag_window", show=not dpg.is_item_shown("add_tag_window")),
          shortcut="ctrl+e"
        )
        dpg.add_menu_item(
          enabled=False,
          label="Eliminar etiqueta",
          tag="menu_delete_tag",
          callback=lambda: dpg.configure_item("delete_tag_window", show=not dpg.is_item_shown("delete_tag_window")),
          shortcut="shift+e"
        )

  def configure_file_selector(self) -> None:
    """
      Configura el explorador de archivos que se muestra al tratar de abrir o guardar un archivo
    """
    with dpg.file_dialog(
        tag="file_dialog",
        default_filename='',
        modal=True,
        show=False,
        directory_selector=False,
        cancel_callback=lambda sender:dpg.hide_item(sender),
        callback=lambda _, app_data, __: (setattr(self, "file", app_data["file_path_name"]), dpg.show_item("ask_minimum_filter_noise") if self.open else self.save_file()),
        width=600,
        height=600,
      ):
        dpg.add_file_extension(".csv", color=(0, 255, 0, 255), custom_text="[csv]")

  def configure_shortcuts(self) -> None:
    """
      Configura los shortcuts y las acciones que se deben realizar al utilizarlos
    """
    # Crear combinaciones de teclas para shortcuts
    shortcuts_function:List[tuple[deque,function]] = [
      # ctrl+o
      (deque((341,79),maxlen=2), lambda: (dpg.show_item("file_dialog"), setattr(self, "open", True))),
      # ctrl+s
      (deque((341,83),maxlen=2), lambda: (dpg.show_item("file_dialog"), setattr(self, "open", False)) if self.is_file_open else ()),
      # ctrl+r
      (deque((341,82),maxlen=2), lambda: (dpg.delete_item("summary_column"), setattr(self, "visible_summary", False), dpg.delete_item("summary")) if self.visible_summary else self.add_summary()),
      # ctrl+g
      (deque((341,71),maxlen=2), lambda: (dpg.delete_item("graphs_column"), setattr(self, "visible_graphs", False), setattr(self, "time_axis", deque()), dpg.delete_item("graphs")) if self.visible_graphs else self.add_graphs()),
      # ctrl+e
      (deque((341,69),maxlen=2), lambda: (dpg.configure_item("add_tag_window", show=not dpg.is_item_shown("add_tag_window"))) if self.is_file_open else ()),
      # shift+e
      (deque((340,69),maxlen=2), lambda: (dpg.configure_item("delete_tag_window", show=not dpg.is_item_shown("delete_tag_window"))) if self.is_file_open else ()),
      # F10
      (deque((299,),maxlen=1), lambda: dpg.toggle_viewport_fullscreen()),
    ]
    with dpg.handler_registry():
      for shortcut, action in shortcuts_function:
        if len(shortcut) == 1:
          dpg.add_key_press_handler(
            key=shortcut[0],
            callback=action
          )
          continue
        self.shortcuts.append(shortcut)
        self.actions.append(action)
      dpg.add_key_press_handler(
        callback=self.key_press_handler
      )

  def key_press_handler(self, _, app_data, __) -> None:
    """
      Mantiene el estado de las teclas presionadas para detectar si se presiono una combinación que se encuentra configurada como shortcut
    """
    self.pressed_keys.append(app_data)
    try:
      action_index = self.shortcuts.index(self.pressed_keys)
      self.actions[action_index]()
    except ValueError:
      pass

  def warning(self, warining:str) -> None:
    """
      Muestra mensajes de emergencia al usuario
    """
    dpg.set_value("popup_message", warining)
    dpg.show_item("popup")

  def update_zoom(self, *_) -> None:
    """
      A partir del movimiento de los limites en la linea de tiempo se modifican las gráficas para hacer un efecto de zoom
    """
    self.start_time: float = (dpg.get_value("start_time") // self.data.DELTA_TIME) * self.data.DELTA_TIME
    self.end_time: float = (dpg.get_value("end_time") // self.data.DELTA_TIME) * self.data.DELTA_TIME
    if self.start_time > self.end_time:
      self.start_time = self.end_time
    self.middle = (self.end_time + self.start_time) / 2
    self.difference = (self.end_time - self.start_time) / 2
    dpg.set_value("start_time", self.start_time)
    dpg.set_value("middle_time", self.middle)
    dpg.set_value("end_time", self.end_time)
    dpg.set_value("add_tag_start", self.start_time)
    dpg.set_value("add_tag_end", self.end_time)
    for time_axis in self.time_axis:
      dpg.set_axis_limits(time_axis, self.start_time, self.end_time)

  def move_zoom(self, *_) -> None:
    """
      A partir de la linea que marca el medio de lo limites de tiempo seleccionados, al moverse mueve los limites para mantenerse en el medio
      Efecto de desplazamiento en las gráficas con zoom
    """
    middle = dpg.get_value("middle_time")
    if (middle - self.difference) < 0:
      dpg.set_value("middle_time", 0 + self.difference)
    elif (middle + self.difference) > self.max_time:
      dpg.set_value("middle_time", self.max_time - self.difference)
    self.middle: float = dpg.get_value("middle_time")
    dpg.set_value("start_time", self.middle - self.difference)
    dpg.set_value("end_time", self.middle + self.difference)
    self.update_zoom()

  def add_summary(self) -> None:
    """
      Si se encuentra oculto el resumen general de los datos después de utilizar el shortcut para ocultarlo lo hace reaparecer
    """
    dpg.add_table_column(parent="table_view", label="Resumen",tag="summary_column", before="graphs_column", init_width_or_weight=1.0)
    with dpg.group(parent="row_view", before="graphs", tag="summary"):
      if type(self.data) == NoneType:
        dpg.add_text("Por favor abre un archivo")
      else:
        self.populate_summary()
    self.visible_summary = True

  def add_graphs(self) -> None:
    """
      Si se encuentran ocultos los gráficos después de utilizar el shortcut para ocultarlos los hace reaparecer
    """
    dpg.add_table_column(parent="table_view", label="Gráficas", tag="graphs_column", init_width_or_weight=3.0)
    with dpg.group(parent="row_view", tag="graphs"):
      if type(self.data) == NoneType:
        dpg.add_text("Por favor abre un archivo")
      else:
        self.populate_graphs()
    self.visible_graphs = True

  def populate_summary(self) -> None:
    """
      A partir de los datos leídos se crea una vista agradable para el usuario
    """
    with dpg.table(
      parent="summary",
      resizable=True,
      reorderable=True,
      hideable=True,
      row_background=True,
    ) as table_id:
      dpg.add_table_column(label="Atributo")
      dpg.add_table_column(label="Valor")
      highlighted = -1
      color:Tuple[int, ...]
      for row, (attribute, value) in enumerate(self.data.parsed.items()):
        with dpg.table_row():
          dpg.add_text(attribute)
          if attribute == "reached":
            highlighted=row
            color = (0,255,0,100) if value else (255,0,0,100)
          dpg.add_text(str(value))
      if highlighted != -1:
        dpg.highlight_table_cell(table_id, highlighted, 1, color=color)

  def populate_graphs(self) -> None:
    """
      A partir de los datos leídos se crea una vista agradable para el usuario
    """
    self.end_time = self.max_time
    with dpg.child_window(parent="graphs", height=-110):
      # Se separan los datos por su locación/electrodo
      for location, frequencies in self.data.hierarchy.items():
        with dpg.tree_node(label=location, default_open=True):
          with dpg.plot(width=-1,no_menus=True, tag=location):
            
            # Añadir tag del eje para actualizarlo al hacer zoom o desplazar el zoom
            self.time_axis.append(dpg.add_plot_axis(dpg.mvXAxis, label="segundos"))
            with dpg.plot_axis(dpg.mvYAxis, label="value"):
              # Marca la parte mas alta de los datos para el electrodo
              ceiling: float = self.data.data[f"{location} {frequencies[0]}"].max()
              # Marca la parte mas baja de los datos para el electrodo
              ground: float = self.data.data[f"{location} {frequencies[0]}"].min()
              for frequency in frequencies:
                # Añadir datos para cada frecuencia
                dpg.add_line_series(self.data.data.index.to_list(), self.data.data[f"{location} {frequency}"].to_list())
                if self.data.data[f"{location} {frequency}"].max() > ceiling:
                  ceiling: float = self.data.data[f"{location} {frequency}"].max()
                if self.data.data[f"{location} {frequency}"].min() < ground:
                  ground: float = self.data.data[f"{location} {frequency}"].min()
              # Marcar puntos donde se supero el umbral
              for start, end in self.data.aceptable:
                dpg.add_area_series([start,start,end,end], [ground,ceiling,ceiling,ground], fill=[0,255,0,100] if self.data.parsed["reached"] else [255,0,0,100])
            # Verificar si hay marcas para este electrodo
            if location not in self.data.tags: continue
            # Mostrar marcas referentes al electrodo
            for time, tag in self.data.tags[location].items():
              dpg.add_plot_annotation(label=tag, tag=f"{location}_{time}", default_value=(time, 0), color=(255,255,0,255))
    
    # Crear linea de tiempo para  hacer zoom a las gráficas
    with dpg.plot(parent="graphs",width=-1, height=100, no_menus=True, no_mouse_pos=True):
      time_selector = dpg.add_plot_axis(dpg.mvXAxis)
      dpg.set_axis_limits(time_selector, 0, self.max_time)
      with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_labels=True, no_tick_marks=True) as time_selector:
        dpg.set_axis_limits(time_selector, 0, 1)
        # Marcar puntos donde se supero el umbral
        for start, end in self.data.aceptable:
          dpg.add_area_series([start,start,end,end], [0,1,1,0], fill=[0,255,0,100] if self.data.parsed["reached"] else [255,0,0,100])

      dpg.add_drag_line(label="Inicio", tag="start_time", callback=self.update_zoom, color=(0,255,0,255))
      dpg.add_drag_line(label="Middle", tag="middle_time", callback=self.move_zoom, color=(255,255,0,255), default_value=self.max_time//2)
      dpg.add_drag_line(label="Fin", tag="end_time",callback=self.update_zoom, color=(255,0,0,255), default_value=self.max_time)

  def add_tag(self, *_) -> None:
    """
      Agrega, mostrar y guardar marcas
    """
    start: float = dpg.get_value("add_tag_start")
    location:str = dpg.get_value("add_tag_location")
    tag = dpg.get_value("add_tag_tag")
    if dpg.get_value("add_tag_as_period"):
      end: float = dpg.get_value("add_tag_end")
      self.data.add_tag(location, end, "fin_"+tag)  
      dpg.add_plot_annotation(label="fin_"+tag, tag=f"{location}_{end}", default_value=(end,0),parent=location, color=(255,255,0,255))
      tag = "inicio_" + tag
    self.data.add_tag(location, start, tag)
    dpg.add_plot_annotation(label=tag, tag=f"{location}_{start}", default_value=(start,0), parent=location, color=(255,255,0,255))
    self.update_delete_tag_window()

  def update_delete_tag_window(self) -> None:
    """
      Actualiza los selectores de la ventana para eliminar marcas
    """
    dpg.configure_item("delete_tag_location", items=list(self.data.tags.keys()))
    dpg.set_value("delete_tag_location", "")
    dpg.set_value("delete_tag_time", "")

  def delete_tag(self, sender) -> None:
    """
      Eliminar marcas de la vista y de los datos
    """
    dpg.disable_item(sender)
    location:str = dpg.get_value("delete_tag_location")
    time:float = float(dpg.get_value("delete_tag_time"))
    print(time)
    dpg.delete_item(f"{location}_{time}")
    self.data.delete_tag(location, time)
    self.update_delete_tag_window()

  def open_file(self) -> None:
    """
      Realizar acciones necesarias después de abrir un archivo
    """
    try:
      self.data = Parser(self.file, self.seconds)
      self.is_file_open = True

      self.time_axis.clear()

      dpg.enable_item("menu_save")
      dpg.enable_item("menu_add_tag")
      dpg.enable_item("menu_delete_tag")
      dpg.delete_item("summary",children_only=True)
      dpg.delete_item("graphs",children_only=True)
      # Obtener el limite de tiempo de los datos adquiridos
      self.max_time = self.data.data.index[-1]
      dpg.configure_item("add_tag_end", max_value=self.max_time)

      dpg.configure_item("add_tag_location", items=list(self.data.hierarchy.keys()))
      dpg.set_value("add_tag_location", list(self.data.hierarchy.keys())[0])

      self.populate_summary()
      self.populate_graphs()
      self.update_zoom()
      self.update_delete_tag_window()

    except FileNotFoundError:
      self.warning("No se pudo abrir el archivo correctamente")
  
  def save_file(self) -> None:
    """
      Guardar archivo, junto con cambios realizados por el usuario
    """
    if type(self.data) == NoneType: return
    self.data.data.to_csv(self.file, index=True)
