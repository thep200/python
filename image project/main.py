import cv2
import numpy as np
import pytesseract as pyt
from matplotlib import pyplot as plt
pyt.pytesseract.tesseract_cmd = r'C:\Users\Thep Ho\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

root_input_img = 'images/root.png'
ROI_saved_path = 'output/rod.png'

class meter_img:

    def __init__(self):
        img = None
        img_original = None
        img_gray = None
        img_blur = None
        thresh = None
        height = None
        width = None

    def img_load(self, source_img):
        self.img = cv2.imread(source_img)
        self.img_original = self.img.copy()
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.img_blur = cv2.GaussianBlur(self.img_gray, (5, 5), 0)
        self.thresh = cv2.threshold(self.img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        self.height, self.width, _ = self.img.shape


    def find_countours(self, source_img):
        cnts = cv2.findContours(source_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        return cnts


    def extractRegionOfDigits(self):
        self.img_load(root_input_img)

        # trộn các phần đã threshold với nhau để lấy phần lớn nhất.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 1))
        img_merge = cv2.morphologyEx(self.thresh, cv2.MORPH_CLOSE, kernel, iterations=5)

        # Detect cạnh sau khi đã merge sẽ khoanh vùng được phần cần xử lý
        self.img_edge = cv2.Canny(img_merge, 0, 255, 255)
        cnts = self.find_countours(self.img_edge)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # ngưỡng để lấy phần cần xử lý 
        process_area = self.height*self.width*(.75)

        # Extract Roi phần cần xử lý
        for cnt in cnts:      
            if cv2.contourArea(cnt) < process_area:   
                x1, y1, x2, y2 = cv2.boundingRect(cnt)
                ROI = 255 - self.thresh[y1:y1 + y2, x1:x1 + x2]
                break

        cv2.imwrite(ROI_saved_path, ROI)
        return ROI

    def cleanRegionOfDigits(self):
        self.img_load(ROI_saved_path)
        self.thresh = cv2.threshold(self.img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        average_area = 0
        cnts = self.find_countours(self.thresh)

        for c in cnts:
            x, y, width, height = cv2.boundingRect(c)
            average_area += width * height
        average = average_area / len(cnts)

        for c in cnts:
            x, y, width, height = cv2.boundingRect(c)
            area = width * height
            if area > average * 3:
                cv2.drawContours(self.thresh, [c], -1, (0, 0, 0), -1)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        dilate = cv2.dilate(self.thresh, kernel, iterations=3)

        cnts = self.find_countours(dilate)
        for c in cnts:
            area = cv2.contourArea(c)
            if area < average * 2:
                cv2.drawContours(self.thresh, [c], -1, (0, 0, 0), -1)

        result = 255 - self.thresh
        return result


    def read_img(self):
        my_digits = pyt.image_to_string(self.cleanRegionOfDigits())
        print("your digits is:", my_digits)

        file = open('output/digits.txt', 'a')
        file.write(root_input_img + " has digits is :" + my_digits)
        file.close()


def main():
    img = meter_img()
    
    plt.subplot(1, 2, 1)
    plt.imshow(img.extractRegionOfDigits(), cmap='gray')

    plt.subplot(1, 2, 2)
    plt.imshow(img.cleanRegionOfDigits(), cmap='gray')

    img.read_img()

    plt.show()

if __name__ == "__main__":
    main()