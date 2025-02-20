import cv2
import numpy as np

# グローバル変数
points_image1 = []
points_image2 = []
current_image = 1  # 現在の画像（1または2）
marker_color = (0, 0, 255)  # 初期マーカー色は赤

# マウスクリックイベントのコールバック関数
def select_points(event, x, y, flags, param):
    global points_image1, points_image2, current_image

    if event == cv2.EVENT_LBUTTONDOWN:
        if current_image == 1 and len(points_image1) < 2:
            points_image1.append((x, y))
            print(f"Point selected in Image 1: ({x}, {y})")
        elif current_image == 2 and len(points_image2) < 2:
            points_image2.append((x, y))
            print(f"Point selected in Image 2: ({x}, {y})")

# 距離を計算する関数
def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def main():
    global points_image1, points_image2, current_image, marker_color

    # 画像の読み込み
    image1 = cv2.imread("image1.png")
    image2 = cv2.imread("image2.png")

    if image1 is None or image2 is None:
        print("Error: Could not load images. Make sure 'image1.jpg' and 'image2.jpg' are in the same directory.")
        return

    # **1回目の点選択**
    print("Select two points on Image 1. Press Enter to confirm after selecting.")
    cv2.namedWindow("Image 1")
    cv2.setMouseCallback("Image 1", select_points)
    while True:
        temp_image1 = image1.copy()
        for point in points_image1:
            cv2.circle(temp_image1, point, 5, marker_color, -1)
        cv2.imshow("Image 1", temp_image1)

        key = cv2.waitKey(1)
        if key == 13 and len(points_image1) == 2:  # Enterキー
            print("Select two points on Image 2. Press Enter to confirm after selecting.")
            break

    current_image = 2
    cv2.namedWindow("Image 2")
    cv2.setMouseCallback("Image 2", select_points)
    while True:
        temp_image2 = image2.copy()
        for point in points_image2:
            cv2.circle(temp_image2, point, 5, marker_color, -1)
        cv2.imshow("Image 2", temp_image2)

        key = cv2.waitKey(1)
        if key == 13 and len(points_image2) == 2:  # Enterキー
            break
            
    cv2.destroyAllWindows()

    # 1回目の距離と比率の計算
    if len(points_image1) == 2 and len(points_image2) == 2:
        distance1 = calculate_distance(points_image1[0], points_image1[1])
        distance2 = calculate_distance(points_image2[0], points_image2[1])
        ratio = distance2 / distance1
        print(f"Distance in Image 1: {distance1}")
        print(f"Distance in Image 2: {distance2}")
        print(f"Ratio: {ratio}")
    else:
        print("Insufficient points selected in the first step.")
        return
        
    real_distance = float(input("Enter the real distance between the points in Image 2 (in meters or other unit): "))
    pixel = real_distance/distance2
    print(f"m/Pixel in Image 2: {pixel} m")
    
    


    # **2回目の点選択**
    points_image1 = []  # リセット
    points_image2 = []  # リセット
    marker_color = (255, 0, 0)  # 2回目は青マーカーに変更

    # Image 1で2点選択
    current_image = 1
    print("Select two points on Image 1. Press Enter to confirm after selecting.")
    cv2.namedWindow("Image 1")
    cv2.setMouseCallback("Image 1", select_points)
    while True:
        temp_image1 = image1.copy()
        for point in points_image1:
            cv2.circle(temp_image1, point, 5, marker_color, -1)
        cv2.imshow("Image 1", temp_image1)

        key = cv2.waitKey(1)
        if key == 13 and len(points_image1) == 2:  # Enterキー
            print("Select two points on Image 2. Press Enter to confirm after selecting.")
            break

    # Image 2で2点選択
    current_image = 2
    cv2.namedWindow("Image 2")
    cv2.setMouseCallback("Image 2", select_points)
    while True:
        temp_image2 = image2.copy()
        for point in points_image2:
            cv2.circle(temp_image2, point, 5, marker_color, -1)
        cv2.imshow("Image 2", temp_image2)

        key = cv2.waitKey(1)
        if key == 13 and len(points_image2) == 2:  # Enterキー
            break
            
    # 2点間の座標差を求める
    if len(points_image1) == 2 and len(points_image2) == 2:
        # Image 1の2点間の差
        diff_image1 = (points_image1[1][0] - points_image1[0][0], points_image1[1][1] - points_image1[0][1])
        # Image 2の2点間の差
        diff_image2 = (points_image2[1][0] - points_image2[0][0], points_image2[1][1] - points_image2[0][1])

        # スケーリング
        scaled_diff_image1_x = diff_image1[0] * ratio
        scaled_diff_image1_y = diff_image1[1] * ratio
        scaled_diff_x = scaled_diff_image1_x - diff_image2[0]
        scaled_diff_y = scaled_diff_image1_y - diff_image2[1]
        real_x = scaled_diff_x * pixel
        real_y = scaled_diff_y * pixel

        print(f"Select point in Image 1: {points_image1}")
        print(f"Select point in Image 2: {points_image2}")
        print(f"Scaled difference based on ratio: ({scaled_diff_x},{scaled_diff_y})")
        print(f"Scaled real difference: ({real_x} m,{real_y} m)")
    else:
        print("Insufficient points selected in the second step.")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
