import os
import shutil

# 源文件夹路径
source_dir = ''
# source_dir = ''
# 目标文件夹路径
target_dir = ''

# 确保目标文件夹存在
os.makedirs(target_dir, exist_ok=True)

# 遍历源文件夹中的所有子文件夹
for folder_name in os.listdir(source_dir):
    folder_path = os.path.join(source_dir, folder_name)

    # 确保是文件夹
    if os.path.isdir(folder_path):
        suv_file = os.path.join(folder_path, '112_ouhe_mask_median.nii.gz')
        #label
        if os.path.exists(suv_file):
            new_suv_name = f'MM_zheer_jz_{folder_name}.nii.gz'
            shutil.copy(suv_file, os.path.join(target_dir, new_suv_name))

print("文件复制和重命名完成。")
