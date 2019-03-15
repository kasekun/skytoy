# -*- coding: utf-8 -*-
"""
@author kasekun
@name Jesse Swan

Note: This is obsolete please use and contribute to skypages
"""
import os.path

import matplotlib
matplotlib.use("TkAgg")
# matplotlib.rcParams['toolbar'] = 'None'
# matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.figure import Figure
from matplotlib.widgets import Slider

from astropy.visualization import PowerStretch, ImageNormalize, ZScaleInterval, LogStretch
from astropy.io import fits

import tkinter as tk
import json

class NavigationToolbar(NavigationToolbar2Tk):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

class SkyToyClass(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "SkyToy")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = SkyFrame(container, self)
        self.frames[SkyFrame] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SkyFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class SkyFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

# change 'figure_width': 1920, 'figure_height': 1080 =(19.2,10.8)
        f = Figure(figsize=(8, 6))
        a = f.add_subplot(111)
        f.subplots_adjust(left=0, bottom=0.005, right=1, top=1)
        a.get_xaxis().set_visible(False)
        a.get_yaxis().set_visible(False)              
        
        # add axes for sliders 
        ax_norma = f.add_axes([0.81, 0.1, 0.15, 0.025])
        ax_contr = f.add_axes([0.81, 0.05, 0.15, 0.025])

        hdu_list = fits.open(sky_image)
        hdu_list.info()
        img = hdu_list[0].data

        contrast = image_contrast
        interval = ZScaleInterval(contrast=contrast)
        vmin, vmax = interval.get_limits(img)

        stretch_options = {'LogStretch': LogStretch(power_normalise), 'PowerStretch': PowerStretch(power_normalise), }

        norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=stretch_options[image_scaling])

        a.imshow(img, origin='lower', norm=norm, cmap='cividis')

        # Embedding In Tk
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Show ToolBar
        toolbar = NavigationToolbar(canvas, self)
        toolbar.update()
        # Activate Zoom
        toolbar.zoom(self)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        delta_f = 0.1

        # add sliders
        s_norma = Slider(ax_norma, 'Normalise', 0.1, 5.0, valinit=power_normalise, valstep=delta_f)
        s_contr = Slider(ax_contr, 'Contrast', 0.1, 1.0, valinit=contrast)


        def update():
            n_norma = s_norma.val
            n_contr = s_contr.val
            # assign new values to contrast and normalise
            interval = ZScaleInterval(contrast=n_contr)
            vmin, vmax = interval.get_limits(img)
            norm = ImageNormalize(vmin=vmin, vmax=vmax, stretch=PowerStretch(n_norma))
            a.imshow(img, origin='lower', norm=norm, cmap='cividis')
            # saving data to json file
            SaveJson(n_norma, n_contr)
            canvas.draw_idle()
        s_norma.on_changed(update)
        s_contr.on_changed(update)

        hdu_list.close()

# load config dato from json file
def LoadJson():

        filepath = os.path.realpath('../skytoy/sky_config.json')
        json_data = json.load(open(filepath))
        json_path = json_data.get('path')
        json_image_scaling = json_data.get('image_scaling')
        json_image_contrast = json_data.get('image_contrast')
        json_max_saturation = json_data.get('max_saturation')
        json_power_normalise = json_data.get('power_normalise')

        return json_path, json_image_scaling, \
            json_image_contrast, json_max_saturation, json_power_normalise


# save dato to json file
def SaveJson(p_normalise, contr):
        filepath = os.path.realpath('../skytoy/sky_config.json')
        json_data = json.load(open(filepath))

        json_data['power_normalise'] = p_normalise
        json_data['image_contrast'] = contr
        # save changes to json file
        jsonFile = open(filepath, 'w+')
        jsonFile.write(json.dumps(json_data, indent=2))
        jsonFile.close()


if __name__ == '__main__':
    # loads JSON file parameters
    path, image_scaling, image_contrast, \
        max_saturation, power_normalise = LoadJson()

    # loads Image
    sky_image = os.path.realpath('../' + path)

    app = SkyToyClass()
    app.mainloop()

    print('Quitting')
