#!/usr/bin/python

# The XML Stuff (need python 2.5+)
from xml.etree.ElementTree import XML as xml
from xml.etree.ElementTree import tostring as xml_to_string

# The GTK Stuff
import gtk.gdk as gdk
import gtk.glade

# The SVG Stuff
import cairo
import rsvg


class Flyer:
    def __init__(self):
        self.glade_file = "gui.glade"
        self.drawing = "drawing.svg"
        self.wTree = gtk.glade.XML(self.glade_file)
        self.window = self.wTree.get_widget("main_window")
        self.wTree.signal_autoconnect(self)
        self.window.show()
        self.svg_data = open(self.drawing).read()

    def on_main_window_destroy(self, window):
        gtk.main_quit( )

    def _update_svg(self, text, name):
        dom = xml(self.svg_data)
        text_fields = dom.findall(".//{http://www.w3.org/2000/svg}text")
        label = '{http://www.inkscape.org/namespaces/inkscape}label'
        for text_field in text_fields:
            if (text_field.get(label) == "#" + name) or \
                    (text_field.get("id") == name):
                span = text_field[0]
                span.text = text
        self.svg_data = xml_to_string(dom)
        self.window.queue_draw()

    def on_event_title_entry_editing_done(self, entry, event):
        text = entry.get_text()
        self._update_svg(text, "title")


    def on_event_loc1_entry_editing_done(self, entry, event):
        text = entry.get_text()
        self._update_svg(text, "loc1")

    def on_event_loc2_entry_editing_done(self, entry, event):
        text = entry.get_text()
        self._update_svg(text, "loc2")

    def on_event_date1_entry_editing_done(self, entry, event):
        text = entry.get_text()
        self._update_svg(text, "date1")

    def on_event_date2_entry_editing_done(self, entry, event):
        text = entry.get_text()
        self._update_svg(text, "date2")

    def save_svg_button_released(self, event):
        f = open("flyer.svg", "w")
        f.write(self.svg_data)
        f.close()
        print "Saved as SVG"

    def save_pdf_button_released(self, event):
        svg = rsvg.Handle(data=self.svg_data)
        svg_width, svg_height = svg.get_dimension_data()[:2]

        surface = cairo.PDFSurface("flyer.pdf", 
                                   svg_width, svg_height)
        cr = cairo.Context(surface)
        svg.render_cairo(cr)

        print "Saved as PDF"

    def save_png_button_released(self, event):
        svg = rsvg.Handle(data=self.svg_data)

        svg_width, svg_height = svg.get_dimension_data()[:2]
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 
                                     svg_width, svg_height)
        cr = cairo.Context(surface)
        svg.render_cairo(cr)

        surface.write_to_png("flyer.png")
        print "Saved as PNG"

    def on_save_all_button_released(self, event):
        self.save_png_button_released(event)
        self.save_pdf_button_released(event)
        self.save_svg_button_released(event)

    def on_svgarea_expose_event(self, widget, event):
        cr = widget.window.cairo_create( )

        width = event.area.width
        height = event.area.height

        svg = rsvg.Handle(data=self.svg_data)

        svg_width, svg_height = svg.get_dimension_data()[:2]
        scale_x = float(width)/svg_width
        scale_y = float(height)/svg_height
        
        cr.scale( scale_x, scale_y )

        svg.render_cairo(cr)

        return False

def main( ):
    Flyer( )
    gtk.main( )

if __name__ == "__main__": main( )

