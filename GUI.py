import customtkinter as _ctk
from . import Iterable as _Iterable
import ast as _ast
from . import Time
class CustomTk:
    def sync_size(obj1, obj2, width=True, height=True):
        def size(e):
            obj2.configure(width=obj1.winfo_width(), height=obj1.winfo_height())
        obj1.bind('<Configure>', size)
    def apply_style(master, datas, nested=False):
        """configure every obj with details
        example:
        main = CTk()
        apply_style(main, {CTkEntry: {'text_color': 'red', 'fg_color': 'white'}})"""
        if nested:
            lst = CustomTk.all_objects(master) 
        else: 
            lst = master.winfo_children()
        for obj in lst:
            typ = type(obj)
            if typ in datas:
                obj.configure(**datas[typ])
    class Texts:
        def __init__(self, master, nested=False):
            self.master = master
            self.nested = nested
            if self.nested:
                self.wids = CustomTk.all_objects(self.master) 
            else:
                self.wids = self.master.winfo_children()
        def save_texts(self, file):
            result = ''
            for w in self.wids:
                try:
                    result += w.cget('text') + '\n'
                except ValueError:
                    pass
            result = result.strip('\n')
            if result:
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(result)
        def load_texts(self, file):
            with open(file, encoding='utf-8') as f:
                texts = f.read().split('\n')
            for w, t in zip(self.wids, texts):
                print(w, t, sep=' | ')
                try:
                    w.configure(text=t)
                except:
                    pass
    def from_to_widgets_event(widgets, func_takes_two, sequence='<Button-1>'):
        def alls():
            in_mode = True
            new = []
            def fi(e):
                nonlocal in_mode
                if in_mode:
                    new.append(e.widget.master)
                    if len(new) == 2:
                        func_takes_two(new[0], new[1])
                        new.clear()
                        in_mode = False
            for i in widgets:
                i.bind(sequence, fi)
        return _ctk.CTkButton(widgets[0].master, text='', command=alls)
    class Manager:
        def show_with_details(obj, dic):
            if dic:
                if 'relwidth' in dic:
                    t = 'place'
                elif 'row' in dic:
                    t = 'grid'
                else:
                    t = 'pack'
            getattr(obj, t)(**dic)
    def change_mode(master, light_icon='Light', dark_icon='Dark'):
        def c():
            icons = [dark_icon, light_icon]
            modes = ['Light', 'Dark']
            _ctk.set_appearance_mode(_Iterable.opponents(modes, _ctk.get_appearance_mode()))
            button.configure(text=_Iterable.opponents(icons, button.cget('text')))
        button = _ctk.CTkButton(master, text=dark_icon, command=c, font=('arial', 30))
        return button
    def limit_len(entry, limit):
        if entry.cget('textvariable'):
            check = entry.cget('textvariable')
        else:
            check = _ctk.StringVar()
            entry.configure(textvariable=check)
        def c(*args):
            if len(entry.get()) > limit:
                entry.delete(entry.index('insert') - 1)
        check.trace_add('write', c)
    def console(master, texts, per_row=3, entry_to_insert=None, font=('arial', 20), text_color='white', return_dic_frame_and_buttons=False):
        result = _ctk.CTkFrame(master)
        def create_button(text):
            if entry_to_insert:
                return _ctk.CTkButton(result, text=text, font=font, text_color=text_color, command=lambda: entry_to_insert.insert('end', text))
            return _ctk.CTkButton(result, text=text, font=font, text_color=text_color)
        buttons = [create_button(str(c)) for c in texts]
        CustomTk.tidy_up(buttons, per_row=per_row)
        return result
    class Timer:
        def __init__(self, duration, obj, start_icon='start', stop_icon='stop', while_resume=None, when_finish=None):
            self.duration = duration
            self.resume = self.duration > 0
            self.obj = obj
            self.obj.configure(text=Time.how_many_hms_in_s(self.duration))
            self.button = _ctk.CTkButton(obj.master, text=start_icon, command=self.start)
            self.start_icon = start_icon
            self.stop_icon = stop_icon
            self.timers = 0
            self.while_resume = while_resume
            self.when_finish = when_finish
        def start(self):
            if self.resume:
                self.button.configure(command=self.stop, text=self.stop_icon)
                self.duration -= 1
                self.obj.configure(text=Time.how_many_hms_in_s(self.duration))
                if self.while_resume:
                    self.while_resume()
                if self.duration == 0:
                    if self.when_finish:
                        self.button.configure(text=self.start_icon)
                        self.when_finish()
                else:
                    self.obj.after(1000, self.start)
        def stop(self):
            self.button.configure(command=self.resume_timer, text=self.start_icon)
            self.resume = False
        def resume_timer(self):
            self.resume = self.duration > 0
            self.start()
    def show_hide_entry_btn(entry, show_ico="show", hide_ico='hide', hide_with="*"):
        entry.configure(show=hide_with)
        btn = _ctk.CTkButton(entry.master, text=show_ico, font=("arial", 20))
        def change():
            entry.configure(_Iterable.opponents([[hide_ico, show_ico], entry.cget('show')]))
        btn.configure(command=change)
        return btn
    def move(obj, objs_same_location=None):
        master = obj.master
        def m(e):
            def t(o):
                x = o.winfo_x()
                y = o.winfo_y()
                o.pack_forget()
                o.grid_forget()
                o.place(x=x, y=y)
                width = o.winfo_width()
                height = o.winfo_height()
                mouse_x = master.winfo_pointerx() - master.winfo_rootx() - width//2
                mouse_y = master.winfo_pointery() - master.winfo_rooty() - height//2
                o.place(x=mouse_x, y=mouse_y)
            t(obj)
            if objs_same_location:
                list(map(t, objs_same_location))
        obj.bind('<B1-Motion>', m)
    def tidy_up(master, widgets, per_row, start_row=0, start_column=0, padx=5, pady=5):
        """
        Arrange widgets in a grid with a fixed number per row.
        """
        c = start_column
        for i in range(start_row):
            master.grid_rowconfigure(i, minsize=widgets[0].winfo_reqheight())
        for i in range(start_column):
            master.grid_columnconfigure(i, minsize=widgets[0].winfo_reqwidth())
        for i in widgets:
            i.grid(row=start_row, column=c, padx=padx, pady=pady)
            c += 1
            if c % per_row == 0:
                start_row += 1
                c = start_column
    def all_objects(master):
        """Return a flat list of all child widgets in master."""
        result = []
        for i in master.winfo_children():
            if isinstance(i, (_ctk.CTkFrame, _ctk.CTkScrollableFrame, _ctk.CTkToplevel)):
                result.extend(CustomTk.all_objects(i))
            else:
                result.append(i)
        return result
    def exit_esc(master):
        master.bind('<Escape>', lambda e: master.destroy())
class Turtle:
    def moving(obj, keys, value=20, when_moving=None):
        """insert keys with this order: [up, down, left, right]"""
        def up():
            obj.setheading(90)
            obj.forward(value)
            if when_moving:
                when_moving()
        def down():
            obj.setheading(270)
            obj.forward(value)
            if when_moving():
                when_moving()
        def left():
            obj.setheading(180)
            obj.forward(value)
            if when_moving:
                when_moving()
        def right():
            obj.setheading(0)
            obj.forward(value)
            if when_moving:
                when_moving()
        for i, e in zip(keys, [up, down, left, right]):
            obj.screen.onkeypress(e, i)
    def in_circle(turtle_obj, shape_as_func, how_many=10):
        """draw shape_as_func in circle"""
        for i in range(how_many):
            shape_as_func()
            turtle_obj.left(360/how_many)
    def rock_bottom(window, obj, before_end=20, on_xy=False):
        x = window.window_width() // 2 - before_end
        y = window.window_height() // 2 - before_end
        if on_xy:
            if abs(obj.xcor()) >= abs(x):
                return 'x'
            elif abs(obj.ycor()) >= abs(y):
                return 'y'
            else:
                return ''
        return abs(obj.xcor()) >= abs(x) or abs(obj.ycor()) >= abs(y)