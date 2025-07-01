#!/bin/bash
# 进入主目录

cd /media/liu/6
# 遍历每个以病人名字命名的文件夹
for patient_dir in *; do
    if [ -d "$patient_dir" ]; then
        cd "$patient_dir"
        if [ -f "112_Bones.nii" ]; then
            echo "Bones.nii already exists in $patient_dir. Skipping..."
        else
            if [ -f "112_CT_resampled.nii.gz" ]; then
                TotalSegmentator -i 112_CT_resampled.nii.gz -o 112_Bones -rs sacrum vertebrae_C1 vertebrae_C2 vertebrae_C3 vertebrae_C4 vertebrae_C5 vertebrae_C6 vertebrae_C7 vertebrae_T1 vertebrae_T2 vertebrae_T4 vertebrae_T5 vertebrae_T6 vertebrae_T7 vertebrae_T8 vertebrae_T9 vertebrae_T10 vertebrae_T11 vertebrae_T12 vertebrae_L1 vertebrae_L2 vertebrae_L3 vertebrae_L4 vertebrae_L5 humerus_left humerus_right scapula_left scapula_right clavicula_left clavicula_right femur_left femur_right hip_left hip_right rib_left_1 rib_left_2 rib_left_3 rib_left_4 rib_left_5 rib_left_6 rib_left_7 rib_left_8 rib_left_9 rib_left_10 rib_left_11 rib_left_12 rib_right_1 rib_right_2 rib_right_3 rib_right_4 rib_right_5 rib_right_6 rib_right_7 rib_right_8 rib_right_9 rib_right_10 rib_right_11 rib_right_12 sternum costal_cartilages costal_cartilages --ml
            else                                                                      
                echo "112_CT_resampled.nii.gz not found in $patient_dir"
            fi
        fi
        cd ..
    fi
done
