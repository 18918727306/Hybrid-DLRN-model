"""
最近邻插值将CT重采样到112_CT_resampled.nii.gz（pet，label也可以降采样）
"""
import os
import SimpleITK as sitk
import re
# 目标路径

base_path = ''
# 遍历以'M'开头的文件夹
for folder_name in os.listdir(base_path):

    #if folder_name.startswith('[0-9]*'):
    #if re.match(r'^\d+-[A-Za-z0-9]+', folder_name):
    # if re.match(r'^\d', folder_name):
    #if re.match(r'^[N*]', folder_name):
    if re.match(r'^[1-N1]', folder_name):
    # if re.match(r'^[D]',folder_name):

        folder_path = os.path.join(base_path, folder_name)

        # 查找CT.nii.gz文件

        ct_file = os.path.join(folder_path, 'CT.nii.gz')
        # ct_file = os.path.join(folder_path, 'SUV.nii.gz')
        # ct_file = os.path.join(folder_path, 'flip_label_NEW.nii.gz')

        if os.path.exists(ct_file):
            # 读取图像
            ct_image = sitk.ReadImage(ct_file)

            # 获取当前的spacing
            original_spacing = ct_image.GetSpacing()
            print(f"Original spacing for {folder_name}: {original_spacing}")

            # 目标spacing
            new_spacing = (1, 1, 2)

            # 计算新的尺寸
            original_size = ct_image.GetSize()
            new_size = [int(round(osz * ospc / nspc)) for osz, ospc, nspc in
                        zip(original_size, original_spacing, new_spacing)]

            # 重新采样图像，使用最近邻插值
            resampler = sitk.ResampleImageFilter()
            resampler.SetOutputSpacing(new_spacing)
            resampler.SetSize(new_size)
            resampler.SetOutputDirection(ct_image.GetDirection())
            resampler.SetOutputOrigin(ct_image.GetOrigin())
            resampler.SetInterpolator(sitk.sitkNearestNeighbor)  # 设置为最近邻插值

            new_ct_image = resampler.Execute(ct_image)

            # 保存重新采样后的图像
            new_ct_file = os.path.join(folder_path, '112_CT_resampled.nii.gz')
            # new_ct_file = os.path.join(folder_path, '112_SUV_resampled.nii.gz')
            # new_ct_file = os.path.join(folder_path, '112_flip_label_resampled.nii.gz')
            sitk.WriteImage(new_ct_image, new_ct_file)

            print(f"Resampled CT saved for {folder_name} at: {new_ct_file}")
