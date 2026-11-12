from pathlib import Path
import random
import os
import sys
import shutil
import argparse


# Define and parse user input arguments

parser = argparse.ArgumentParser()

parser.add_argument(
    '--datapath',
    help='Path to data folder containing image and annotation files',
    required=True
)

parser.add_argument(
    '--train_pct',
    help='Ratio of images to go to train folder (example: 0.8)',
    type=float,
    default=0.8
)

args = parser.parse_args()

data_path = args.datapath
train_percent = args.train_pct


# Check for valid entries

if not os.path.isdir(data_path):
    print('Directory specified by --datapath not found.')
    sys.exit(1)

if train_percent < 0.01 or train_percent > 0.99:
    print('Invalid entry for train_pct. Please enter a number between 0.01 and 0.99.')
    sys.exit(1)


# Calculate validation and test percentages

remaining_percent = 1 - train_percent
val_percent = remaining_percent / 2
test_percent = remaining_percent / 2


# Define paths to input dataset

input_image_path = os.path.join(data_path, 'images')
input_label_path = os.path.join(data_path, 'labels')

if not os.path.isdir(input_image_path) or not os.path.isdir(input_label_path):
    print('The dataset must contain images and labels folders.')
    sys.exit(1)


# Define paths to output folders

cwd = os.getcwd()

train_img_path = os.path.join(cwd, 'data/train/images')
train_txt_path = os.path.join(cwd, 'data/train/labels')

val_img_path = os.path.join(cwd, 'data/validation/images')
val_txt_path = os.path.join(cwd, 'data/validation/labels')

test_img_path = os.path.join(cwd, 'data/test/images')
test_txt_path = os.path.join(cwd, 'data/test/labels')


# Remove previous split folders to avoid keeping old files

for split_path in [
    os.path.join(cwd, 'data/train'),
    os.path.join(cwd, 'data/validation'),
    os.path.join(cwd, 'data/test')
]:
    if os.path.exists(split_path):
        shutil.rmtree(split_path)


# Create output folders

for dir_path in [
    train_img_path, train_txt_path,
    val_img_path, val_txt_path,
    test_img_path, test_txt_path
]:
    os.makedirs(dir_path, exist_ok=True)
    print(f'Created folder at {dir_path}.')


# Get list of image files

img_file_list = sorted([
    path for path in Path(input_image_path).rglob('*')
    if path.is_file() and path.suffix.lower() in ['.jpg', '.jpeg', '.png']
])

print(f'\nNumber of image files: {len(img_file_list)}')


# Set random seed and shuffle image list

random.seed(42)
random.shuffle(img_file_list)


# Determine number of files for each subset

file_num = len(img_file_list)

train_num = int(file_num * train_percent)
remaining_num = file_num - train_num

val_num = remaining_num // 2
test_num = remaining_num - val_num

print('\nImages moving to each subset:')
print(f'Train: {train_num} ({train_percent * 100:.1f}%)')
print(f'Validation: {val_num} ({val_percent * 100:.1f}%)')
print(f'Test: {test_num} ({test_percent * 100:.1f}%)')


# Define subsets and destination folders

subsets = [
    (train_num, train_img_path, train_txt_path),
    (val_num, val_img_path, val_txt_path),
    (test_num, test_img_path, test_txt_path)
]


# Copy images and corresponding annotations

start_index = 0

for set_num, new_img_path, new_txt_path in subsets:

    selected_images = img_file_list[start_index:start_index + set_num]

    for img_path in selected_images:

        img_fn = img_path.name
        base_fn = img_path.stem
        txt_fn = base_fn + '.txt'

        txt_path = os.path.join(input_label_path, txt_fn)

        shutil.copy(img_path, os.path.join(new_img_path, img_fn))

        # Copy annotation if it exists.
        # Images without annotations are treated as background images.

        if os.path.exists(txt_path):
            shutil.copy(txt_path, os.path.join(new_txt_path, txt_fn))

    start_index += set_num


print('\nDataset split completed successfully.')
