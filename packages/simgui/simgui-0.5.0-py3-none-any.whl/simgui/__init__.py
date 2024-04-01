from typing import Union
from PySide2.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QApplication, QComboBox, QGridLayout, QMessageBox
from PySide2.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPolygonItem
from PySide2.QtGui import QPixmap, QBrush, QColor, QPolygonF
from PySide2.QtCore import Qt, QTimer, QEvent, QPointF
from urllib.request import build_opener
from random import randint

try:
  from simpleaudio import WaveObject
except:
  from .mockaudio import WaveObject  

def make_color(color):
  try:
      r, g, b=color
      return QColor(r, g, b)
  except:
      return QColor(color)

def get_css_color(color):
  qc=make_color(color)
  n=qc.name(QColor.HexRgb)
  return n

class WidgetWrapper:
  def __init__(self, w: QWidget, sgapp=None):
      self.w=w
      self.sgapp=sgapp
  def on_click(self, func):
      self.w.clicked.connect(func)
  def set_label_text(self, text):
      self.set_wid_text(text)
  def set_button_text(self, text):
      self.set_wid_text(text)
  def get_label_text(self):
      return self.get_wid_text()
  def set_wid_text(self, text: Union[str, int]):
      self.w.setText(str(text))
  def get_wid_text(self):
      return self.w.text()
  def set_wid_size(self, w: int, h: int):
      self.w.setFixedSize(w, h)
  def set_wid_min_size(self, w, h):
      self.w.setMinimumSize(w, h)
  def set_wid_max_size(self, w, h):
      self.w.setMaximumSize(w, h)
  def set_wid_color(self, color):
      c=get_css_color(color)
      self.w.setStyleSheet(f"background-color: {c}")
  def set_label_img(self, img_url):
      data=self.sgapp.fetch_web_data(img_url)
      pm=QPixmap()
      pm.loadFromData(data)
      self.w.setScaledContents(True)
      self.w.setPixmap(pm)
  def on_edited(self, func):
      self.w.textEdited.connect(func)
  def on_index_changed(self, func):
      self.w.activated.connect(func)
  def add_combo_item(self, item):
      self.w.addItem(str(item))
  def get_combo_text(self):
      return self.w.currentText()
  def get_input_text(self):
      return self.w.text()
  def get_input_num(self):
      t=self.get_input_text()
      return int(t)
  def get_input_value(self):    
      t=self.get_input_text()
      try:
        return int(t)
      except:
        return t
  def set_input_text(self, text):
      self.w.setText(str(text))

class GIWrapper:
  def __init__(self, sgapp, gi):
    self.sgapp=sgapp
    self.gi=gi
  def set_gi_pos(self, x, y):
    self.gi.setPos(x, y)
  def get_gi_x(self):
    return self.gi.pos().x()
  def get_gi_y(self):
    return self.gi.pos().y()
  def set_gi_color(self, color):    
    br=QBrush(make_color(color))
    self.gi.setBrush(br)
  def set_gi_img(self, img_url_or_file):
    pm=self.gi.pixmap()
    pm2=self.sgapp.load_pixmap(img_url_or_file, pm.width(), pm.height())
    self.gi.setPixmap(pm2)
  def set_gi_rect_size(self, w, h):
    self.gi.setRect(0, 0, w, h)
  def set_gi_cir_radius(self, r):
    self.gi.setRect(0, 0, r, r)
  def remove_gi(self):
    self.sgapp.gs.removeItem(self.gi)
  def get_brect_in_parent(self):
    r=self.gi.boundingRect()
    r=self.gi.mapRectToParent(r)
    return r
  def are_gi_overlap(self, giw):
    r1=self.get_brect_in_parent()
    r2=giw.get_brect_in_parent()
    return r1.intersects(r2)

class SimGraphicsView(QGraphicsView):
  def __init__(self, scene, key_handler, mouse_handler):
      super().__init__(scene)
      self.key_handler=key_handler
      self.mouse_handler=mouse_handler
  def keyPressEvent(self, event):
    self.key_handler(event)
  def keyReleaseEvent(self, event):
    self.key_handler(event)
  def mousePressEvent(self, event):
    self.mouse_handler(event)

class MainWin(QWidget):
  def __init__(self, key_handler):
      super().__init__()
      self.key_handler=key_handler
  def keyPressEvent(self, event):
    self.key_handler(event)
  def keyReleaseEvent(self, event):
    self.key_handler(event)

class SimGuiApp(QApplication):
    SCENE_WIDTH=400
    SCENE_HEIGHT=300
    def __init__(self) -> None:
        super().__init__()
        self.mod=None
    def start(self, mod):
        self.mod=mod
        self.in_modal=False
        self.key_ev=None
        self.gs=None
        self.gv=None
        self.gi_dict={}
        self.timer_dict={}
        self.wid_dict={}
        self.last_row=None
        self.auto_row=0
        self.auto_col=0
        self.make_opener()
        self.wid=MainWin(self.on_key)
        self.wid.setWindowTitle("simgui")
        self.lo=QGridLayout()
        self.wid.setLayout(self.lo)
        self.wid.show()
        ev=QEvent(QEvent.Type.User)
        self.postEvent(self, ev)
        self.exec_()
    def event(self, ev):
      if ev.type()==QEvent.Type.User:
        self.call_handler("on_ready")  
      return super().event(ev)
    def make_opener(self):
      self.op=build_opener()
      self.op.addheaders=[("User-agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")]
      self.op.cache={}
    def call_handler(self, fn, data=None):
        handler=self.mod.get(fn)
        if handler:
          if data:
            handler(data)
          else:
            handler()
    def add_label(self, name, text, **kwargs):
        lbl=QLabel(str(text))
        ww=WidgetWrapper(lbl, self)
        self.add_wid(name, ww, **kwargs)
        return ww
    def add_button(self, name, text, **kwargs):
        btn=QPushButton(str(text))
        ww=WidgetWrapper(btn)
        if name:
          def on_click():
            self.call_handler("on_click_"+name)
          ww.on_click(on_click)
        self.add_wid(name, ww, **kwargs)
        return ww
    def set_wid_text(self, name: str, text: Union[str, int]):
      self.get_wid(name).set_wid_text(text)
    def get_wid_text(self, name):
      return self.get_wid(name).get_wid_text()
    def set_wid_size(self, name: str, w: int, h: int):
      ww=self.get_wid(name)
      ww.set_wid_size(w, h)
    def set_wid_min_size(self, name, w, h):
      ww=self.get_wid(name)
      ww.set_wid_min_size(w, h)
    def set_wid_max_size(self, name, w, h):
      ww=self.get_wid(name)
      ww.set_wid_max_size(w, h)
    def set_wid_color(self, name, color):
      ww=self.get_wid(name)
      ww.set_wid_color(color)
    def fetch_web_data(self, url):
      if url in self.op.cache:
        return self.op.cache[url]
      else:
        d=self.op.open(url).read()
        self.op.cache[url]=d
        return d
    def set_label_img(self, name, img_url):
      ww=self.get_wid(name)
      ww.set_label_img(img_url)
    def add_wid(self, name, ww, **kwargs):
      if name:
        if name in self.wid_dict:
          raise ValueError(f"widget named {name} already exists", name)
        self.wid_dict[name]=ww
      if "right" in kwargs:
        row=self.last_row
        col=self.auto_col
      else:
        row=self.auto_row
        col=0
      row=kwargs.get("row", row)
      col=kwargs.get("col", col)
      rows=kwargs.get("rows", 1)
      cols=kwargs.get("cols", 1)
      self.lo.addWidget(ww.w if hasattr(ww, "w") else ww, row, col, rows, cols)
      self.last_row=row
      self.auto_row=row+rows
      self.auto_col=col+cols
    def get_wid(self, name)->WidgetWrapper:
      if name in self.wid_dict:
        return self.wid_dict[name]
      else:
        raise ValueError(f"no widget named {name}", name)
    def add_input(self, name, **kwargs):
        edit=QLineEdit()
        ww=WidgetWrapper(edit)
        if name:
          def on_edited():
            self.call_handler("on_edited_"+name)
          ww.on_edited(on_edited)
        self.add_wid(name, ww, **kwargs)
        return ww
    def add_combo(self, name, **kwargs):
        cb=QComboBox()
        ww=WidgetWrapper(cb)
        if name:
          def on_idx_changed():
            self.call_handler("on_index_changed_"+name)
          ww.on_index_changed(on_idx_changed)
        self.add_wid(name, ww, **kwargs)
        return ww
    def add_combo_item(self, name, item):
        ww=self.get_wid(name)
        ww.add_combo_item(item)
    def get_combo_text(self, name):
        ww=self.get_wid(name)
        return ww.get_combo_text()
    def get_input_text(self, name):
      ww=self.get_wid(name)
      return ww.get_input_text()
    def get_input_num(self, name):
      ww=self.get_wid(name)
      return ww.get_input_num()
    def get_input_value(self, name):
      ww=self.get_wid(name)
      return ww.get_input_value()
    def set_input_text(self, name, text):
      ww=self.get_wid(name)
      ww.set_input_text(text)
    def on_key(self, event):
      evt=event.type()
      if evt==QEvent.KeyPress:
        self.key_ev=event
        self.call_handler("on_key")
      elif evt==QEvent.KeyRelease:
        self.key_ev=event
        self.call_handler("on_key_up")
    def on_mouse(self, event):
      evt=event.type()
      if evt==QEvent.MouseButtonPress:
        self.mouse_ev=event
        self.call_handler("on_mouse")
    def add_graphics_view(self, min_w, min_h, scene_w=None, scene_h=None):
        if self.gs:
          raise ValueError("Only one graphics view can be added")
        self.gs=QGraphicsScene()
        self.gv=SimGraphicsView(self.gs, self.on_key, self.on_mouse)
        self.gv.setMinimumSize(min_w, min_h)
        if scene_w and scene_h:
          self.gv.setSceneRect(0, 0, scene_w, scene_h)
        else:
          #there is a 1 pixel margin hard coded
          self.gv.setSceneRect(0, 0, SimGuiApp.SCENE_WIDTH-2, SimGuiApp.SCENE_HEIGHT-2)
        self.add_wid("simgui_gv", self.gv)
    def add_gi_img(self, name, x, y, w, h, img_url_or_file):
      pm2=self.load_pixmap(img_url_or_file, w, h)
      gi=QGraphicsPixmapItem(pm2)
      giw=GIWrapper(self, gi)
      giw.set_gi_pos(x, y)
      self.add_gi(name, giw)
      return giw
    def load_pixmap(self, img_url_or_file, w, h):
      if img_url_or_file.find("://")>0:
        data=self.fetch_web_data(img_url_or_file)
        pm=QPixmap()
        pm.loadFromData(data)
      else:
        from pathlib import Path
        p=Path(img_url_or_file)
        if p.exists():
          pm=QPixmap(img_url_or_file)
        else:
          raise ValueError(f"File {img_url_or_file} not found")
      pm2=pm.scaled(w, h, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
      return pm2
    def set_gi_img(self, name, img_url_or_file):
      giw=self.get_gi(name)
      giw.set_gi_img(img_url_or_file)
    def add_gi_rect(self, name, x, y, w, h, color):
      gi=QGraphicsRectItem(0, 0, w, h)
      giw=GIWrapper(self, gi)
      giw.set_gi_pos(x, y)
      giw.set_gi_color(color)
      self.add_gi(name, giw)
      return giw
    def add_gi_polygon(self, name, points, color):
      x, y=points[0]
      pts=[QPointF(x2-x, y2-y) for (x2, y2) in points]
      gi=QGraphicsPolygonItem(QPolygonF(pts))
      giw=GIWrapper(self, gi)
      giw.set_gi_pos(x, y)
      giw.set_gi_color(color)      
      self.add_gi(name, giw)
      return giw
    def set_gi_rect_size(self, name, w, h):
      giw=self.get_gi(name)
      giw.set_gi_rect_size(w, h)
    def add_gi_cir(self, name, x, y, r, color):
      gi=QGraphicsEllipseItem(0, 0, r, r)
      giw=GIWrapper(self, gi)
      giw.set_gi_pos(x, y)
      giw.set_gi_color(color)   
      self.add_gi(name, giw)
      return giw
    def set_gi_cir_radius(self, name, r):
      giw=self.get_gi(name)
      giw.set_gi_cir_radius(r)
    def add_gi(self, name, giw):
      if self.gs==None:
        raise ValueError("Must add a graphics scene first")
      if name:
        if name in self.gi_dict:
          raise ValueError(f"Graphics item {name} already exists")
        self.gi_dict[name]=giw
      self.gs.addItem(giw.gi)
    def set_gi_pos(self, name, x, y):
      giw=self.get_gi(name)
      giw.set_gi_pos(x, y)
    def get_gi_x(self, name):
      giw=self.get_gi(name)
      return giw.get_gi_x()
    def get_gi_y(self, name):
      giw=self.get_gi(name)
      return giw.get_gi_y()
    def set_gi_color(self, name, color):    
      giw=self.get_gi(name)
      giw.set_gi_color(color)
    def gi_exists(self, name):
      return  name in self.gi_dict
    def get_gi(self, name):
      if name in self.gi_dict:
        return self.gi_dict[name]
      else:
        raise ValueError(f"No graphics item named {name}")
    def remove_gi(self, name):
      if self.gs==None:
        raise ValueError("Must add a graphics scene first")
      giw=self.get_gi(name)
      del self.gi_dict[name]
      giw.remove_gi()
    def make_unique_name(self, prefix):
      while True:
        name=prefix+str(randint(0, 65535))
        if not(name in self.gi_dict) and not(name in self.wid_dict):
          return name
    def get_key(self)->str:
      code_map={Qt.Key_Left: "Left", Qt.Key_Right: "Right", Qt.Key_Up: "Up", Qt.Key_Down: "Down", \
            Qt.Key_Enter: "Enter", Qt.Key_Insert: "Insert", Qt.Key_Delete: "Delete", \
            Qt.Key_Return: "Enter", Qt.Key_Home: "Home", Qt.Key_End: "End",
            Qt.Key_PageUp: "PageUp", Qt.Key_PageDown: "PageDown" }
      key=self.key_ev.key()
      txt=self.key_ev.text()
      if key in code_map:
        return code_map[key]
      elif txt:
        return txt
      else:
        return "Unknown"
    def get_mouse_x(self)->int:
      p=self.mouse_ev.pos()
      return int(p.x())
    def get_mouse_y(self)->int:
      p=self.mouse_ev.pos()
      return int(p.y())
    def get_mouse_btn(self)->str:
      b=self.mouse_ev.button()
      if b==Qt.LeftButton:
        return "Left"
      elif b==Qt.RightButton:
        return "Right"
      else:
        return "Other"
    def start_timer(self, name, interval):
      def on_timeout():
        if not self.in_modal:
          self.call_handler("on_timeout_"+name)
      tm=QTimer()
      tm.timeout.connect(on_timeout)
      tm.start(int(interval*1000))
      self.timer_dict[name]=tm
    def stop_timer(self, name):
      self.timer_dict[name].stop()
    def send_data_to_future(self, data, interval):
      def on_timeout():
        tm.stop()
        self.call_handler("on_data_from_past", data)
      tm=QTimer()
      tm.timeout.connect(on_timeout)
      tm.start(int(interval*1000))
    def are_gi_overlap(self, n1, n2):
      giw1=self.get_gi(n1)
      giw2=self.get_gi(n2)
      return giw1.are_gi_overlap(giw2)
    def msg_box(self, text):
      self.in_modal=True
      try:
        QMessageBox.information(self.wid, "Info", str(text))
      finally:
        self.in_modal=False
    def play_wav(self, path):
      wo=WaveObject.from_wave_file(path)
      wo.play()
    def get_win(self)->MainWin:
      return self.wid

sgapp=SimGuiApp()

# the mod parameter is no longer needed
def start(mod=None):
  import __main__
  sgapp.start(vars(__main__))

def add_label(name: str, text: str, **kwargs)->WidgetWrapper:
    return sgapp.add_label(name, text, **kwargs)

def make_label(text: str, **kwargs)->WidgetWrapper:
    return add_label(None, text, **kwargs)

def set_label_text(name: str, text: Union[str, int]):
    sgapp.set_wid_text(name, text)

def get_label_text(name: str):
    return sgapp.get_wid_text(name)

def set_label_img(name: str, img_url: str):
    sgapp.set_label_img(name, img_url)

def set_wid_color(name: str, color):
    sgapp.set_wid_color(name, color)

def set_wid_size(name: str, w: int, h: int):
    sgapp.set_wid_size(name, w, h)

def set_wid_min_size(name: str, w, h):
    sgapp.set_wid_min_size(name, w, h)

def set_wid_max_size(name: str, w, h):
    sgapp.set_wid_max_size(name, w, h)

def add_button(name: str, text: str, **kwargs)->WidgetWrapper:
    return sgapp.add_button(name, text, **kwargs)    

def make_button(text: str, **kwargs)->WidgetWrapper:
  return add_button(None, text, **kwargs)

def set_button_text(name: str, text: Union[str, int]):
    sgapp.set_wid_text(name, text)

def add_input(name: str, **kwargs)->WidgetWrapper:
    return sgapp.add_input(name, **kwargs)    

def make_input(**kwargs)->WidgetWrapper:    
    return add_input(None, **kwargs)

def get_input_text(name):
    return sgapp.get_input_text(name)        

def get_input_num(name):
    return sgapp.get_input_num(name)        

def get_input_value(name):
    return sgapp.get_input_value(name)        

def set_input_text(name, text):
    return sgapp.set_input_text(name, text)

def add_combo(name, **kwargs)->WidgetWrapper:
  return sgapp.add_combo(name, **kwargs)      

def make_combo(**kwargs)->WidgetWrapper:
  return add_combo(None, **kwargs)

def add_combo_item(name, item):
  sgapp.add_combo_item(name, item)

def get_combo_text(name):
  return sgapp.get_combo_text(name)

def add_graphics_view(min_w, min_h, scene_w=None, scene_h=None):
  sgapp.add_graphics_view(min_w, min_h, scene_w, scene_h)

def add_gi_img(name: str, x: int, y: int, w: int, h: int, img_url: str)->GIWrapper:
  return sgapp.add_gi_img(name, x, y, w, h, img_url)

def make_gi_img(x: int, y: int, w: int, h: int, img_url: str)->GIWrapper:
  return add_gi_img(None, x, y, w, h, img_url)

def add_gi_rect(name: str, x: int, y: int, w: int, h: int, color)->GIWrapper:
  return sgapp.add_gi_rect(name, x, y, w, h, color)

def make_gi_rect(x: int, y: int, w: int, h: int, color)->GIWrapper:
  return add_gi_rect(None, x, y, w, h, color)

def add_gi_cir(name: str, x: int, y: int, r: int, color)->GIWrapper:
  return sgapp.add_gi_cir(name, x, y, r, color)

def make_gi_cir(x: int, y: int, r: int, color)->GIWrapper:
  return add_gi_cir(None, x, y, r, color)

def add_gi_polygon(name, points, color)->GIWrapper:
  return sgapp.add_gi_polygon(name, points, color)

def make_gi_polygon(points, color)->GIWrapper:
  return add_gi_polygon(None, points, color)

def remove_gi(name):
  sgapp.remove_gi(name)

def get_key()->str:
  return sgapp.get_key()

def get_mouse_x()->int:
  return sgapp.get_mouse_x()

def get_mouse_y()->int:
  return sgapp.get_mouse_y()

def get_mouse_btn()->str:
  return sgapp.get_mouse_btn()

def get_gi_x(name)->int:
  return sgapp.get_gi_x(name)

def get_gi_y(name)->int:
  return sgapp.get_gi_y(name)

def set_gi_pos(name, x: int, y: int):
  sgapp.set_gi_pos(name, x, y)

def set_gi_size(name: str, w: int, h: int):
  sgapp.set_gi_size(name, w, h)

def set_gi_img(name, img_url_or_file):
  sgapp.set_gi_img(name, img_url_or_file)

def set_gi_color(name, color):
  sgapp.set_gi_color(name, color)

def set_gi_rect_size(name, w, h):
  sgapp.set_gi_rect_size(name, w, h)

def set_gi_cir_radius(name, r):
  sgapp.set_gi_cir_radius(name, r)

def start_timer(name: str, interval: float):
  sgapp.start_timer(name, interval)

def stop_timer(name):
  sgapp.stop_timer(name)

def make_unique_name(prefix):
  return sgapp.make_unique_name(prefix)

def gi_exists(name: str):
  return sgapp.gi_exists(name)

def get_wid(name: str)->WidgetWrapper:
  return sgapp.get_wid(name)

def are_gi_overlap(n1: str, n2: str)->bool:
  return sgapp.are_gi_overlap(n1, n2)

def msg_box(text: str):
  sgapp.msg_box(text)

def quit():
  sgapp.quit()

def play_wav(path):
  sgapp.play_wav(path)

def send_data_to_future(data, interval):
  sgapp.send_data_to_future(data, interval)

def get_win()->MainWin:
  return sgapp.get_win()