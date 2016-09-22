#!/usr/bin/env python
#-*- coding: utf-8 -*-

#from __future__ import division
from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk
import os
import sys
import glob
import random

# colors for the bboxes
#COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']
COLORS = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
# image sizes for the examples
SIZE = 256, 256

IMAGESIZE = 800
# image format
Image_FORMAT = ['.jpg', '.JPG', 'jpeg', '.JPEG', '.png', '.PNG']

class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.parent = master
        self.parent.title("图像标记工具")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)

        # initialize global state
        #self.imageDir = ''
        self.imageList= []
        #self.egDir = ''
        #self.egList = []
        # tag file storage path
        self.outDir = ''
        # the position of the current display image in the self.imageList
        self.cur = 0
        # total number of image in the self.imageList
        self.total = 0
        self.category = None
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.clearAll = False
        # the width and height of the original image
        self.img_Width = 0
        self.img_Height = 0

        # initizlize radiobutton
        self.var = IntVar()
        self.radio = []
        self.radioName = []

        # initialize widthRate heightRate
        #self.widthRate = 0.0
        #self.heightRate = 0.0
        self.scaleRate = 0.0	

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.hl = None
        self.vl = None

        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "图像 地址:")
        self.label.grid(row = 0, column = 0, sticky = E)
        self.entry = Entry(self.frame)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "加载", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 2, sticky = W+E)

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        #self.parent.bind("s", self.cancelBBox)
        #self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        #self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 1, column = 1, rowspan = 5, sticky = W+N)
        self.mainPanel.config(width = IMAGESIZE, height = IMAGESIZE)

        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = '画框信息:')
        self.lb1.grid(row = 1, column = 2,  sticky = W+N)
        self.listbox = Listbox(self.frame, width = 30, height = 16)
        self.listbox.grid(row = 2, column = 2, sticky = N)
        self.btnDel = Button(self.frame, text = '删除', command = self.delBBox)
        self.btnDel.grid(row = 3, column = 2, sticky = W+E+N)
        self.btnClear = Button(self.frame, text = '清空', command = self.clearBBox)
        self.btnClear.grid(row = 4, column = 2, sticky = W+E+N)

        # change category
        self.btnChange = Button(self.frame, text = "类别修改", command = self.changeCate)
        self.btnChange.grid(row = 5, column = 2, sticky = W+E+N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 6, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< 前一张', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='后一张 >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtncp = Button(self.ctrPanel, text='后一张(copy) >>', width = 10, command = self.nextcpImage)
        self.nextBtncp.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "图片:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "前往图片 No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)
        
        '''
	# example pannel for illustration
        self.egPanel = Frame(self.frame, border = 10)
        self.egPanel.grid(row = 1, column = 0, rowspan = 5, sticky = N)
        self.tmpLabel2 = Label(self.egPanel, text = "")
        self.tmpLabel2.pack(side = TOP, pady = 5)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(Label(self.egPanel))
        	self.egLabels[-1].pack(side = TOP)
       	'''		
	
        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

        #　display radiobutton
        self.radioLabel = Label(self.frame)
        self.radioLabel.grid(row=7, column=0, columnspan=3)
        
        self.radioPanel = Frame(self.frame)
        self.radioPanel.grid(row=8, column=0, columnspan=3)
        word_fi = open("words.txt", 'r')
        line_i = 0		
        for line in word_fi.readlines():
            self.radio.append(Radiobutton(self.radioPanel, text=line.strip(), variable=self.var, value=line_i+1, command=self.selRadio, width = 9, anchor=NW))
            self.radioName.append(line.strip())
            self.radio[line_i].grid(row=int(line_i/8), column=(line_i)%8, sticky = W)
            line_i = line_i+1
        if line_i == 0:
            return
        self.var.set(1)
        self.selRadio()
        """
        self.radio1 = Radiobutton(self.frame, text="Option 1", variable=self.var, value=1, command = self.selRadio)
        self.radio1.grid(row=7, column=0)
        self.radio2 = Radiobutton(self.frame, text="Option 2", variable=self.var, value=2, command = self.selRadio)
        self.radio2.grid(row=7, column=1)
        self.radio3 = Radiobutton(self.frame, text="Option 3", variable=self.var, value=3, command = self.selRadio)
        self.radio3.grid(row=7, column=2)
        self.var.set(1)
       	"""		

        # for debugging
##        self.setImage()
##        self.loadDir()

    def changeCate(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        # self.mainPanel.delete(self.bboxIdList[idx])
        # self.bboxIdList.pop(idx)
        vals = self.bboxList.pop(idx)
        self.listbox.delete(idx)
        ca = self.var.get()
        self.bboxList.insert(idx, (vals[0], vals[1], vals[2], vals[3], self.radioName[ca-1]))        
        # self.bboxList.append((x1, y1, x2, y2, ca))
        # self.bboxIdList.append(self.bboxId)
        # self.bboxId = None
        self.listbox.insert(idx, '(%d, %d) -> (%d, %d):%s' %(vals[0], vals[1], vals[2], vals[3], self.radioName[ca-1]))
        self.listbox.itemconfig(idx, fg = COLORS[(idx) % len(COLORS)])

    def selRadio(self):
        selection = "你选择了类别： "+self.radioName[self.var.get()-1]
        self.radioLabel.config(text = selection)

    def loadDir(self, dbg = False):
        '''
        if not dbg:
            s = self.entry.get()
            self.parent.focus()
            self.category = int(s)
        else:
            s = r'D:\workspace\python\labelGUI'
       	'''
##        if not os.path.isdir(s):
##            tkMessageBox.showerror("Error!", message = "The specified dir doesn't exist!")
##            return
        self.category = self.entry.get()
        self.parent.focus()
        # judge whether there has input
        if self.category == None or self.category == "":
            print 'No input'
            return
        # get image list
        imageDir = self.category #os.path.join(r'./Images', self.category)
        print imageDir
        # find all file names and directory names in this directory
        self.imageList = glob.glob(os.path.join(imageDir, '*'))
        # remove directories and files that do not conform to the suffix format
        imglist = range(len(self.imageList))
        imglist.reverse()		
        for i in imglist:
            if os.path.isdir(self.imageList[i]):
                self.imageList.pop(i)
                continue
            if not os.path.splitext(self.imageList[i])[1] in Image_FORMAT:
                self.imageList.pop(i)
        #self.imageList = glob.glob(os.path.join(self.imageDir, '*'))
        if len(self.imageList) == 0:
            print 'No images found in the specified dir!'
            tkMessageBox.showinfo("", "此文件夹中没有图片")
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

         # set up output dir
        self.outDir = self.category #os.path.join(r'./Labels', self.category)
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
		
        """
        # load example bboxes
        # self.egDir = os.path.join(r'./Examples', '%03d' %(self.category))
        # if not os.path.exists(self.egDir):
        #     return
        # filelist = glob.glob(os.path.join(self.egDir, '*.JPEG'))
        # self.tmp = []
        # self.egList = []
        # random.shuffle(filelist)
        # for (i, f) in enumerate(filelist):
        #    if i == 3:
        #        break
        #    im = Image.open(f)
        #    r = min(SIZE[0] / im.size[0], SIZE[1] / im.size[1])
        #    new_size = int(r * im.size[0]), int(r * im.size[1])
        #    self.tmp.append(im.resize(new_size, Image.ANTIALIAS))
        #    self.egList.append(ImageTk.PhotoImage(self.tmp[-1]))
        #    self.egLabels[i].config(image = self.egList[-1], width = SIZE[0], height = SIZE[1])
		"""
        boxes = []
        self.loadImage(boxes)
        print '%d images loaded from %s' %(self.total, self.category)

    def loadImage(self, boxes):
        # load image
        self.scaleRate = 1.0
        widthRate = 0.0
        heightRate = 0.0
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        print "img.size :",self.img.size
        print "img.format :",self.img.format
        self.img_width, self.img_height = self.img.size
        if self.img_width > IMAGESIZE:
            widthRate = self.img_width*1.0 / IMAGESIZE
        if self.img_height > IMAGESIZE:
            heightRate = self.img_height*1.0 / IMAGESIZE
        self.scaleRate = max(widthRate, heightRate, 1.0)
        print "scaleRate :",self.scaleRate
        if self.scaleRate != 1.0:
            self.img.thumbnail((int(self.img_width / self.scaleRate), int(self.img_height / self.scaleRate)))
        self.tkimg = ImageTk.PhotoImage(self.img)
        #self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        #self.mainPanel.config(width = 400, height = 400)	        
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

        # load labels
        self.clearAll = True
        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        bbox_cnt = 0
        if len(boxes)!=0:
            for i in range(len(boxes)):
                self.bboxList.append(boxes[i])
                tmp0 = int(boxes[i][0])
                tmp1 = int(boxes[i][1])
                tmp2 = int(boxes[i][2])
                tmp3 = int(boxes[i][3])
                tmp4 = boxes[i][4]
                tmpId = self.mainPanel.create_rectangle(int(float(tmp0)/self.scaleRate), int(float(tmp1)/self.scaleRate), \
                                                            int(float(tmp2)/self.scaleRate), int(float(tmp3)/self.scaleRate), \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                self.bboxIdList.append(tmpId)
                self.listbox.insert(END, '(%d, %d) -> (%d, %d):%s' %(tmp0, tmp1, tmp2, tmp3, tmp4))
                self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        bbox_cnt = int((line.split())[0].strip())
                        print "bbox_cnt :",bbox_cnt
                        continue
                        '''
                        lis = line.split(' ')
                        if len(lis) == 1:
                            bbox_cnt = int(lis[0].strip())
                        else:
                            bbox_cnt = int(lis[0].strip())
                            self.var.set(int(lis[1].strip()))
                        '''
                    tmp = [t.strip() for t in line.split()]
                    tmp[0] = int(tmp[0])
                    tmp[1] = int(tmp[1])
                    tmp[2] = int(tmp[2])
                    tmp[3] = int(tmp[3])					
                    # print tmp
                    self.bboxList.append(tuple(tmp))
                    tmpId = self.mainPanel.create_rectangle(int(float(tmp[0])/self.scaleRate), int(float(tmp[1])/self.scaleRate), \
                                                            int(float(tmp[2])/self.scaleRate), int(float(tmp[3])/self.scaleRate), \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '(%d, %d) -> (%d, %d):%s' %(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4]))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
    

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            #if self.var.get() == None:
            f.write('%d\n' %len(self.bboxList))
            #else:
            #    f.write("%d %d\n"%(len(self.bboxList),self.var.get()))
            for bbox in self.bboxList:
                f.write(' '.join(map(str, bbox)) + '\n')
        print 'Image No. %d saved' %(self.cur)

    def lengthRange(self, x, y):
        if x > y:
            return True
        return False

    def mouseClick(self, event):
        if self.tkimg:
            if self.STATE['click'] == 0:
            	if event.x > self.tkimg.width() or event.y > self.tkimg.height():
            		return
                self.STATE['x'], self.STATE['y'] = event.x, event.y
            else:
                if self.tkimg.width() >= event.x and self.tkimg.height() >= event.y:
                    if self.STATE['x'] == event.x and self.STATE['y'] == event.y:
                        print "two clicks in the same location"
                        return
                    x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
                    y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
                    x1 = int(x1 * max(self.scaleRate, 1.0))
                    x2 = int(x2 * max(self.scaleRate, 1.0))
                    y1 = int(y1 * max(self.scaleRate, 1.0))
                    y2 = int(y2 * max(self.scaleRate, 1.0))
                    if self.lengthRange(x1, self.img_width):
                    	x1 = self.tkimg.width()
                    	x2 = self.tkimg.width()
                    if self.lengthRange(x2, self.img_width):
                    	x2 = self.tkimg.width()
                    if self.lengthRange(y1, self.img_height):
                    	y1 = self.tkimg.height()
                    	y2 = self.tkimg.height()
                    if self.lengthRange(y2, self.img_height):
                    	y2 = self.tkimg.height()
                    ca = self.var.get()
                    self.bboxList.append((x1, y1, x2, y2, self.radioName[ca-1]))
                    self.bboxIdList.append(self.bboxId)
                    self.bboxId = None
                    self.listbox.insert(END, '(%d, %d) -> (%d, %d):%s' %(x1, y1, x2, y2, self.radioName[ca-1]))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
            self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        if self.tkimg:
            if self.tkimg:
                if self.hl:
                    self.mainPanel.delete(self.hl)
                    self.hl = None
                if self.vl:
                    self.mainPanel.delete(self.vl)
                    self.vl = None
                if self.tkimg.height() >= event.y and self.tkimg.width() >= event.x:
                    self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
                    self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
                    self.disp.config(text = '鼠标位置　x: %d, y: %d' %(int(event.x * max(self.scaleRate, 1.0)), int(event.y * max(self.scaleRate, 1.0))))
            if 1 == self.STATE['click']:
                if self.bboxId:
                    self.mainPanel.delete(self.bboxId)
                if self.tkimg.height() >= event.y and self.tkimg.width() >= event.x:
                    self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                                  event.x, event.y, \
                                                                  width = 2, \
                                                                  outline = COLORS[len(self.bboxList) % len(COLORS)])


    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        print "sel :",sel
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBBox(self):
        if self.clearAll == False:
            resu = tkMessageBox.askyesno("警告", "您将删除所有画框")
            print "clearAll :",resu
            if resu == False:
				return
        self.clearAll = False
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur == 1:
            tkMessageBox.showinfo("", "当前已是第一张图片")
        if self.cur > 1:
            self.cur -= 1
            boxes = []
            self.loadImage(boxes)

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur == self.total:
            tkMessageBox.showinfo("", "当前已是最后一张图片")
        if self.cur < self.total:
            self.cur += 1
            boxes = []
            self.loadImage(boxes)

    def nextcpImage(self, event = None):
        self.saveImage()
        if self.cur == self.total:
            tkMessageBox.showinfo("", "当前已是最后一张图片")
        if self.cur < self.total:
            self.cur += 1
            boxes = self.bboxList
            self.loadImage(boxes)        
            

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            boxes = []
            self.loadImage(boxes)

##    def setImage(self, imagepath = r'test2.png'):
##        self.img = Image.open(imagepath)
##        self.tkimg = ImageTk.PhotoImage(self.img)
##        self.mainPanel.config(width = self.tkimg.width())
##        self.mainPanel.config(height = self.tkimg.height())
##        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.mainloop()
