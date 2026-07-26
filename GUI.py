import customtkinter as _ctk
from . import Math as _Math
from . import Files as _Files
from . import String as _String
from . import Iterable as _Iterable
import ast as _ast
class CustomTk:
    def collaspe_expand(text_field, text='🔻', limit=5, collaspe=2):
        def alls():
            old_h = text_field.winfo_height()
            def col_e():
                text = text_field.get('1.0', 'end') if isinstance(text_field, _ctk.CTkTextbox) else text_field.get()
                if len(text.split('\n'))-1 > limit and text_field.winfo_height() == old_h:
                    text_field.configure(height=collaspe*50)
                else:
                    text_field.configure(height=old_h)
            def pb():
                x = text_field.winfo_x()+text_field.winfo_width()-40
                btn = _ctk.CTkButton(text_field.master, text=text, command=col_e, width=40)
                btn.place(x=x, y=text_field.winfo_y())
            pb()
        text_field.after(100, alls)
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
    def chart(master, values, with_labels=False, width=50, color='blue', corner_radius=0, orientation='vertical'):
        values = [i for i in values if i != 0 and isinstance(i, (int, float))]
        if values:
            frame = _ctk.CTkScrollableFrame(master, orientation=orientation)
            data = [_ctk.CTkFrame(frame, fg_color=color, height=((i / sum(values))*100)+2, width=width, corner_radius=corner_radius) for i in values]
            CustomTk.tidy_up(data, len(data), start_row=0)
            frame.update()
            if with_labels:
                labels = []
                for i in range(len(data)):
                    labels.append(_ctk.CTkLabel(frame, text=values[i], font=('arial', 20)))
                CustomTk.tidy_up(labels, len(labels), start_row=1)
            frame.configure(width=frame.winfo_reqwidth(), height=frame.winfo_reqheight())
            return frame
    def history_binds(obj):
        old_func = obj.bind
        def bind(sequence=None, command=None, add=True):
            if not all([sequence, command]):
                v = [d.copy() for d in obj._binds]
                for d in v:
                    del d['id']
                return v
            else:
                old_func(sequence, command, add)
                ids = [d['id'] for d in obj._binds]
                v = {'id': obj.winfo_id(), 'sequence': sequence, 'command': command, 'add': add}
                if v['id'] not in ids:
                    obj._binds.append(v)
        if not hasattr(obj, '_binds'):
            setattr(obj, '_binds', [])
            setattr(obj, 'bind', bind)
    def apply_binds(obj1, obj2):
        """copy binds from obj1 to obj2
            Note: to make this function work out, you should call CustomTk.history_bind in it's correct place (like before make an event"""
        if hasattr(obj1, '_binds'):
            a = obj1._binds
            if a:
                for i in a:
                    obj2.bind(**i)
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
    def copy_text_style(widgets):
        wids = CustomTk.has_text_iterable(widgets)
        def c(obj1, obj2):
            atts = {}
            for i in ['fg_color', 'bg_color', 'font', 'text_color']:
                atts[i] = obj1.cget(i)
            obj2.configure(**atts)
        btn = CustomTk.from_to_widgets_event(widgets, c)
        btn.configure(text='copy style')
        return btn
    def dont_enter(entry, iterable):
        if entry.cget('textvariable'):
            check = entry.cget('textvariable')
        else:
            check = _ctk.StringVar()
            entry.configure(textvariable=check)
        def c(*args):
            if check.get()[-1] in iterable:
                entry.delete(entry.index('insert') - 1)
        check.trace_add('write', c)
    def len_entry(entry, text_with_num='', with_spaces=True):
        if entry.cget('textvariable'):
            check = entry.cget('textvariable')
        else:
            check = _ctk.StringVar()
            entry.configure(textvariable=check)
        label = _ctk.CTkLabel(entry.master, text=f'{text_with_num}0')
        def c(*args):
            lenth_text = len(check.get()) if with_spaces else len(check.get().replace(' ', ''))
            lenth_all = f"{text_with_num}{lenth_text}"
            label.configure(text=lenth_all)
        check.trace_add('write', c)
        return label
    def label_widget(obj, message, side='above', value=0, text_color='black', font=('arial', 10), fg_color=None):
        l = _ctk.CTkLabel(obj.master, text=message, text_color=text_color, font=font, fg_color=fg_color)
        obj.master.update()
        def m():
            l.lift()
            if side == 'above':
                l.place(x=obj.winfo_x(), y=obj.winfo_y()-obj.winfo_height()-value)
            else:
                l.place(x=obj.winfo_x(), y=obj.winfo_y()+obj.winfo_height()+value)
        obj.master.after(200, m)
    def entry_label(obj, func=None):
        is_label = isinstance(obj, _ctk.CTkLabel)
        event = "<Double-Button-1>" if is_label else "<Return>"
        atts = ['fg_color', 'text_color', 'font', 'corner_radius']
        if obj.cget('fg_color') == 'transparent':
            atts.remove('fg_color')
        attributes = {i: obj.cget(i) for i in atts}
        def convert(e):
            if is_label:
                a = _ctk.CTkEntry(obj.master)
                a.configure(border_color=a.cget('bg_color'))
            else:
                a = _ctk.CTkLabel(obj.master)
            a.configure(**attributes)
            a.configure(corner_radius=obj.cget('corner_radius')+1)
            if callable(func):
                func()
            def m():
                x = obj.winfo_x()
                y = obj.winfo_y()
                if is_label:
                    a.insert(0, obj.cget('text'))
                else:
                    a.configure(text=obj.get())
                a.place(x=x, y=y)
                obj.destroy()
                CustomTk.entry_label(a)
            obj.after(200, m)
        obj.bind(event, convert)
    def clone_widget(widget, master=None):
        """clone a widget with it's DNA with many properties like fg_color, text, text_color
        widget: is the widget to clone
        master: if you want to put the widget in another master or the widget's master if it's given
        apply_bind: call CustomTk.apply_bind(given widget, new widget), Note: to make this work out,
        call CustomTk.history_binds(widget) before cloning"""
        cls = widget.__class__
        new = cls(master or widget.winfo_toplevel())
        if isinstance(widget, _ctk.CTkScrollableFrame):
            new = cls(master or widget.winfo_toplevel(), orientation=widget._orientation)
        attr = ['bg_color', 'fg_color', 'text_color', 'text_color_disabled', 'corner_radius', 'anchor', 'text', 'wraplength', 'image', 'compound', 'font',
                'placeholder_text_color', 'border_color', 'border_width', 'placeholder_text', 'textvariable', 'state', 'border_spacing', 'hover_color',
                'background_corner_colors', 'hover', 'command', 'switch_width', 'switch_height',
                'progress_color', 'button_color', 'button_hover_color', 'button_length', 'variable', 'checkbox_width', 'checkbox_height', 'checkmark_color', 'width', 'height']
        widget.update()
        for i in attr:
            i = i.strip('_')
            try:
                new_config = {i: widget.cget(i)}
                new.configure(**new_config)
            except Exception as e:
                pass
        return new
    def clone_frame(frame, master=None):
        new_frame = CustomTk.clone_widget(frame, master or frame.winfo_toplevel())
        for i in frame.winfo_children():
            if isinstance(i, (_ctk.CTkFrame, _ctk.CTkScrollableFrame)):
                f = CustomTk.clone_frame
            else:
                f = CustomTk.clone_widget
            CustomTk.Manager.manager_same(i, f(i, new_frame))
        return new_frame
    def add_texts_to_file(master, file):
        _Files.make_if_not_exists(file, 'txt')
        new = CustomTk.has_text_iterable(CustomTk.all_objects(master))
        new = sorted(new, key=lambda i: str(i))
        new = [i.cget('text') for i in new]
        _Files.read_write_txt_file(file, 'write', str(new))
    def texts_from_file(master, file):
        _Files.make_if_not_exists(file, 'txt')
        text = _Files.read_write_txt_file(file)
        if text:
            lst = _ast.literal_eval(text)
            a = sorted(CustomTk.has_text_iterable(CustomTk.all_objects(master)), key=lambda w: str(w))
            for i, e in zip(a, lst):
                i.configure(text=e)
    def has_text(obj, with_empty=False):
        try:
            obj.cget('text')
            if with_empty:
                assert obj.cget('text').strip()
            return True
        except:
            return False
    def has_text_iterable(iterable, with_empty=False, text_obj=False):
        result = []
        for i in iterable:
            if CustomTk.has_text(i, with_empty):
                result.append(i)
        if text_obj:
            return {'texts': [t.cget('text') for t in result], 'widgets': result}
        return result
    def show_hide_message(master, message, text_color='red', font=('arial', 30), x=None, y=None, hide_after=1, in_btn=False):    
        if in_btn:
            cls = _ctk.CTkButton
        else:
            cls = _ctk.CTkLabel
        me = cls(master, text=message, font=font, text_color=text_color)
        def s():
            if not me.winfo_ismapped():
                if x and y:
                    me.place(x=x, y=y)
                else:
                    me.pack()
        s()
        me.after(int(hide_after*1000), me.destroy)
        return me
    def change_mode(master, light_icon='light', dark_icon='dark'):
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
    def sync_entry_with_label(entry, label):
        if entry.cget('textvariable'):
            var = entry.cget('textvariable')
        else:
            var = _ctk.StringVar()
        var.trace_add('write', lambda *args:label.configure(text=entry.get()))
        entry.configure(textvariable=var)
    def console(master, texts, per_row=3, entry_to_insert=None, font=('arial', 20), text_color='white', return_dic_frame_and_buttons=False):
        result = _ctk.CTkFrame(master)
        def create_button(text):
            if entry_to_insert:
                return _ctk.CTkButton(result, text=text, font=font, text_color=text_color, command=lambda: entry_to_insert.insert('end', text))
            return _ctk.CTkButton(result, text=text, font=font, text_color=text_color)
        buttons = [create_button(str(c)) for c in texts]
        CustomTk.tidy_up(buttons, per_row=per_row)
        if return_dic_frame_and_buttons:
            return {'frame': result, 'buttons': buttons}
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
            if entry.cget("show") == hide_with:
                entry.configure(show='')
                btn.configure(text=hide_ico)
            else:
                entry.configure(show=hide_with)
                btn.configure(text=show_ico)
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
    def good_size(widgets):
        """resize widgets with the biggest size (height, width)"""
        def m():
            width = [i.winfo_reqwidth() for i in widgets]
            height = [i.winfo_reqheight() for i in widgets]
            for i in widgets:
                i.configure(width=max(width), height=max(height))
        widgets[0].after(100, m)
    def sort_types(widgets, per_row, start_col=0, start_row=0, type_of='fg_color', orientation='vertical', leave_space=0, reverse=False, padx=0, pady=0):
        types = {str(i.cget(type_of)) for i in widgets if not _Math.int_or_float(i.cget(type_of))}
        if type_of == 'text':
            types = sorted(types, reverse=reverse)
            types_num = sorted({str(i.cget(type_of))
                    for i in widgets if _Math.int_or_float(i.cget(type_of))}, key=float, reverse=reverse)
            types = types + types_num
        wids = []
        for i in types:
            new = []
            for o in widgets:
                if str(o.cget(type_of)) == i:
                    new.append(o)
            if new:
                wids.append(new)
        widgets[0].master.update()
        for i in wids:
            CustomTk.tidy_up(i, per_row, start_column=start_col, start_row=start_row, padx=padx, pady=pady)
            if orientation == 'horizontal':
                start_col = int(i[-1].grid_info()['column']) + 1 + leave_space
            else:
                start_row = int(i[-1].grid_info()['row']) + 1 + leave_space
    def tidy_up(widgets, per_row, start_row=0, start_column=0, padx=5, pady=5):
        master = widgets[0].master
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
            if isinstance(i, (_ctk.CTkFrame, _ctk.CTkScrollableFrame)):
                result.extend(CustomTk.all_objects(i))
            else:
                result.append(i)
        return result
    def edit_all_widgets_texts(iterable, font='arial', size=20, text_color='lightblue', bg='', with_empty=False):
        """Apply font, text color, and background to all child widgets in master."""
        def m():
            for i in CustomTk.has_text(iterable, with_empty=with_empty):
                if bg:
                    i.configure(font=(font, size), text_color=text_color, fg_color=bg)    
                else:
                    i.configure(font=(font, size), text_color=text_color, fg_color='transparent')
        iterable[0].master.after(len(iterable) // 1000, m)
    def exit_esc(master):
        master.bind('<Escape>', lambda e: master.destroy())
    def info(widget, information, font='arial', size=20, bg='', hide_after=2):
        """Show a tooltip label below widget on hover, auto-hide after hide_after seconds."""
        def show(e):
            x = widget.winfo_x()
            y = widget.winfo_y()
            a = CustomTk.show_hide_message(widget.master, information, text_color='black', font=('arial', 20), x=x, y=y, hide_after=hide_after)
            widget.bind('<Leave>', lambda e: a.destroy())
        widget.bind('<Enter>', show)
    def mouse_wheel_num(entry, end, step=1):
        """Scroll through numbers inside an entry with the mouse wheel."""
        def f(e):
            if _Math.int_or_float(entry.get()):
                a = float(entry.get())
                entry.delete(0, 'end')
                if e.delta >= 1:
                    new_num = type(step)(a + step)
                else:
                    new_num = type(step)(a - step)
                if a == end:
                    new_num = 0
                entry.insert(0, round(new_num, 2))
        entry.bind("<MouseWheel>", f)
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
