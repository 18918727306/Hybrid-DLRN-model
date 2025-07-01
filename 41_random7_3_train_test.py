"""
随机将数据集划分成7：3的比例
"""
import os
import shutil
import random
import pandas as pd

# 定义路径
src_images_dir = ''
src_labels_dir = ''
dst_base_dir = ''

# 创建目标文件夹
imagesTr_dir = os.path.join(dst_base_dir, 'imagesTr')
imagesTs_dir = os.path.join(dst_base_dir, 'imagesTs')
labelsTr_dir = os.path.join(dst_base_dir, 'labelsTr')
labelsTs_dir = os.path.join(dst_base_dir, 'labelsTs')

os.makedirs(imagesTr_dir, exist_ok=True)
os.makedirs(imagesTs_dir, exist_ok=True)
os.makedirs(labelsTr_dir, exist_ok=True)
os.makedirs(labelsTs_dir, exist_ok=True)

# 获取所有病人的文件名
patients = [f.split('_')[1] for f in os.listdir(src_images_dir) if f.endswith('0000.nii.gz')]

# 打乱顺序
random.shuffle(patients)

# # 定义函数用于检查连续编号并打乱
# def remove_consecutive(patients):
#     # 避免出现连续的病人
#     for i in range(1, len(patients)):
#         if abs(int(patients[i][1:]) - int(patients[i-1][1:])) == 1:
#             # 如果病人编号是连续的，就交换一下当前病人与列表后面的随机病人
#             swap_idx = random.randint(i, len(patients) - 1)
#             patients[i], patients[swap_idx] = patients[swap_idx], patients[i]
#     return patients

# # 打乱后检查是否有连续病人，并进行调整
# patients = remove_consecutive(patients)

# 按7:3分割
split_index = int(len(patients) * 0.8)
train_patients = patients[:split_index]
test_patients = patients[split_index:]

# 记录训练集和测试集的病人文件名（只记录需要的部分）
train_patient_names = []
test_patient_names = []

# 复制训练集病人文件
for patient in train_patients:
    # 复制 CT 和 SUV 文件到 imagesTr
    ct_file = os.path.join(src_images_dir, f'MM_{patient}_0000.nii.gz')
    suv_file = os.path.join(src_images_dir, f'MM_{patient}_0001.nii.gz')
    
    shutil.copy(ct_file, os.path.join(imagesTr_dir, f'MM_{patient}_0000.nii.gz'))
    shutil.copy(suv_file, os.path.join(imagesTr_dir, f'MM_{patient}_0001.nii.gz'))
    
    # 复制标签文件到 labelsTr
    label_file = os.path.join(src_labels_dir, f'MM_{patient}.nii.gz')
    shutil.copy(label_file, os.path.join(labelsTr_dir, f'MM_{patient}.nii.gz'))
    
    # 记录病人文件名
    train_patient_names.append(f'{patient}')

# 复制测试集病人文件
for patient in test_patients:
    # 复制 CT 和 SUV 文件到 imagesTs
    ct_file = os.path.join(src_images_dir, f'MM_{patient}_0000.nii.gz')
    suv_file = os.path.join(src_images_dir, f'MM_{patient}_0001.nii.gz')
    
    shutil.copy(ct_file, os.path.join(imagesTs_dir, f'MM_{patient}_0000.nii.gz'))
    shutil.copy(suv_file, os.path.join(imagesTs_dir, f'MM_{patient}_0001.nii.gz'))
    
    # 复制标签文件到 labelsTs
    label_file = os.path.join(src_labels_dir, f'MM_{patient}.nii.gz')
    shutil.copy(label_file, os.path.join(labelsTs_dir, f'MM_{patient}.nii.gz'))
    
    # 记录病人文件名
    test_patient_names.append(f'{patient}')

# 处理训练集和测试集长度不一致的问题，填充空白确保两者长度一致
max_len = max(len(train_patient_names), len(test_patient_names))
train_patient_names += [''] * (max_len - len(train_patient_names))  # 如果train_patient_names短，补充空值
test_patient_names += [''] * (max_len - len(test_patient_names))  # 如果test_patient_names短，补充空值

# 创建Excel表格，只记录第一列和第五列
df = pd.DataFrame({
    'Train_Patient_Names': train_patient_names,  # 第一列
    '': '',  # 空白列
    '': '',  # 空白列
    '': '',  # 空白列
    'Test_Patient_Names': test_patient_names  # 第五列
})

# 保存Excel文件
excel_path = os.path.join(dst_base_dir, '')
df.to_excel(excel_path, index=False)

print(f"病人分组已完成，并保存到 {excel_path}")
