import re
import math
import numpy as np

def generate_rgb_list(array, midpoint=None, R=[248,255,99], G=[105,235,190], B=[107,132,123]):
    
    '''传入一个Series，返回rgb三元组列表。'''

    center = (array.max()+array.min())/2 if midpoint == 'middle' else array.median() if midpoint == 'median' else 0

    rgb = []
    for x in array:        
        d = x-center
        if d:
            k = d/(array.max()-center if d>0 else array.min()-center)
            r = R[1] + (math.ceil(k*(R[2]-R[1])) if d>0 else math.floor(k*(R[0]-R[1])))
            g = G[1] + (math.ceil(k*(G[2]-G[1])) if d>0 else math.floor(k*(G[0]-G[1])))
            b = B[1] + (math.ceil(k*(B[2]-B[1])) if d>0 else math.floor(k*(B[0]-B[1])))
		# 全元素相等时，默认皆为最大值。
        elif center==array.max(): 
            r = R[1] + (R[2]-R[1])
            g = G[1] + (G[2]-G[1])
            b = B[1] + (B[2]-B[1])
        elif center==array.min():
            r = R[1] + (R[0]-R[1])
            g = G[1] + (G[0]-G[1])
            b = B[1] + (B[0]-B[1])
        else:
            r = R[1]
            g = G[1]
            b = B[1]
        rgb.append((r,g,b))

    return rgb

def html_add_color_by_col(html, rgb, icol, row_offset=0):
    
    '''
    html：df.to_html()
    rgb：rgb三元组列表
    icol：需要添加色阶的列号
    row_offset：行偏移
    '''
    
    m = re.match(r'(\<table.*?\>\s*\<thead\>.*?\<\/thead\>)\s*(\<tbody\>.*?\<\/tbody\>\s*\<\/table\>)', html.replace('\n',''))
    head = m.group(1)
    body = m.group(2)
    body_list = body.split('</tr>')
    

    row_list = body_list[:row_offset]
    for i in np.arange(len(rgb)):
        row = body_list[row_offset+i]
        row = row.replace('<td>',f'<td style="background-color:rgb{rgb[i]}">',icol+1)\
                 .replace(f'<td style="background-color:rgb{rgb[i]}">','<td>',icol)
        row_list.append(row)
    row_list += body_list[row_offset+len(rgb):]

    return head+'</tr>'.join(row_list)


def html_add_color_by_row(html, rgb, irow, col_offset=0):

    '''
    html：df.to_html()
    rgb：rgb三元组列表
    irow：需要添加色阶的行号
    col_offset：列偏移
    '''
    
    m = re.match(r'(\<table.*?\>\s*\<thead\>.*?\<\/thead\>)\s*(\<tbody\>.*?\<\/tbody\>\s*\<\/table\>)', html.replace('\n',''))
    head = m.group(1)
    body = m.group(2)
    body_list = body.split('</tr>')
    
    row_list = body_list
    row = body_list[irow].replace('<td>','<td style="background-color:white">',col_offset)
    for i in np.arange(len(rgb)):
        row = row.replace('<td>',f'<td style="background-color:rgb{rgb[i]}">',1)
    row_list[irow] = row.replace('<td style="background-color:white">','<td>',col_offset)

    return head+'</tr>'.join(row_list)


def df_to_html_with_color(df, by_cols=None, start_row=None, end_row=None, by_rows=None, start_col=None, end_col=None, midpoint=None, max_color=[99,190,123], mid_color=[255,235,132], min_color=[248,105,107]):
    
    '''
    df：DateFrame
    by_cols：按列添加色阶，传入列名或列号list，所有列可传入'all'
    start_row：按列操作时限定行范围，传入起始行号，默认为第一行
    end_row：按列操作时限定行范围，传入结束行号+1，默认为第一列
    by_rows：按行添加色阶，传入行号list，所有行可传入'all'
    start_col：按行操作时限定列范围，传入起始列名或列号，默认为第一列
    end_col：按行操作时限定列范围，传入结束列名或列号+1，默认为最后一列
    midpoint：中点类型，可指定'medain'或'middle'，否则默认为0
    max_color：最大值RGB色值
    mid_color：中点值RGB色值
    min_color：最小值RGB色值
    '''
    
    html = df.to_html(index=True).replace('\n','')
    R = [min_color[0],mid_color[0],max_color[0]]
    G = [min_color[1],mid_color[1],max_color[1]]
    B = [min_color[2],mid_color[2],max_color[2]]
    
    if by_cols:
        by_cols = np.arange(len(df.columns)) if by_cols == 'all' else df.columns.get_indexer(by_cols) if isinstance(by_cols[0],str) else by_cols
        for icol in sorted(by_cols,reverse=True):  # 只能从后往前填色
            rgb = generate_rgb_list(df.iloc[start_row:end_row,icol], midpoint=midpoint, R=R, G=G, B=B)
            html = html_add_color_by_col(html, rgb, icol=icol, row_offset=start_row if start_row else 0)
    elif by_rows:
        by_rows = np.arange(len(df)) if by_rows == 'all' else by_rows
        start_col = df.columns.get_loc(start_col) if isinstance(start_col,str) else start_col
        end_col = df.columns.get_loc(end_col) if isinstance(end_col,str) else end_col
        for irow in sorted(by_rows):
            rgb = generate_rgb_list(df.iloc[irow,start_col:end_col], midpoint=midpoint, R=R, G=G, B=B)
            html = html_add_color_by_row(html, rgb, irow=irow, col_offset=start_col if start_col else 0)

    return html
