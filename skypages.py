# -*- coding: utf-8 -*-
"""
@author kasekun
@name Jesse Swan
"""
import os.path

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from matplotlib.figure import Figure
from matplotlib.widgets import Slider

from astropy.visualization import PowerStretch, ImageNormalize, ZScaleInterval, LogStretch
from astropy.io import fits

import tkinter as tk
from tkinter import ttk

import json

import os
try: print(__file__)
except: __file__ = os.path.abspath(os.path.join(os.curdir, 'jnk.jnk')) # ipython copy-paste hack
thisdir = os.path.dirname(os.path.abspath(__file__))
datapath = os.path.join(thisdir, 'skydata')

LARGE_FONT= ("Verdana", 12)

"""
TODO: Incorperate additional images into json and tkinter pages
TODO: Match 'zoom' of image across all pages
TODO: Relocate buttons for page toggling
TODO: Relocate contrast and normalisation sliders
TODO: Add additional normalisation options (currently 'LogNorm', 'Powernorm')
TODO: Make selection of normalisation a button toggle within tkinter frames
TODO: Add colourmap options to config (rather than 'cividis' default)
TODO: Make modular classes less reliant on copy-paste
"""


class NavigationToolbar(NavigationToolbar2Tk):
    """
    Customise the matplotlib navigation toolbar
    """
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


class SkyToyClass(tk.Tk):
    """
    Parent containter for pages of various sky images
    """

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "SkyToy")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (UPage, GPage, RPage, IPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(UPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class UPage(tk.Frame):
    """
    Page for u-band photometry
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="u", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="optical g",
                            command=lambda: controller.show_frame(GPage))
        button.pack()

        button2 = ttk.Button(self, text="optical r",
                             command=lambda: controller.show_frame(RPage))
        button2.pack()

        button3 = ttk.Button(self, text="optical i",
                             command=lambda: controller.show_frame(IPage))
        button3.pack()

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

        def update(val):
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


class GPage(tk.Frame):
    """
    Page for g-band photometry
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="optical g", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="optical u",
                            command=lambda: controller.show_frame(UPage))
        button.pack()

        button2 = ttk.Button(self, text="optical r",
                             command=lambda: controller.show_frame(RPage))
        button2.pack()

        button3 = ttk.Button(self, text="optical i",
                             command=lambda: controller.show_frame(IPage))
        button3.pack()


class RPage(tk.Frame):
    """
    Page for r-band photometry
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="optical r", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="optical g",
                            command=lambda: controller.show_frame(GPage))
        button.pack()

        button2 = ttk.Button(self, text="optical u",
                             command=lambda: controller.show_frame(UPage))
        button2.pack()

        button3 = ttk.Button(self, text="optical i",
                             command=lambda: controller.show_frame(IPage))
        button3.pack()


class IPage(tk.Frame):
    """
    Page for i-band photometry
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="optical i", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="optical g",
                            command=lambda: controller.show_frame(GPage))
        button.pack()

        button2 = ttk.Button(self, text="optical r",
                             command=lambda: controller.show_frame(RPage))
        button2.pack()

        button3 = ttk.Button(self, text="optical u",
                             command=lambda: controller.show_frame(UPage))
        button3.pack()

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

        stretch_options = {'LogStretch': LogStretch(power_normalise),
                           'PowerStretch': PowerStretch(power_normalise), }

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

        def update(val):
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


def LoadJson():
    """
    Load configuration information
    :return: configuration values
    """
    filepath = os.path.join(thisdir, 'sky_config.json')
    json_data = json.load(open(filepath))
    json_path = json_data.get('path')
    json_image_scaling = json_data.get('image_scaling')
    json_image_contrast = json_data.get('image_contrast')
    json_max_saturation = json_data.get('max_saturation')
    json_power_normalise = json_data.get('power_normalise')

    return json_path, json_image_scaling, \
           json_image_contrast, json_max_saturation, json_power_normalise


# save dato to json file
def SaveJson(p_normalise, contrast):
    """
    Save slider adjusted values to config file
    :param p_normalise: slider-adjusted normalisation value
    :param contrast: slider-adjusted contrast value
    :return: None
    """
    filepath = os.path.join(thisdir, 'sky_config.json')
    json_data = json.load(open(filepath))

    json_data['power_normalise'] = p_normalise
    json_data['image_contrast'] = contrast

    jsonFile = open(filepath, 'w+')
    jsonFile.write(json.dumps(json_data, indent=2))
    jsonFile.close()


if __name__ == '__main__':
    image_path, image_scaling, image_contrast, \
    max_saturation, power_normalise = LoadJson()

    sky_image = os.path.join(thisdir, image_path)

    app = SkyToyClass()
    app.mainloop()

    print('\nQuitting')
