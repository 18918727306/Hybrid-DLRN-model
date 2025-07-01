import os
import nibabel as nib
import numpy as np

# 指定总文件夹路径

main_folder = '

# 遍历每个病人文件夹
for patient_folder in os.listdir(main_folder):
    patient_path = os.path.join(main_folder, patient_folder)

    # 检查是否是文件夹
    if os.path.isdir(patient_path):
        # 寻找patch文件夹
        # patch_path = os.path.join(patient_path, 'patch')

        # 检查patch文件夹是否存在
        # if os.path.exists(patch_path) and os.path.isdir(patch_path):
            # 寻找Bones文件夹
        # bones_path = os.path.join(patient_path, 'liver')
        #
        # # 检查Bones文件夹是否存在
        # if os.path.exists(bones_path) and os.path.isdir(bones_path):
        #     # 在Bones文件夹的同一级创建BonesBinarized文件夹
        #     bones_binarized_path = os.path.join(patch_path, 'BonesBinarized')
        #     os.makedirs(bones_binarized_path, exist_ok=True)

        # 遍历Bones文件夹内的NIfTI文件
        for filename in os.listdir(patient_path):
            # if filename.endswith('Bones.nii.gz'):
            if os.path.basename(filename) == '112_Bones.nii.gz':
                file_path = os.path.join(patient_path, filename)

                # 加载NIfTI文件
                nifti_img = nib.load(file_path)
                nifti_data = nifti_img.get_fdata()

                # 进行二值化处理
                threshold = 0  # 设置二值化阈值为0，非黑色部分变为白色
                binary_data = np.where(nifti_data > threshold, 1, 0)

                # 创建新的NIfTI图像
                binary_img = nib.Nifti1Image(binary_data, nifti_img.affine, nifti_img.header)

                # 保存二值化后的NIfTI文件到BonesBinarized文件夹
                save_path = os.path.join(patient_path, f'112_Bones_binarized.nii.gz')
                nib.save(binary_img, save_path)

        # 提示当前病人的处理已完成
        print(f"Processing for patient '{patient_folder}' is completed.")
