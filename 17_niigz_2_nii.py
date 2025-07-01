"""
查找文件名：112_Bones.nii
变成112_Bones.nii.gz
"""
import os
import nibabel as nib
import gzip
import shutil


def compress_nii_to_nii_gz(input_path, output_path):
    # Load the .nii file
    img = nib.load(input_path)
    # Save the image as a .nii.gz file
    nib.save(img, output_path)


def main():
    base_dir = r'' # 替换为实际的路径
    
    # base_dir = '/media/liu/686a353e-91ce-4db0-b3e0-36c5ad3ecb17/MM/00_Data_1030/HUAXI_raw/hunhe_miman'
    # 遍历所有名人文件夹
    for celebrity in os.listdir(base_dir):
        celebrity_dir = os.path.join(base_dir, celebrity)

        if os.path.isdir(celebrity_dir):
            # 遍历名人文件夹内的所有病人文件
            for patient_file in os.listdir(celebrity_dir):
                patient_file_path = os.path.join(celebrity_dir, patient_file)
                # patient_file_path = os.path.join(celebrity_dir, patient_file)

                # if patient_file.endswith('Bones.nii'):
                if os.path.basename(patient_file) == '112_Bones.nii':
                    # 定义输出的 .nii.gz 文件路径
                    output_file_path = patient_file_path + '.gz'
                    # 压缩并保存 .nii 为 .nii.gz
                    compress_nii_to_nii_gz(patient_file_path, output_file_path)


if __name__ == '__main__':
    main()
