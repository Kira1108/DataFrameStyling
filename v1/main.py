import numpy as np
import pandas as pd


if __name__ == "__main__":
    df = pd.DataFrame(
        np.random.randn(10, 4), 
        columns = ['A','B','C','D']
    )


    df.to_html("dataframe.html")
    df.style.to_html("style.html")
    
    style = df.style.background_gradient(
        axis=None, cmap="YlGnBu"
    )

    style.to_html("style_background.html")
    print(type(style))
    #<class 'pandas.io.formats.style.Styler'>


    obj = style.format(lambda x:x > 0)
    print(type(obj))