from __future__ import annotations
import pandas as pd
from typing import Protocol, Callable
import tags

from IPython.display import display, HTML

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
        """Convert a styled table to html"""

        header = tags.tr(
            [tags.th_col("&nbsp;",col = 0)] + \
            [tags.th_col(col,col=i+1) for i, col in enumerate(self.df.columns)])

        indices = list(self.df.index)
        cells = []

        for i, _ in self.df.iterrows():
            row_index = tags.th_row(indices[i], row=i+1)
            row_contents = [tags.td(i+1, j+1, content = self.df.iloc[i,j]) 
                                for j, col in enumerate(self.df.columns)]

            cells.append(tags.tr([row_index] + row_contents))

        return tags.table([header] + cells, id = "df_table", attrs = {'border':'3'}).html()

    def display(self) -> None:
        display(HTML(self.to_html()))


if __name__ == "__main__":
    import numpy as np
    df = pd.DataFrame(
        np.random.randn(10, 4), 
        columns = ['A','B','C','D']
    )

    print("Converting dataframe to html")
    fname = 'styler.html'
    html = Styler(df).format(lambda x:x >0, subset =['A']).to_html()
    with open(fname,'w') as f:
        f.write(html)
    print(f"Data saved to {fname}, Done.")


