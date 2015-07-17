# -*- coding: utf-8 -*-

import os
import os.path

if os.path.exists('./logs'):
    pass
else:
   os.makedirs('./logs')
   print '创建log目录完成'
