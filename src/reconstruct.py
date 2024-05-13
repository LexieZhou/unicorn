import argparse
import warnings
import os
from rembg import remove

import numpy as np
from torch.utils.data import DataLoader

from dataset import get_dataset
from model import load_model_from_path
from model.renderer import save_mesh_as_gif
from utils import path_mkdir
from utils.path import MODELS_PATH
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
    # Load the model and prepare it
    device = get_torch_device()
    model = furniture_type + '.pkl'
    m = load_model_from_path(MODELS_PATH / model).to(device)
    m.eval()

    # change background of the image to white
    input_img = open(image_path, 'rb').read()
    output_img = remove(input_img, bgcolor=[255, 255, 255, 255])

    # save the image with no background
    noBG_folder = 'img_no_bg'
    os.makedirs(noBG_folder, exist_ok=True)
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
    input_image_path = os.path.join("demo", 'chair3.jpeg')
    reconstruction_model = reconstruct(input_image_path, 'chair')

    # save the result
    out = path_mkdir('demo' + '_rec')
    name = 'chair3'
    save_mesh_as_obj(reconstruction_model, out / f'{name}_mesh.obj')
    # if SAVE_GIF:
    #     save_mesh_as_gif(reconstruction_model, out / f'{name}_mesh.gif', n_views=100, dist=d, elev=e, renderer=m.renderer)

    print_log("Done!")