"""
加载112_liver.nii.gz和112_SUV_resampled.nii.gz，计算liver的SUVmedian


"""
import os
import nibabel as nib
import numpy as np
import pandas as pd


def load_nii(file_path):
    """Load a NIfTI file and return the image data as a numpy array."""
    img = nib.load(file_path)
    data = img.get_fdata()
    return data


def calculate_median_suv(liver_data, suv_data):
    #以liver作为mask，为1的表示肝脏区域，提取liver的SUV，取median
    """Calculate the median SUV value for the voxels where liver_data is 1."""
    suv_values = suv_data[liver_data > 0]
    median_suv = np.median(suv_values)
    return median_suv


def main():

    folder1 = '/'
    folder2 = '/'
    results = []

    for patient_dir in os.listdir(folder1):
        patient_path1 = os.path.join(folder1, patient_dir)
        patient_path2 = os.path.join(folder1, patient_dir)
        #在同一个病人文件夹下找到病人的112_liver.nii.gz和112_SUV_resampled.nii.gz
        if os.path.isdir(patient_path1) and os.path.isdir(patient_path2):
            liver_path = os.path.join(patient_path1, '112_liver.nii.gz')
            suv_path = os.path.join(patient_path1, '112_SUV_resampled.nii.gz')

            if os.path.exists(liver_path) and os.path.exists(suv_path):
                liver_data = load_nii(liver_path)
                suv_data = load_nii(suv_path)

                print(f'liver_path:{liver_path}')

                print(suv_data.shape)
                print(liver_data.shape)
                #确定liver和SUV形状一致
                if(suv_data.shape != liver_data.shape):
                    continue

                print(f'当前处理的患者是：{patient_path1}')
                #计算的SUVmedian
                median_suv = calculate_median_suv(liver_data, suv_data)

                results.append({'Patient': patient_dir, 'Median_SUV': median_suv})
            else:
                if not os.path.exists(liver_path):
                    print(f"binarized_liver.nii.gz not found for {patient_dir}")
                if not os.path.exists(suv_path):
                    print(f"SUV.nii.gz not found for {patient_dir}")

    df = pd.DataFrame(results)
    df.to_csv('', index=False)
    print("Results saved to Patients_median_SUV.csv")


if __name__ == "__main__":
    main()
