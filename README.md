# Styling DataFrame

It is a quite easy job, but you can learn something.
![styled_table](https://user-images.githubusercontent.com/17697154/203257309-f87a5d69-8c3d-45a5-bdd2-5988ad97731b.png)             
*This table colorfy is implemented in v4 version*


Usage
```python
mystyle = compose(
    Beautify(caption = "This is a Pretty Table", cell_padding = '10px'),
    RowColorfy(subset = ['A','B']),
    ColumnColorfy(subset = ['C'], cmap = 'twilight'),
    Colorfy(subset = ['D','E','F'], cmap = 'Spectral'),
    HideIndex()
)

mystyle(df).to_html("very_beautiful_table.html")
```

Not implemented but a better way to normalize color scale with a center
```python
import numpy as np
import pandas as pd

from matplotlib import colors

# specify vmin, vcenter and vmax
divnorm=colors.TwoSlopeNorm(vmin=-3., vcenter=0., vmax=3)
df = pd.DataFrame(np.random.normal(0,1,(10,2)),columns=['a','b'])

# convert using a gmap object
df.style.background_gradient(cmap='RdYlGn',gmap = divnorm(df).data, axis = None)
```
