"""
输入112_SUV_resampled.nii.gz和112_Bones_binarized.nii.gz
骨骼区域（bones_data > 0）的SUV值大于中位数（肝脏median_suv）的像素被设置为1，其他像素为0
"""
import os
import nibabel as nib
import numpy as np
import pandas as pd


def load_nii(file_path):
    """Load a NIfTI file and return the image data as a numpy array."""
    img = nib.load(file_path)
    data = img.get_fdata()
    return data, img.affine, img.header


def save_nii(data, affine, header, file_path):
    """Save a numpy array as a NIfTI file."""
    img = nib.Nifti1Image(data, affine, header)
    nib.save(img, file_path)


def generate_mask(suv_data, bones_data, median_suv):
    #如果骨骼的SUV大于0同时大于肝脏SUV的median，则设置为1，否则为0
    """Generate a mask where values at positions of bones_data > 0 are set to 1 if SUV > median_suv, otherwise 0."""
    mask = np.zeros_like(suv_data)#创建一个与SUV数据同样形状的零数组（mask）
    mask[(bones_data > 0) & (suv_data > median_suv)] = 1
    
    return mask


def main():
    csv_path = r''
    folder2 = r''
    folder3 = r''
    folder4 = r'/'
  

    # Read the CSV file
    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        patient_name = row['Patient']
        median_suv = row['Median_SUV']

        # patient_folder2 = os.path.join(folder2, str(int(patient_name)))
        # patient_folder4 = os.path.join(folder4, str(int(patient_name)))
        patient_folder2 = os.path.join(folder4, patient_name)
        patient_folder4 = os.path.join(folder4, patient_name)
        suv_path = os.path.join(patient_folder2, '112_SUV_resampled.nii.gz')
        bones_path = os.path.join(patient_folder4, '112_flip_label_resampled_2_CT.nii.gz')
        #bones_path = os.path.join(patient_folder4, '112_Bones_binarized.nii.gz')
        if os.path.exists(suv_path) and os.path.exists(bones_path):
            # Load SUV image
            suv_data, suv_affine, suv_header = load_nii(suv_path)
            # Load Bones image
            bones_data, bones_affine, bones_header = load_nii(bones_path)

            # Generate mask
            mask_data = generate_mask(suv_data, bones_data, median_suv)

            # Create the output directory if it doesn't exist
            # patient_folder3 = os.path.join(folder3, str(int(patient_name)))
            patient_folder3 = os.path.join(folder3, patient_name)
            os.makedirs(patient_folder3, exist_ok=True)

            # Save the mask
            #mask_path = os.path.join(patient_folder3, '112_ouhe_mask_median.nii.gz')
            mask_path = os.path.join(patient_folder3, '112_cross_person_Median_mask.nii.gz')
            save_nii(mask_data, suv_affine, suv_header, mask_path)

            print(f"Mask saved for {patient_name} at {mask_path}")
        else:
            if not os.path.exists(suv_path):
                print(f"SUV_resampled.nii.gz not found for {patient_name}")
            if not os.path.exists(bones_path):
                print(f"112_Bones_binarized.nii.gz not found for {patient_name}")


if __name__ == "__main__":
    main()
