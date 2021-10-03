import imageio
import os

def convert_video_to_gif(input_file, output_file=None):	
    if not output_file:
        output_file = os.path.splitext(input_file)[0] + ".gif"
		
    print("Converting {0} to {1}".format(input_file, output_file))

    reader = imageio.get_reader(input_file)
    fps = reader.get_meta_data()['fps']

    writer = imageio.get_writer(output_file, fps=fps)

    for i,im in enumerate(reader):
        writer.append_data(im)

    writer.close()

convert_video_to_gif("path/to/video", "path/to/gif")
