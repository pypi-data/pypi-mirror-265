import json
import numpy as np
import pandas as pd
from collections import deque, defaultdict
from typing import Iterable, List, Dict

# Issue: Crear clase que parse un csv en una estructura de Python
# 
# Autor: Ignacio de la Torre Arias
# Correo electrónico: ignacio.delatorre4320@alumnos.udg.mx
# Fecha de creación: 22/03/2024

class Parser:
  POSITIONS_PER_SECOND: int = 8
  DELTA_TIME: float = 1/8
  
  def __init__(self, file_name:str, min_time_period: float) -> None:
    self.parsed:Dict[str,any] = {}
    
    self.data: pd.DataFrame = pd.read_csv(file_name, index_col=0)
    
    self.parsed["slug"] = file_name
    self.parsed["reached"] = "Umbral +" in self.data.columns

    # Corregir desplazamiento
    self.data.index = np.arange(0,len(self.data.index)/self.POSITIONS_PER_SECOND,self.DELTA_TIME)

    # Unificar Umbral
    self.data.rename(columns={"Umbral -": "Umbral", "Umbral +": "Umbral"}, inplace=True)
    # Unificar promedio, se considera que los datos solo incluirán un promedio
    self.data.rename(columns={key:"Promedio" for key in self.data.columns[self.data.columns.to_series().apply(lambda name: "Promedio" in name)].to_list()}, inplace=True)

    t = self.filter_umbral_noise(self.data[self.data["Umbral"] == 1].index, min_time_period=min_time_period)
    noise:deque[tuple[float,float]] = t[0]
    self.aceptable:deque[tuple[float,float]] = t[1]
    for beginning_noise, finish_noise in noise:
      # Eliminar ruido (puntos que marcan 1 en el Umbral pero no se encuentran dentro de un grupo cuyo periodo entre inicio y fin del grupo sea mayor o igual al tiempo mínimo establecido)
      self.data.loc[(self.data.index >= beginning_noise) & (self.data.index <= finish_noise),"Umbral"] = 0

    reached_times = pd.Series(map(lambda period: period[-1]-period[0], self.aceptable))

    self.parsed["first_time_reached"] = self.aceptable[0][0]
    self.parsed["time_max"] = reached_times.max()
    self.parsed["time_min"] = reached_times.min()
    self.parsed["reached_times"] = reached_times.size
    self.parsed["time_average"] = reached_times.mean()
    self.parsed["reached_time"] = reached_times.sum()
    self.parsed["not_reached_time"] = self.data.index[-1] - self.parsed["reached_time"]
    meta_data_columns = [
      self.data.columns.get_loc("Umbral"),
      self.data.columns.get_loc("Promedio"),
    ]
    if "tags" in self.data.columns:
      meta_data_columns.append(self.data.columns.get_loc("tags"))
    self.hierarchy = self.electrode_grouper(self.data.columns.delete(meta_data_columns))
    self.tags:Dict[str,Dict[float,str]] = defaultdict(dict)
    if "tags" in self.data.columns:
      tags = self.data.loc[~self.data["tags"].isna(),"tags"].to_dict()
      try:
        tags:Dict[float,Dict[str,str]] = dict(map(lambda pair: (pair[0], json.loads(pair[1])),tags.items()))
        for time, tag_group in tags.items():
          for location, tag in tag_group.items():
            self.tags[location][time] = tag
      except:
        self.data["tags"] = pd.NA
    else:
      self.data["tags"] = pd.NA

  def add_tag(self, location:str, time:float, tag:str) -> None:
    """
    Añade etiquetas a determinado punto en el tiempo, se ve reflejado en el atributo tags

    :param location: locación del electrodo al cual se le añade la etiquete

      Ejemplo: F3
    :param time: Punto en el tiempo que se debe añadir la etiqueta
    :param tag: etiqueta que se debe añadir
    """
    self.tags[location][time] = tag
    stored_tag:Dict[str,str] = {}
    stored_str = self.data.loc[time,"tags"]
    if not pd.isna(stored_str):
      stored_tag:Dict[str,str] = json.loads(stored_str)
    stored_tag.update({location:tag})
    self.data.loc[time,"tags"] = json.dumps(stored_tag)

  def delete_tag(self,  location:str, time:float) -> None:
    """
    Elimina etiquetas en un punto en el tiempo, se ve refleja en el atributo tags
    
    :param location: locación del electrodo al cual se le quita la etiquete
    :param time: Punto en el tiempo en el que se encuentra la etiqueta
    """
    if self.tags[location].get(time) != None:
      self.tags[location].pop(time)
      stored_tag:Dict[str,str] = json.loads(self.data.loc[time,"tags"])
      stored_tag.pop(location)
      if len(stored_tag) == 0:
        self.data.loc[time,"tags"] = pd.NA
      else:
        self.data.loc[time,"tags"] = json.dumps(stored_tag)
    if len(self.tags[location]) == 0:
      self.tags.pop(location)

  @classmethod
  def filter_umbral_noise(cls, times:Iterable[float], min_time_period:float) -> tuple[deque[tuple[float,float]], deque[tuple[float,float]]]:
    """
    Detecta ruidos en el Umbral

    :param times: Tiempos en los cuales se supero el umbral
    :param min_time_period: Tiempo mínimo por el cual se tiene que superar el Umbral para no considerarse ruido
    :return: Una tuple con dos listas
      
      (Datos Inválidos (ruido), Datos Validos)

      Estas listas se componen de tuples, con información acerca de los periodos, los periodos son el tiempo consecutivo por el cual se mantuvo el umbral activo

      (inicio de un periodo de tiempo, final del periodo)
    """
    invalid: deque[
      tuple[
        float,  # Beginning
        float   # Last
      ]] = deque(maxlen=times.size)
    valid: deque[
      tuple[
        float,  # Beginning
        float   # Last
      ]] = deque(maxlen=times.size//(cls.POSITIONS_PER_SECOND*3))
    beginning = 0
    while beginning < times.size:
      # Se hacen iteraciones mientras se puedan seguir creando grupos
      right = times.size - 1
      left = beginning
      found = False
      while left <= right and not found:
        # Se busca una pendiente que determina el final de un grupo mediante una estrategia de búsqueda binaria
        mid = (right + left) // 2
        if times[mid] > (times[beginning] + (cls.DELTA_TIME*(mid-beginning))):
          # El valor es mayor que lo esperado, la pendiente esta mas atrás
          right = mid - 1
        else:
          # La pendiente se encuentra mas adelante
          left = mid + 1
          if (mid+1 == times.size) or times[mid+1] > (times[beginning] + (cls.DELTA_TIME*(mid+1-beginning))):
            # Estamos en el limite de la pendiente
            if (times[mid] - times[beginning]) < min_time_period:
              # El valle es mas corto de lo que se requiere
              invalid.append((times[beginning],times[mid]))
            else:
              valid.append((times[beginning],times[mid]))
            found = True
      beginning = mid+1
    return (invalid,valid)

  @classmethod
  def electrode_grouper(cls, names:List[str]) -> Dict[str,List[str]]:
    """
    Se seleccionan los electrodos que se buscan incluir

    :param names: Los nombres de los electrodos (incluida su ubicación y frecuencia) tal cual aparecen en la tabla de datos que se buscaran los valores
      Estructura de nombres
      
      "{location} {frequency}"
      
      Ejemplos:
      
      "F3 Theta"
      
      "F4 Beta baja"
    :return: Electrodos agrupados con sus frecuencias en una estructura jerárquica
    """
    separated = np.array([s.split(sep=" ") for s in names])
    # Extraer locaciones utilizadas
    locations = np.unique(separated[:,0])
    # Extraer frecuencias utilizadas
    frequencies = set(map(lambda names: " ".join(names),separated[:,1:]))
    # Validar locaciones con sus respectivas frecuencias
    return {location:[frequency for frequency in frequencies if f"{location} {frequency}" in names] for location in locations}