"""
遍历指定的根文件夹，寻找每个病人的 ROI 文件（R1.uint16.nii.gz），完成翻转操作后，保存到与原文件同级的位置，命名为 flip_label_NEW.nii.gz。
"""
import os
import SimpleITK as sitk

# 指定根文件夹路径

root_folder = r""

# 遍历根文件夹下的所有子文件夹
for subdir, dirs, files in os.walk(root_folder):
    # 遍历当前子文件夹中的所有文件
    for file in files:
        # 检查文件是否为 "R1.uint16.nii.gz"
        if file == "R1-1-1.uint16.nii.gz":
            # 构建完整的文件路径
            image_path = os.path.join(subdir, file)
            try:
                # 读取图像
                image = sitk.ReadImage(image_path)
                print(f"Original image type: {image.GetPixelIDTypeAsString()}")
                
                # 前后左右的翻转操作, [x, y, z], 翻转 y 轴
                flipped_image = sitk.Flip(image, [False, True, False])
                
                # 确保翻转后的图像数据类型为 int16
                flipped_image = sitk.Cast(flipped_image, sitk.sitkUInt16)
                print(f"Flipped image type: {flipped_image.GetPixelIDTypeAsString()}")
                
                # 构建输出路径，命名为 flip_label_NEW.nii.gz
                output_path = os.path.join(subdir, "flip_label_NEW.nii.gz")
                
                # 保存翻转后的图像
                sitk.WriteImage(flipped_image, output_path)
                print(f"Processed {image_path}, saved flipped image to {output_path}")
            except Exception as e:
                print(f"Error processing {image_path}: {e}")

print("Task completed.")
