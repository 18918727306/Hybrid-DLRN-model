
“”“
遍历指定目录下每个病人命名的子文件夹，检查是否存在名为112_CT_resampled.nii.gz的CT图像文件

使用TotalSegmentator工具对CT图像进行分割，并将结果保存到病人对应的输出目录。

检查分割结果中是否存在liver.nii.gz文件。如果存在，将其重命名为112_liver.nii.gz；如果不存在，则输出相应的错误信息
”“”
# 进入主目录

cd ""

# 设置目标根目录

output_root=""
# 遍历每个以病人名字命名的文件夹
for patient_dir in *; do
    if [ -d "$patient_dir" ]; then
        cd "$patient_dir"

        # 检查CT_resampled_112.nii.gz是否存在
        if [ -f "112_CT_resampled.nii.gz" ]; then
            # 设置病人liver的输出目录
            output_dir="$output_root/$patient_dir"
            liver_output="$output_dir/112_liver.nii.gz"

            # 如果liver_112.nii.gz已存在则跳过当前文件夹
            if [ -f "$liver_output" ]; then
                echo "112_liver.nii.gz already exists in $patient_dir, skipping..."
            else
                # 创建病人对应的输出目录
                mkdir -p "$output_dir"

                # 运行TotalSegmentator，并将liver结果保存在病人对应的输出目录中
                TotalSegmentator -i 112_CT_resampled.nii.gz -o "$output_dir" -rs liver

                # 检查并重命名liver.nii.gz为liver_112.nii.gz
                if [ -f "$output_dir/liver.nii.gz" ]; then
                    mv "$output_dir/liver.nii.gz" "$liver_output"
                    echo "Renamed liver.nii.gz to 112_liver.nii.gz in $patient_dir"
                else
                    echo "liver.nii.gz not found after segmentation in $patient_dir"
                fi
            fi
        else
            echo "CT_resampled_112.nii.gz not found in $patient_dir"
        fi
        cd ..
    fi
done
