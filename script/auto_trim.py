import os

from image_similarity_measures.quality_metrics import ssim
import cv2


if __name__ == '__main__':
    # load the images -- the original, the original + contrast,
    # and the original + photoshop
    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    root_folder = """images/Wood Youtube"""
    for file in os.listdir(root_folder):

        cap = cv2.VideoCapture(f"{root_folder}/{file}")
        fps = cap.get(cv2.CAP_PROP_FPS)

        prev_frame = None
        similar = None
        # Check if camera opened successfully
        if cap.isOpened() == False:
            print("Error opening video stream or file")

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        start_index = 0
        file_out = f"{root_folder}/done/{os.path.splitext(file)[0]}.avi"
        out = cv2.VideoWriter(file_out, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, (frame_width, frame_height))

        scale_percent = 25  # percent of original img size
        width = int(frame_width * scale_percent / 100)
        height = int(frame_height * scale_percent / 100)
        dim = (width, height)
        number_frame = 0
        is_full_sense = False
        total_frame = 0
        # Read until video is completed
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            # convert the images to grayscale
            if ret == True:

                # Display the resulting frame
                # cv2.imshow('Frame', frame)
                if prev_frame is not None:
                    origin_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                    prev_img = cv2.resize(prev_frame, dim, interpolation=cv2.INTER_AREA)
                    similar = ssim(origin_frame, prev_img)
                    # prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                    # original_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # similar = compare_images(frame, prev_frame, 'demo')
                    print("SSIM: %.2f FILE_OUT: %s Time %.1f" % (similar, file_out, round(total_frame/(fps*60), 1)))

                if similar:
                    if similar > 0.9 and number_frame/fps < 5:
                        number_frame += 1
                        out.write(frame)
                    if similar < 0.9:
                        number_frame = 0

                total_frame += 1
                prev_frame = frame
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break

            # Break the loop
            else:
                break

        # When everything done, release the video capture object
        cap.release()

        # Closes all the frames
        cv2.destroyAllWindows()
