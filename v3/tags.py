from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# We Could convert content to html like this
# but I still like to write something that can be reused in the future.

# def to_html(self) -> str:
#     html = "<table>{}</table>"
#     lines = []

#     indices = list(self.df.index)

#     lines.append('<tr>')
#     lines.append('<th>&nbsp;</th>')
#     for i, col in enumerate(self.df.columns):
#     lines.append(f"<th>{col}</th>")
#     lines.append('</tr>')

#     for i, _ in self.df.iterrows():
#     lines.append("<tr>")
#     lines.append(f"<th>{indices[i]}</th>")
#     for j, col in enumerate(df.columns):
#         lines.append(f"<td>{self.df.iloc[i,j]}</td>")
#     lines.append("</tr>")
#     return html.format("\n".join(lines))

def create_tag(tag:str, attrs:dict = None) -> str:
    
    """Create an html tag with attributes
    Args:
        tag (str): tag name
        attrs (dict): attributes, key being attribute name, value being attribute value

    Returns:
        str: html tag"""


    if attrs is None:
        return f"<{tag}>"
    
    str_attrs = [f'{k}="{v}"' for k,v in attrs.items() if isinstance(v, str)]
    num_attrs = [f'{k}={v}' for k,v in attrs.items() if isinstance(v, (int, float))]
    attrs = " ".join(str_attrs + num_attrs)
    return f"<{tag} {attrs}>"


def wrap_with_tag(content:str, tag:str, attrs:dict = None) -> str:
    
    """Wrap content with html tag
    Args:
        content (str): content to be wrapped
        tag (str): tag name
        attrs (dict): attributes, key being attribute name, value being attribute value

    Returns:
        str: content wrapped with html tag"""

    return create_tag(tag, attrs) + str(content) + f"</{tag}>"


class Element:
    def __init__(self, content:Any=""):
        self.content = content

    def _name(self):
        if hasattr(self, "name") and (self.name is not None):
            return self.name
        return self.__class__.__name__

    def _attrs(self):
        if not hasattr(self, "attrs"):
            return None
        return self.attrs

    def html(self):
        if isinstance(self.content,list):
            content = "\n".join([c.html() for c in self.content])
        elif isinstance(self.content, Element):
            content = self.content.html() + "\n"
        else:
            content = self.content
        return wrap_with_tag(content, self._name(), self._attrs())


@dataclass
class td(Element):
    """Table Cell element"""
    row:int
    col:int
    content:Any=""
    table_id:str = "df_table"
    attrs:dict = None

    def __post_init__(self):
        class_attr = f'data row{self.row} col{self.col}'
        id_attr = f"{self.table_id}_row{self.row}_col{self.col}"
        attrs = self.attrs or {}
        attrs.update({"class": class_attr, "id": id_attr})
        self.attrs = attrs


@dataclass
class th_col(Element):
    """Column header of a table"""
    content:Any=""
    table_id:str = "df_table"
    level:int = 0
    col:int = None
    attrs:dict = None
    name:str = "th"

    def __post_init__(self):
        class_attr = f'col_heading level{self.level} col{self.col}'
        id_attr = f"{self.table_id}_level{self.level}_col{self.col}"
        attrs = self.attrs or {}
        attrs.update({"class": class_attr, "id": id_attr})
        self.attrs = attrs


@dataclass
class th_row(Element):
    """Row header of a table"""
    content:str=""
    table_id:str = "df_table"
    level:int = 0
    row:int = None
    attrs:dict = None
    name:str = 'th'

    def __post_init__(self):
        class_attr = f'row_heading level{self.level} row{self.row}'
        id_attr = f"{self.table_id}_level{self.level}_row{self.row}"
        attrs = self.attrs or {}
        attrs.update({"class": class_attr, "id": id_attr})
        self.attrs = attrs

@dataclass
class tr(Element):
    """Row element"""
    content:str=""
    attrs:dict = None

@dataclass
class table(Element):
    content:str=""
    id:str="df_table"
    attrs:dict = None

    def __post_init__(self):
        id_attr = {'id': self.id}
        attrs = self.attrs if self.attrs is not None else {}
        attrs.update(id_attr)
        self.attrs = attrs


if __name__ == "__main__":

    def print_content(ele):
        print("*"*100)
        print(ele.html())

    print_content(
        table("hello table", attrs = {'bakcground':"yhellow"})
    )

    mytable = table([
        tr(),
        tr(), 
        tr()
        ], 
        attrs = {'u':'v'})
    print_content(mytable)


    mytable = table([
        tr([th_col("", col=0),       th_col("col1", col = 1), th_col("col2", col = 2), th_col("col3", col = 3)]),
        tr([th_row("row1", row=1),   td(1,1,"Hello"),         td(1,2,"World"),         td(1,3,"Man")]),
        tr([th_row("row2", row=2),   td(2,1,"Myname"),        td(2,2,"is"),            td(2,3,"Peter")]), 
        ], 
        attrs = {'border':'3'})
    print_content(mytable)

    with open("tags.html",'w') as f:
        f.write(mytable.html())

