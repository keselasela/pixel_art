import numpy as np
import math
import cv2
from PIL import Image, ImageDraw

def make_mosaic_art(source_directory= "",
                    dot_size = 10, 
                    interval = 1,
                    K = 8):

    target_image = Image.open(source_directory + "target.jpg")
    target_image = target_image.resize(math.floor(i/10)*10 for i in target_image.size)
    tile_num = tuple(math.floor(i/10) for i in  target_image.size)
    tile_list = make_tile_list(target_image, tile_num)
    #オブジェクト検出（輪郭）--------------------------------
    # グレースケール形式に変換する。
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 大津の手法で2値化する。
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    plt.imshow(binary, cmap=plt.cm.gray)
    plt.show()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3));
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    plt.imshow(opening, cmap=plt.cm.gray)
    plt.show()
    ret, contours, hierarchy = cv2.findContours(
    opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    drawn = cv2.drawContours(src.copy(), contours, -1, (0, 255, 0), 2)

    plt.imshow(cv2.cvtColor(drawn, cv2.COLOR_BGR2RGB))
    plt.show()
    #--------------------------------------------------------
    # get binary image and apply Gaussian blur
    coins = cv2.imread('target.jpg')
    coins_gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY)
    coins_preprocessed = cv2.GaussianBlur(coins_gray, (5, 5), 0)
    
    # get binary image
    _, coins_binary = cv2.threshold(coins_preprocessed, 130, 255, cv2.THRESH_BINARY)
    
    # invert image to get coins
    coins_binary = cv2.bitwise_not(coins_binary)
    #-----------------------------------------------------------------------------

def draw_pixel(clustered_color_list, tile_list, image_size):
    image = Image.new('RGB', image_size, (0,0,0))
    draw = ImageDraw.Draw(image)
    for i, j in zip(tile_list,clustered_color_list):
        draw.rectangle(i, fill=tuple(j), outline=(0,0,0))
    image.save('pixeled_target.jpg', quality=95)

def make_tile_color_list(tile_list, image):
    '''
    targetを分割し、リスト化したものであるタイルリストを元に
    それぞれのタイルに対応したRGBを格納したリストを返します
    '''
    tile_color_list = []
    for i in tile_list:
        central_color_of_tile = image.getpixel((math.floor((i[2] + i[0]) / 2) , math.floor((i[3] + i[1])/ 2) ))
        tile_color_list.append(central_color_of_tile)
    return tile_color_list

def make_tile_list(target_image, tile_num):
    '''
    targetを分割し、そのリストを返します
    tile_numは分割数であり、第一引数がｘ軸方向、第二引数がｙ軸方向
    '''
    x_tile_num = tile_num[0]
    y_tile_num = tile_num[1]
    x_target_size = target_image.size[0]
    y_target_size = target_image.size[1]
    tile_list = []
    for y in range(0, y_tile_num):
        for x in range(0, x_tile_num):
            tile = (x*x_target_size/x_tile_num, y*y_target_size/y_tile_num,
            (x+1)*x_target_size/x_tile_num, (y+1)*y_target_size/y_tile_num )
            tile = tuple(math.floor(i) for i in tile)
            tile_list.append(tile)
    return tile_list



if __name__ == "__main__":
    print("start")
    make_mosaic_art()

