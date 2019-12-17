import os
import imageio

png_dir = 'gif'
images = []
for file_name in os.listdir(png_dir):
    if file_name.endswith('.png'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave('gif/lucknow-aod-january-2019.gif', images, fps=1)