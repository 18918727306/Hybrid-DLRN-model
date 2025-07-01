"""
根据112_CT_resampled.nii.gz重采样flip_label_NEW.nii.gz图像
生成：112_flip_label_resampled_2_CT.nii.gz
"""

import os
import nibabel as nib
import SimpleITK as sitk


def resample_pet_to_ct(ct_image_path, pet_image_path, output_path):
    # 读取CT图像
    ct_image = sitk.ReadImage(ct_image_path)
    ct_size = ct_image.GetSize()
    ct_spacing = ct_image.GetSpacing()
    ct_direction = ct_image.GetDirection()
    ct_origin = ct_image.GetOrigin()

    # 读取PET图像
    pet_image = sitk.ReadImage(pet_image_path)
    pet_resampler = sitk.ResampleImageFilter()

    pet_resampler.SetReferenceImage(ct_image)
    pet_resampler.SetSize(ct_size)
    pet_resampler.SetOutputSpacing(ct_spacing)
    pet_resampler.SetOutputDirection(ct_direction)
    pet_resampler.SetOutputOrigin(ct_origin)
    pet_resampler.SetInterpolator(sitk.sitkLinear)

    # 重采样PET图像
    resampled_pet = pet_resampler.Execute(pet_image)

    # 保存重采样后的PET图像
    sitk.WriteImage(resampled_pet, output_path)


def main():

    root_dir = ''
    for patient_dir in os.listdir(root_dir):
        patient_path = os.path.join(root_dir, patient_dir)
        if os.path.isdir(patient_path):
            ct_path = os.path.join(patient_path, '112_CT_resampled.nii.gz')
            #pet_path = os.path.join(patient_path, 'SUV.nii.gz')
            #output_pet_path = os.path.join(patient_path, '112_SUV_resampled.nii.gz')
            pet_path = os.path.join(patient_path, 'flip_label_NEW.nii.gz')
            output_pet_path = os.path.join(patient_path, '112_flip_label_resampled_2_CT.nii.gz')
            # pet_path = os.path.join(patient_path, 'R1_Abs_thres2.5to50.0.uint16.nii.gz')
            # output_pet_path = os.path.join(patient_path, '112_lifex2.5_label_resampled.nii.gz')
            if os.path.exists(ct_path) and os.path.exists(pet_path):
                print(f"Processing {patient_dir}...")
                resample_pet_to_ct(ct_path, pet_path, output_pet_path)
            else:
                if not os.path.exists(ct_path):
                    print(f"CT image not found for {patient_dir}")
                if not os.path.exists(pet_path):
                    print(f"PET image not found for {patient_dir}")


if __name__ == "__main__":
    main()
