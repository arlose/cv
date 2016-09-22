# -*- coding: utf-8 -*-
import os
import codecs 

l = ["鸡蛋","玉米","茄子-长","茄子-圆","番茄","胡萝卜","青椒-长","青椒-圆","冬瓜","黄瓜","苦瓜","丝瓜","西葫芦","洋葱","蒜苔","青菜","菜花","西兰花","菠菜","芹菜","生菜","莴笋","空心菜","苹果","梨","葡萄","橙","金针菇","平菇","香菇","酸奶","豆腐"]

for word in l:
    os.system("convert -fill black -background white -bordercolor white -border 4 -font simkai.ttf -pointsize 18 label:\"%s\" \"%s.png\""%((word), word))


