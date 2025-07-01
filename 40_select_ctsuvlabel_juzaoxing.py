"""
从每个病人文件夹中，提取输入网络的ctsuv和label
"""
import os
import shutil

# 定义源文件夹路径和目标文件夹路径
src_dir = ''

dst_labels_dir = ''

# 确保目标文件夹存在
# os.makedirs(dst_images_dir, exist_ok=True)
os.makedirs(dst_labels_dir, exist_ok=True)


# 遍历源文件夹中的所有子文件夹
for patient_folder in os.listdir(src_dir):
    patient_dir = os.path.join(src_dir, patient_folder)  # 病人文件夹的完整路径

    if os.path.isdir(patient_dir):  # 确保它是一个文件夹
        # 定义每个文件的路径

        label_file = os.path.join(patient_dir, '112_ouhe_mask_median.nii.gz')

        # 确保这些文件存在
        # if os.path.exists(ct_file) and os.path.exists(suv_file) and os.path.exists(label_file):
        if os.path.exists(label_file):
            # 使用当前的文件夹名作为病人ID
            patient_id = patient_folder

            # # 重命名并复制 CT 文件
            # new_ct_name = f'MM_{patient_id}_0000.nii.gz'
            # shutil.copy(ct_file, os.path.join(dst_images_dir, new_ct_name))

            # # 重命名并复制 SUV 文件
            # new_suv_name = f'MM_{patient_id}_0001.nii.gz'
            # shutil.copy(suv_file, os.path.join(dst_images_dir, new_suv_name))

            # 重命名并复制 Label 文件
            new_label_name = f'MM_{patient_id}.nii.gz'
            shutil.copy(label_file, os.path.join(dst_labels_dir, new_label_name))
        else:
            print(f'病人 {patient_folder} 的文件缺失，跳过该病人。')
    else:
        print(f'{patient_folder} 不是一个有效的病人文件夹，跳过。')

print("文件提取和重命名完成。")
