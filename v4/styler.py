from abc import ABC, abstractmethod
import pandas as pd
from pandas.io.formats.style import Styler
from dataclasses import dataclass
from functools import partial
from functools import reduce


class DfStyler(ABC):

    def _to_style(self, df):
        if isinstance(df, Styler):
            return df
        elif isinstance(df, pd.DataFrame):
            return df.style
        else:
            raise TypeError("df must be either a Styler or a DataFrame")

    @abstractmethod
    def set_style(self,s:Styler) -> Styler:
        ...

    def convert(self, df) -> Styler:
        return self.set_style(self._to_style(df))

    def __call__(self, df) -> Styler:
        return self.convert(df)


class Beautify(DfStyler):

    def __init__(self, 
        caption = None, 
        caption_side:str = "top", 
        header_background:str = "#f0f0f0", 
        header_font_color:str = "black", 
        cell_padding = "5px"):

        self.caption = caption
        self.caption_side = caption_side

        self.cell_hover = {
            'selector': 'td:hover',
            'props': [('background-color', 'white'),("color",'black')]
        }

        self.headers = {
            'selector': 'th',
            'props':  f'color: {header_font_color}; background-color: {header_background};'
        }

        self.table_elements = {
            "selector":"table, td, th",
            "props": f"border: 1px solid gray; padding:{cell_padding};",
        }
    
    def set_style(self, s) -> Styler:
        if self.caption:
            s.set_caption(self.caption)\
            .set_table_styles([{
                'selector': 'caption',
                'props': f'caption-side: {self.caption_side}; font-size: 3em;'
            }], overwrite=False)

        s.set_table_styles([self.cell_hover,self.table_elements, self.headers])
        s.set_table_attributes('style="border-collapse: collapse; border: 1px solid black;"')
        return s

@dataclass
class Colorfy(DfStyler):
    
    subset: list = None
    vmin: float = None
    vmax: float = None
    axis:int = None
    cmap:str='RdYlGn'
    low: float = 0
    high: float = 0
    text_color_threshold: float = 0.408


    def set_style(self,s:Styler) -> Styler:
        s.background_gradient(
            subset=self.subset, 
            axis=self.axis, 
            vmin=self.vmin, 
            vmax=self.vmax, 
            cmap=self.cmap, 
            low=self.low, 
            high=self.high, 
            text_color_threshold=self.text_color_threshold
        )
        return s

RowColorfy = partial(Colorfy, axis=1)
RowColorfy.__doc__ == Colorfy.__doc__

ColumnColorfy = partial(Colorfy, axis=0)
ColumnColorfy.__doc__ == Colorfy.__doc__

class HideIndex(DfStyler):
    def set_style(self,s:Styler) -> Styler:
        s.hide(axis = 'index')
        return s

def compose(*func):
    def _compose(f, g):
        return lambda x : g(f(x))
    return reduce(_compose, func, lambda x : x)

if __name__ == "__main__":
    import numpy as np
    df = pd.DataFrame(np.random.random((10, 7)), columns = ['A','B','C','D','E','F','G'])

    ########## Use DfStyle Funtionally ##########
    # a functional way to apply multiple styles
    beautier = Beautify(caption = "This is a Pretty Table")
    s = beautier(df)

    row_color = RowColorfy(subset = ['A','B'])
    row_color(s)

    col_color = ColumnColorfy(subset = ['C'])
    col_color(s)

    fram_color = Colorfy(subset = ['D','E','F'])
    fram_color(s)

    print(s.to_html())


    ########## Construct a styler pipeline ##########
    mystyle = compose(
        Beautify(caption = "This is a Pretty Table", cell_padding = '10px'),
        RowColorfy(subset = ['A','B']),
        ColumnColorfy(subset = ['C'], cmap = 'twilight'),
        Colorfy(subset = ['D','E','F'], cmap = 'Spectral'),
        HideIndex()
    )

    mystyle(df).to_html("very_beautiful_table.html")