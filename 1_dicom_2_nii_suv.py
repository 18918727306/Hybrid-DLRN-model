"""
将CT DICOM (.ima)&PET（.ima） 转换为 NIfTI 格式并保存
对PET图像应用标准化取值单位（SUV）转换

"""
import pathlib as plb
import tempfile
import os
import dicom2nifti
import nibabel as nib
import numpy as np
import pydicom
import shutil
# import nilearn.image
from tqdm import tqdm
import dicom2nifti.settings as settings

settings.disable_validate_slice_increment()


def find_patient_folders(root_path):
    root = plb.Path(root_path)
    #patient_dirs = list(root.glob('N*'))  # 查找以D开头的文件夹
    #patient_dirs = list(root.glob('[0-9]*'))  # 查找以数字开头的文件夹
    patient_dirs = list(root.glob('1-N1'))
    return patient_dirs

def calculate_suv_factor(dcm_path):
    ds = pydicom.dcmread(str(dcm_path))
    # ds = pydicom.read_file(str(dcm_path))
    total_dose = ds.RadiopharmaceuticalInformationSequence[0].RadionuclideTotalDose
    start_time = ds.RadiopharmaceuticalInformationSequence[0].RadiopharmaceuticalStartTime
    half_life = ds.RadiopharmaceuticalInformationSequence[0].RadionuclideHalfLife
    acq_time = ds.AcquisitionTime
    weight = ds.PatientWeight
    time_diff = conv_time(acq_time) - conv_time(start_time)
    act_dose = total_dose * 0.5 ** (time_diff / half_life)
    suv_factor = 1000 * weight / act_dose
    return suv_factor


def conv_time(time_str):
    # 转换 DICOM 时间字符串
    return (float(time_str[:2]) * 3600 + float(time_str[2:4]) * 60 + float(time_str[4:13]))


def convert_pet(pet, suv_factor):
    # 将PET图像数据转换为SUV
    affine = pet.affine
    pet_data = pet.get_fdata()
    pet_suv_data = (pet_data * suv_factor).astype(np.float32)
    pet_suv = nib.Nifti1Image(pet_suv_data, affine)
    return pet_suv


def dcm2nii_CT(CT_dcm_path, nii_out_path):
    # 将CT DICOM (.ima) 转换为 NIfTI 格式并保存
    with tempfile.TemporaryDirectory() as tmp:
        tmp = plb.Path(str(tmp))
        dicom2nifti.convert_directory(CT_dcm_path, str(tmp), compression=True, reorient=True)
        nii = next(tmp.glob('*nii.gz'))
        shutil.copy(nii, nii_out_path / 'CT.nii.gz')


def dcm2nii_PET(PET_dcm_path, nii_out_path):
    # 将PET DICOM 转换为 NIfTI，并应用SUV转换
    # first_pt_dcm = next(PET_dcm_path.glob('*.IMA'))
    # first_pt_dcm = next(PET_dcm_path.glob('*.dcm'))
    # first_pt_dcm =next(PET_dcm_path.glob('*.DCM'), next(PET_dcm_path.glob('*.dcm'), None))
    first_pt_dcm =next(PET_dcm_path.glob('*.DCM'), next(PET_dcm_path.glob('*.dcm'), next(PET_dcm_path.glob('*.IMA'),None)))
    
    suv_corr_factor = calculate_suv_factor(first_pt_dcm)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = plb.Path(str(tmp))
        dicom2nifti.convert_directory(PET_dcm_path, str(tmp), compression=True, reorient=True)

        nii = next(tmp.glob('*nii.gz'))
        shutil.copy(nii, nii_out_path / 'PET.nii.gz')

        suv_pet_nii = convert_pet(nib.load(nii_out_path / 'PET.nii.gz'), suv_factor=suv_corr_factor)
        nib.save(suv_pet_nii, nii_out_path / 'SUV.nii.gz')


def process_patient_folders(root_path):
    patient_dirs = find_patient_folders(root_path)

    for patient_dir in tqdm(patient_dirs):
        try:
            # ct_dir = patient_dir / 'CT'
            ct_dir = patient_dir / 'CT'
            # pet_dir = patient_dir / 'PET'
            pet_dir = patient_dir / 'PET'

            # 检查是否已存在 CT.nii.gz、PET.nii.gz 和 SUV.nii.gz 文件，如果存在则跳过当前病人文件夹
            if (ct_dir / 'CT.nii.gz').exists() and (pet_dir / 'PET.nii.gz').exists() and (
                    pet_dir / 'SUV.nii.gz').exists():
                print(f"跳过 {patient_dir}，因为已存在 CT.nii.gz、PET.nii.gz 和 SUV.nii.gz 文件")
                continue

            # 检查CT和PET目录是否存在
            if not ct_dir.exists() or not pet_dir.exists():
                print(f"CT 或 PET 文件夹在 {patient_dir} 中未找到")
                continue

            # 处理 CT 图像
            try:
                dcm2nii_CT(ct_dir, patient_dir)
            except Exception as e:
                print(f"处理 CT 图像时出错: {patient_dir}, 错误信息: {e}")
                continue  # 跳过此患者，处理下一个

            # 处理 PET 图像并进行 SUV 转换
            try:
                dcm2nii_PET(pet_dir, patient_dir)
            except Exception as e:
                print(f"处理 PET 图像时出错: {patient_dir}, 错误信息: {e}")
                continue  # 跳过此患者，处理下一个

        except Exception as e:
            print(f"处理患者文件夹时出错: {patient_dir}, 错误信息: {e}")
            continue  # 跳过此患者，处理下一个


if __name__ == "__main__":
    # 更新根路径为您的数据路径
    root_path = ''
    process_patient_folders(root_path)
