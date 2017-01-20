#coding=utf8
#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re


if __name__ == "__main__":
    df1 = pd.DataFrame({'key':['b', 'b', 'a', 'c', 'a', 'a', 'b'],
                        'data1':range(7)})

    df2 = pd.DataFrame({'key': ['a', 'b', 'd'],
                        'data2': range(3)})


    # print df2
    # print pd.merge(df1, df2, how='right')

    data = {'Dave': 'dave@google.com', 'Steve': 'Steve@gmail.com',
            'Rob': 'rob@gmail.com', 'Wes':np.nan}
    data = pd.Series(data)
    print data.str.contains('gmail')
