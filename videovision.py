import cv2,os,replicate,base64,requests,glob,time,ffmpeg

api_token = "bbbecaf1d1c505aa269d0cd9b6008fd5a3e6385f"
os.environ["REPLICATE_API_TOKEN"] = api_token
model = replicate.models.get("tencentarc/gfpgan")
version = model.versions.get("9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3")
input_video= input("Enter the file name: ")

def frames2video():
    image_folder = f'result/'
    input_file = input_video
    video = cv2.VideoCapture(input_file)
    fps = video.get(cv2.CAP_PROP_FPS)
    video = cv2.VideoCapture(0)
    image_filenames = glob.glob(image_folder + '*.png')
    image_filenames.sort(key=lambda x: int(x.split('\\')[-1].split('.')[0]))
    first_image = cv2.imread(image_filenames[0])
    height, width, _ = first_image.shape
    frame_size = (width, height)
    output_file = 'output.avi'
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

    for filename in image_filenames:
        image = cv2.imread(filename)
        out.write(image)

    out.release()
    video.release()

    video = cv2.VideoCapture("output.avi")

    if not video.isOpened():
        raise IOError("Error opening the video file")

    fps = video.get(cv2.CAP_PROP_FPS)
    width, height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        out.write(frame)

    video.release()
    out.release()



def img2uri(img):
    with open(img, "rb") as image_file:
        image_data = image_file.read()

    image_data_base64 = base64.b64encode(image_data).decode("utf-8")
    data_uri = "data:image/png;base64," + image_data_base64
    return data_uri

def url2img(url,img):
  image_url = url

  response = requests.get(image_url)

  if response.status_code == 200:
    with open(img, 'wb') as f:
      f.write(response.content)

def predict(img,name):
    uri = img2uri(img)
    img = version.predict(img=uri)
    url2img(img, name)

def video2frames(vid,dire):
    print(vid)
    cap = cv2.VideoCapture(vid)
    if not cap.isOpened():
        raise IOError("Error opening video file!")
    success, frame = cap.read()
    if not os.path.exists(dire):
        os.makedirs(dire)
    count = 1
    while success:
        cv2.imwrite(f"{dire}/frame{count}.jpg", frame)
        success, frame = cap.read()
        count += 1
    cap.release()

video2frames(input_video, 'images')

images = os.listdir('images')
images.sort(key=lambda x: int(x.split(".")[0][5:]))
i = 0

def seconds_to_string(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    days = hours // 24
    hours = hours % 24
    result = ''
    if days > 0:
        result += f'{days} days '
    if hours > 0:
        result += f'{hours} hours '
    if minutes > 0:
        result += f'{minutes} minutes '
    if seconds > 0:
        result += f'{seconds} seconds'

    return result
initial = time.time()
for image in images:
    if not os.path.exists('result'):
        os.makedirs('result')
    predict(f"images/{image}", f"result/{image.split('.jpg')[0].split('frame')[1]}.png")
    os.system('cls')
    i+=1
    final = round(round(time.time()-initial)/i)
    time_remaining = seconds_to_string((len(images)-i)*final)
    
    print(f"{round((i/len(images))*100)}% Completed!\n{time_remaining} remaining!")
frames2video()


input_filename = 'output.avi'
output_filename = 'output.mp4'

(
    ffmpeg
    .input(input_filename)
    .output(output_filename, c='copy', f='mp4')
    .overwrite_output()
    .run()
)
input_file = input_video
output_file = "output.mp3"

command = ['ffmpeg', '-i', input_file, output_file]
subprocess.run(command)

input_video = "output.mp4"
input_audio = "output.mp3"
output_file = "final.mp4"

command = ['ffmpeg', '-i', input_video, '-i', input_audio, '-c', 'copy', output_file]
subprocess.run(command)

os.system('del output.mp3')
os.system('del output.mp4')
os.system('del output.avi')
