# import required libraries
import cv2
import os

# read the input image
 

class FaceCrop:
    def __init__(self, root_folder,destination_folder):
        # self.rootfolder = "../Samples/"
        self.rootfolder = root_folder
        self.destination_folder = destination_folder

    def generate(self):
        self.loadVideos()

    def crop_face(self, file, user_dir):
        img = cv2.imread(file)
        print(file)
        # convert to grayscale of each frames
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # read the haarcascade to detect the faces in an image
        face_cascade = cv2.CascadeClassifier(
            'haarcascades/haarcascade_frontalface_default.xml')

        # detects faces in the input image
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        print('Number of detected faces:', len(faces))

        # loop over all detected faces
        if len(faces) > 0:
            for i, (x, y, w, h) in enumerate(faces):

                # To draw a rectangle in a face
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                face = img[y:y + h, x:x + w]
                # cv2.imshow("Cropped Face", face)
                print(user_dir)

                if not os.path.exists(f"faces/{user_dir}"):
                    print(f'faces/{user_dir}')
                    os.makedirs(f'faces/{user_dir}', exist_ok=True)
                cv2.imwrite(
                    f'faces/{user_dir}/{file.split("/")[-1]}', face)
                 

                # display the image with detected faces
                # cv2.imshow("image", img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

    def crop_frame(self, frame, user_dir):
        img = frame
        # print(file)
        # convert to grayscale of each frames
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # read the haarcascade to detect the faces in an image
        face_cascade = cv2.CascadeClassifier(
            'haarcascades/haarcascade_frontalface_default.xml')

        # detects faces in the input image
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        print('Number of detected faces:', len(faces))

        # loop over all detected faces
        if len(faces) > 0:
            for i, (x, y, w, h) in enumerate(faces):

                # To draw a rectangle in a face
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                face = img[y:y + h, x:x + w]
                # cv2.imshow("Cropped Face", face)
                print(user_dir)
                usernameFolder = user_dir.split("_")[0]
                usernameFile = user_dir.split("_")[1]
                print(usernameFile+" File")
                if not os.path.exists(f"{self.destination_folder}/{usernameFolder}"):
                    #print(f'faces/{usernameFolder}')
                    os.makedirs(f'{self.destination_folder}/{usernameFolder}', exist_ok=True)
                cv2.imwrite(
                    f'{self.destination_folder}/{usernameFolder}/{usernameFile}.jpg', face)
                print(f"{self.destination_folder}{i}.jpg is saved")

                # display the image with detected faces
                # cv2.imshow("image", img)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

    def loadVideos(self):
        #videorootfolder = "../Samples/Videos"
        videorootfolder = self.rootfolder
        for dir in os.listdir(videorootfolder):
            # set video file path of input video with name and extension
            print(f"{videorootfolder}/{dir}")
            vid = cv2.VideoCapture(f"{videorootfolder}/{dir}")

            if not os.path.exists('newimages'):
                os.makedirs('newimages')

            # for frame identity
            index = 0
            while (True):
                # Extract images
                ret, frame = vid.read()
                # end of frames
                if not ret:
                    break
                # Saves images
                name = 'newimages/frame' + str(index) + '.jpg'
                print('Creating...' + name)
                # cv2.imwrite(name, frame)
                print(f"{dir.split('.')[0]}_{index}")
                # if index < 70:
                self.crop_frame(frame, f"{dir.split('.')[0]}_{index}")
                # next frame
                index += 1
