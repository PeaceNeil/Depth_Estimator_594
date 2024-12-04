import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_depth_map(file_path, rectangle_ratio, threshold, visualize=False):

    depth_map = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    if depth_map is None:
        raise FileNotFoundError(f"Unable to read file: {file_path}")

    h, w = depth_map.shape
    center_x, center_y = w // 2, h // 2

    # Calculate rectangle size based on the ratio
    rect_width = int(w * rectangle_ratio[0])
    rect_height = int(h * rectangle_ratio[1])

    # Calculate the rectangle boundaries
    x1 = max(0, center_x - rect_width // 2)
    y1 = max(0, center_y - rect_height // 2)
    x2 = min(w, center_x + rect_width // 2)
    y2 = min(h, center_y + rect_height // 2)

    roi = depth_map[y1:y2, x1:x2]

    mean_value = np.mean(roi)
    print(f"Mean value of the center rectangle: {mean_value}")

    # Optional visualization
    if visualize:
        depth_map_visual = depth_map.copy()
        # Draw a rectangle on the visualization map
        depth_map_visual = cv2.cvtColor(depth_map_visual, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(depth_map_visual, (x1, y1), (x2, y2), (255, 0, 0), 5)

        # Plot the depth map and the ROI
        plt.figure(figsize=(8, 8))
        plt.title("Depth Map with Center Rectangle")
        plt.imshow(depth_map_visual, cmap="gray")
        plt.axis("off")
        plt.show()

    # Return the result based on the threshold
    return "stop" if mean_value > threshold else "safe"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perception based on depth map")
    parser.add_argument('--image_path', type=str, required=True, help="Path to the input depth image.")
    parser.add_argument('--rectangle_ratio', type=float, nargs=2, default=(0.5, 0.5), 
                        help="Center rectangle ratio as two floats (default: 0.5 0.5).")
    parser.add_argument('--threshold', type=int, default=128, 
                        help="Threshold value for processing (default: 128).")
    parser.add_argument('--visualize', type=str, default='True', 
                        help="Enable or disable visualization (True/False).")

    args = parser.parse_args() # Set to True to enable visualization

    result = process_depth_map(args.image_path, args.rectangle_ratio, args.threshold, visualize=args.visualize)
    print(f"Result: {result}")
