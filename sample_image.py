import cv2
import os

# 定义视频文件路径和保存帧的文件夹
video_path = 'fly.mp4'  # 替换为你的视频文件路径
output_folder = 'frames'

# 创建保存帧的文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 打开视频文件
cap = cv2.VideoCapture(video_path)

frame_count = 0

# 循环遍历视频的每一帧
while cap.isOpened():
    ret, frame = cap.read()  # 读取帧
    if not ret:
        break

    # 保存帧为JPG文件
    frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(frame_filename, frame)

    frame_count += 1

# 释放视频对象
cap.release()

print(f"视频的所有帧已保存到 '{output_folder}' 文件夹中。")