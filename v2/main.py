from __future__ import annotations
import pandas as pd
from typing import Protocol, Callable

from IPython.display import display, HTML

"""
what is a styler object?
styler is an object of type pandas.io.formats.style.Styler

1. styler has a format function
you can pass a formatter to styler.format() function
df.style.format(precision=0, na_rep='MISSING', thousands=" ",
                formatter={('Decision Tree', 'Tumour'): "{:.2f}",
                           ('Regression', 'Non-Tumour'): lambda x: "$ {:,.1f}".format(x*-1e6)
                          })

2. you can also pass a function to styler.format() function
def rain_condition(v):
    if v < 1.75:
        return "Dry"
    elif v < 2.75:
        return "Rain"
    return "Heavy Rain"
styler.format(rain_condition)

3. styler has a format_index function
which also receives a function parameter
styler.format_index(lambda v: v.strftime("%A"))

4. styler has a caption function, which adds a title to a dataframe
styler.set_caption("Weather Conditions")

5. styler has a gradient function, which set colorbar of a dataframe / rows or columns
styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
"""




class StyledDataFrame:
    """A Styled DataFrame has an attribute `style` which is a Styler object"""

    def __init__(self, df:pd.DataFrame):
        self.df = df
        
    @property
    def style(self) -> Styler:
        return Styler(self.df)

    def to_html(self):
        return self.style.to_html()


class StylerProtocol(Protocol):
    """A Styler does 2 things: 1. format dataframe 2. convert dataframe to html string"""

    def format(self, formatter:Callable, subset:list = None) -> Styler:
        """use formatter to format dataframe, the core of this function is to alter dataframe inplace"""

    def to_html(self) -> str:
        """convert styler object to html string"""


class Styler:

    def __init__(self, df):
        self.df = df.copy()

    def format(self, formatter:Callable, subset:list = None) -> Styler:
        subset = subset or self.df.columns
        for col in subset:
            # use formatter to alter dataframe inplace
            self.df[col] = self.df[col].apply(formatter)

        # return self object of a new Styler object with altered dataframe
        return Styler(self.df)

    def to_html(self) -> str:
        """for simplicity, we only use dataframe.style.to_html() to implement the html conversion"""
        return self.df.style.to_html()

    def display(self) -> None:
        display(HTML(self.to_html()))


if __name__ == "__main__":
    import numpy as np
    df = pd.DataFrame(
        np.random.randn(10, 4), 
        columns = ['A','B','C','D']
    )

    html = Styler(df).format(lambda x:x >0, subset =['A']).to_html()
    print(html)


