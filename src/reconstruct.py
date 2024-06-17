import argparse
import warnings
import os
import sys
import shutil
from rembg import remove

import numpy as np
from torch.utils.data import DataLoader

from dataset import get_dataset
from model import load_model_from_path
from model.renderer import save_mesh_as_gif
from utils import path_mkdir
from utils.path import MODELS_PATH, PROJECT_PATH
from utils.logger import print_log
from utils.mesh import save_mesh_as_obj, normalize
from utils.pytorch import get_torch_device


# BATCH_SIZE = 32
# N_WORKERS = 4
# PRINT_ITER = 2
# SAVE_GIF = True
warnings.filterwarnings("ignore")

# furniture_type is chair or table
def reconstruct(image_path, furniture_type):
    BATCH_SIZE = 32
    N_WORKERS = 4

    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # noBG_folder = os.path.join(script_dir, 'img_no_bg')
    # if os.path.exists(noBG_folder):
    #     print(f"Deleting existing '{noBG_folder}' folder...")
    #     shutil.rmtree(noBG_folder)
    # print(f"Creating '{noBG_folder}' folder...")
    # os.makedirs(noBG_folder)

    noBG_folder = os.path.join(PROJECT_PATH, 'img_no_bg')
    if os.path.exists(noBG_folder):
        print(f"Deleting existing '{noBG_folder}' folder...")
        shutil.rmtree(noBG_folder)
    print(f"Creating '{noBG_folder}' folder...")
    os.makedirs(noBG_folder)

    # Load the model and prepare it
    device = get_torch_device()
    model = furniture_type + '.pkl'
    m = load_model_from_path(MODELS_PATH / model).to(device)
    m.eval()

    # change background of the image to white
    input_img = open(image_path, 'rb').read()
    output_img = remove(input_img, bgcolor=[255, 255, 255, 255])

    # save the image with no background
    output_path = os.path.join(noBG_folder, os.path.basename(image_path))
    with open(output_path, 'wb') as output_file:
       output_file.write(output_img)
    
    # Load the image and reconstruct the mesh
    data = get_dataset(noBG_folder)(split='test', img_size=m.init_kwargs['img_size'])
    loader = DataLoader(data, batch_size=BATCH_SIZE, num_workers=N_WORKERS, shuffle=False)
    for j, (inp, _) in enumerate(loader):
        imgs = inp['imgs'].to(device)
        meshes = m.predict_mesh_pose_bkg(imgs)[0]
        mcenter = normalize(meshes[0])

        return mcenter


if __name__ == '__main__':
    print_log("Starting reconstruction...")

    # Check if the correct number of arguments is provided
    if len(sys.argv) < 3:
        print("Please provide image_path and image_type as arguments.")
        sys.exit(1)

    # # Get image_path and image_type from command-line arguments
    # out = path_mkdir('demo' + '_rec')
    # image_path = sys.argv[1]
    # image_type = sys.argv[2]
    # reconstruction_model = reconstruct(image_path, image_type)
    # save_mesh_as_obj(reconstruction_model, out / f'generated_mesh.obj')

    room_furniture_file = sys.argv[1]
    room_furniture_type = sys.argv[2]
    if room_furniture_file and room_furniture_type:
        # Reconstruct furniture
            reconstruction_model = reconstruct(image_path=f"/app/input/{room_furniture_file}", furniture_type=room_furniture_type)
            # Generate result file paths
            filename, _ = os.path.splitext(room_furniture_file)
            obj_path = f"/app/output/{filename}_mesh.obj"
            save_mesh_as_obj(reconstruction_model, obj_path)
    print_log("Done!")