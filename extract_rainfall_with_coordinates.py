import cv2
import numpy as np
import pandas as pd

def convert_pixel_to_coordinates(pixel_x, pixel_y, ref_points):
    ref_a, ref_b = ref_points

    delta_x = (ref_b['lat'] - ref_a['lat']) / (ref_b['pixel_x'] - ref_a['pixel_x'])
    delta_y = (ref_b['lon'] - ref_a['lon']) / (ref_b['pixel_y'] - ref_a['pixel_y'])

    lat = ref_a['lat'] + (pixel_x - ref_a['pixel_x']) * delta_x
    lon = ref_a['lon'] + (pixel_y - ref_a['pixel_y']) * delta_y

    return lat, lon

def process_image(image_path, ref_points, legend_width, color_ranges):
    img = cv2.imread(image_path)

    # 裁剪图像并忽略图例区域
    img = img[:, legend_width:]

    # 提取在设定颜色范围内的像素
    masks = []
    for lower, upper in color_ranges:
        mask = cv2.inRange(img, lower, upper)
        masks.append(mask)
        print(mask)
    binary_img = cv2.bitwise_or(*masks)

    # 查找图像中的轮廓
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 提取降水量信息以及经度和纬度
    rainfall_data = []
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)

        if M["m00"] != 0:
            pixel_x = int(M["m10"] / M["m00"])
            pixel_y = int(M["m01"] / M["m00"])
            lat, lon = convert_pixel_to_coordinates(pixel_x, pixel_y, ref_points)

            rainfall_data.append({
                'id': i + 1,
                'area': area,
                'latitude': lat,
                'longitude': lon
            })

    return rainfall_data, contours, img


def save_data_to_csv(data, output_path):
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

def create_debug_image(input_img, contours, output_path):
    img_copy = input_img.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # 绘制轮廓
    cv2.drawContours(img_copy, contours, -1, (255, 0, 0), 2)

    for i, cnt in enumerate(contours):
        # 计算轮廓的质心并添加ID标签
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            pixel_x = int(M["m10"] / M["m00"])
            pixel_y = int(M["m01"] / M["m00"])
            cv2.putText(img_copy, str(i + 1), (pixel_x, pixel_y), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    # 保存调试图片
    cv2.imwrite(output_path, img_copy)


# 示例
image_path = 'radar_image.png'
csv_output_path = 'rainfall_data_with_coordinates.csv'
debug_image_output_path = 'debug_rainfall_image.png'

ref_points = [
    {'pixel_x': 0, 'pixel_y': 0, 'lat': 14.981259928342144, 'lon': 99.52284727468773},
    {'pixel_x': 965, 'pixel_y': 800, 'lat': 12.728301173259432, 'lon': 102.2016701846946}
]
legend_width = 73

# 定义颜色范围
color_ranges = [
    (np.array([  0, 215,   0], dtype=np.uint8), np.array([  0, 216,   0], dtype=np.uint8)),  # #00d800
    (np.array([ 85, 215,   0], dtype=np.uint8), np.array([ 85, 216,   0], dtype=np.uint8)),  # #00d855
    (np.array([  0, 252,   0], dtype=np.uint8), np.array([  0, 255,   0], dtype=np.uint8)),  # #00fc00
    (np.array([  1, 180,   0], dtype=np.uint8), np.array([  1, 180,   0], dtype=np.uint8))  # #00b401
    # (np.array([  2, 209,   4], dtype=np.uint8), np.array([  2, 209,   4], dtype=np.uint8))   # #04d102
]

rainfall_data, contours, original_img = process_image(image_path, ref_points, legend_width, color_ranges)
save_data_to_csv(rainfall_data, csv_output_path)
create_debug_image(original_img, contours, debug_image_output_path)