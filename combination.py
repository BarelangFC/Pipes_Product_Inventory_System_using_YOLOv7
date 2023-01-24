from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
import sys
from datetime import datetime
import csv
import darknet_images
import darknet
import cv2


class buka_ui(QMainWindow):    
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi('ui/riset.ui',self)        
        self.start_button.clicked.connect(self.start_button_clicked)
        self.browse_button.clicked.connect(self.browse_button_clicked)
        self.export_button.clicked.connect(self.export_button_clicked)
        self.reset_button.clicked.connect(self.reset_button_clicked)       
        self.imagePath = ''   
        self.imagePath_baru = ''
        self.counter = ''
        self.textBrowser_5.append("Click Browse Image First")


# start button
    def start_button_clicked(self):
        print('start button clicked')
        args = darknet_images.parser()
        darknet_images.check_arguments_errors(args)
        darknet_images.random.seed(4)  # deterministic bbox colors            
        darknet_images.network, class_names, class_colors = darknet.load_network(
            args.config_file,
            args.data_file,
            args.weights,
            batch_size=args.batch_size
        )            
        images = darknet_images.load_images(args.input)
        # print(images)
        index = 0       
        while True:
            index+=1
            if args.input:
                if index >= len(images):
                    break
                darknet_images.image_name = images[index]
            else:
                darknet_images.image_name = self.imagePath
            break
                   
        image, detections = darknet_images.image_detection(darknet_images.image_name, darknet_images.network, class_names, class_colors, args.thresh)
        # if args.save_labels:
        #     darknet_images.save_annotations(image_name, image, detections, class_names)
        # print("Count: ", len(detections))
        self.counter = len(detections)
        # if not args.dont_show:
        #     darknet_images.cv2.imshow('Pipes Product Inventory System Using YOLOv7', image)            
        #     if darknet_images.cv2.waitKey() & 0xFF == ord('q'):
        #         break
        
        filename = 'saved_data.jpeg'
        cv2.imwrite(filename, image)
        self.imagePath = filename
        pixmap = QPixmap()
        pixmap.load(self.imagePath)
        pixmap_resized = pixmap.scaled(685,475,QtCore.Qt.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap_resized)
        scene = QtWidgets.QGraphicsScene()
        self.textBrowser_5.clear()
        self.textBrowser_5.append("Detection & Counting Result. Click Export Button to Save Result")
        scene.addItem(item)
        self.graphicsView.setScene(scene)
        
        # print("image path:", self.imagePath)
        now = datetime.now()   
        d1_string = now.strftime("%d-%m-%Y") #date output
        t1_string = now.strftime("%H:%M:%S") #time output
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser_4.clear()  
        self.textBrowser_2.append("{}".format(d1_string))       #date
        self.textBrowser_4.append("{}".format(t1_string))       #time
        self.textBrowser_3.append("{}". format(self.counter))   #total pipes
        self.update()


# browse button
    def browse_button_clicked(self):    
        print('browse button clicked')
        self.textBrowser_5.clear() 
        self.textBrowser_5.append("Selecting Image")                  
        image = QFileDialog.getOpenFileName(None, 'Open File', '',"Image file(*.jpg , *.jpeg,  *.png,  *.jpeg,)")
        self.imagePath = image[0]        
        pixmap = QPixmap()
        pixmap.load(self.imagePath)
        pixmap_resized = pixmap.scaled(685,475,QtCore.Qt.KeepAspectRatio)
        item = QtWidgets.QGraphicsPixmapItem(pixmap_resized)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        self.graphicsView.setScene(scene)
        self.textBrowser_5.clear()
        self.textBrowser_5.append("Click Start Button To Detect")
        self.imagePath_baru = self.imagePath.split("/")
        a = self.imagePath_baru[5]
        # print("image path:", self.imagePath_baru)
        self.textBrowser.clear()
        self.textBrowser.append("{}".format(a))    #file name image path        

# export button
    def export_button_clicked(self):
        now = datetime.now()
        d_string = now.strftime("%d-%m-%Y") #date output
        t_string = now.strftime("%H:%M:%S") #time output
        print('export button clicked')
        with open('Inventory Report.csv', mode='a') as f:
            keys = ['Date', 'Time', 'File Name', 'Counter']
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writerow({'Date': d_string, 'Time': t_string, 'File Name': self.imagePath_baru[5], 'Counter': self.counter})
        self.textBrowser_5.clear()       
        self.textBrowser_5.append("Data Successfully Exported. Click Browse Image Again to Detect New Image")


# clear button  
    def reset_button_clicked(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser_4.clear()
        self.textBrowser_5.clear()      


# main program
def run():   
    app = QApplication(sys.argv)    
    widget = buka_ui()    
    widget.show()    
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    run()