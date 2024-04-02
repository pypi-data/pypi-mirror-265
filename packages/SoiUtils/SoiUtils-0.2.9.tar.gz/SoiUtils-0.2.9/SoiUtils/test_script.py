from datasets.datasets import ImageDetectionDatasetCollection, collate_fn, export_dataset
from cloud.storage import download_folder
from pathlib import Path
import os
from torch.utils.data import DataLoader

#download_folder("/home/xd_alazar_gcp_idf_il/data/soi_exp_dataset_new", "soi_analytics", "soi_experiments")
video_collection = ImageDetectionDatasetCollection("/home/xd_alazar_gcp_idf_il/data/new_videos", 
                                                   [])
export_dataset(video_collection, "/home/xd_alazar_gcp_idf_il/data/", "soi_exp_dataset_new", copy_images=False, move_images=False, tags=None)
video_collection.export("./coco_dataset", "temp_name.json", copy_images=True)

"""
loader = DataLoader(video_collection, batch_size=2, collate_fn=collate_fn, shuffle=True)
for i, (_, dets) in enumerate(loader):
    print(f"{i}. Number of dets {len(dets[0])}")

for i in range(video_collection.num_subsets()):
    print(len(video_collection.get_sub_dataset(i)))
"""
