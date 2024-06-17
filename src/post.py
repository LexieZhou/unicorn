
import os
import traceback, sys

from utils.mesh import save_mesh_as_obj
import reconstruct as rc

def post(self):
    try:
        room_furniture_file = self.get_argument("room_furniture_file", None)
        room_furniture_type = self.get_argument("room_furniture_type", None)

        if room_furniture_file and room_furniture_type:
        # Reconstruct furniture
            reconstruction_model = rc.reconstruct(image_path=f"/app/input/{room_furniture_file}", furniture_type=room_furniture_type)
            # Generate result file paths
            filename, _ = os.path.splitext(room_furniture_file)
            obj_path = f"/app/output/{filename}_mesh.obj"
            save_mesh_as_obj(reconstruction_model, obj_path)
            self.write(f"{filename}_mesh.obj")
            self.set_status(200)
            return
    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())
        err = traceback.format_exc()