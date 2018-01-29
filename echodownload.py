import wget, sys, os, os.path, shutil, subprocess
import xml.etree.ElementTree as ET
from cv2 import VideoWriter, imread, resize
FPS = 20.0
def isfile(f):
    if not os.path.isfile(f):
        return False
    statinfo = os.stat(f)
    if statinfo.st_size < 4096:
        return False
    return True
class CV2Writer:
    def __init__(self, out_name, size):
        from cv2 import VideoWriter, VideoWriter_fourcc
        self.vid = VideoWriter(out_name, cv2.VideoWriter_fourcc(*"MP4V"), FPS, size, True)
    def write(self, img):
        self.vid.write(img)
    def close(self):
        self.vid.release()
class SKWriter:
    def __init__(self, out_name, size):
        import skvideo.io
        self.vid =  skvideo.io.FFmpegWriter(out_name, inputdict={'-r': str(int(FPS)) + "/1"})
    def write(self, img):
        self.vid.writeFrame(img)
    def close(self):
        self.vid.close()
BACKEND = SKWriter
for i in xrange(1, len(sys.argv), 2):
    base_url =  sys.argv[i].replace('https://', 'http://')
    uuid = base_url.split('/')[-2]
    if len(sys.argv) > 2:
        lecture_name = sys.argv[i + 1]
    else:
        lecture_name = uuid
    try:
        os.mkdir(lecture_name)
    except:
        pass 
    try:
        os.mkdir(os.path.join(lecture_name, 'build'))
    except:
        pass
    os.chdir(os.path.join(lecture_name, 'build'))

    print 'Downloading', lecture_name
    if not os.path.isfile('presentation.xml'):
        wget.download(base_url + 'presentation.xml')
    if not os.path.isfile('audio.mp3'):
        wget.download(base_url + 'audio.mp3') 

    presentation_root = ET.parse('presentation.xml').getroot()
    dest = os.path.join('..', lecture_name + '.mkv')
    if presentation_root.find(".//track[@type='video']") is not None:   
        for video in presentation_root.find(".//track[@type='video']"):
            uri = video.attrib['uri']
            if 'audio-video' not in uri:
                print 'No audio-video for', lecture_name
            if not os.path.isfile(uri):
                wget.download(base_url + uri)
            shutil.copy(uri, os.path.join('..', lecture_name + '.mp4')) 
            break 
    if not isfile(os.path.join('..', lecture_name + '.mp4')) and not isfile(dest): # create using flipbook
        writer = None
        size = None
        for image in presentation_root.find(".//track[@type='flipbook']"):
            duration, uri = int(image.attrib['duration']), image.attrib['uri']
            if not os.path.isfile(uri):
                wget.download(base_url + 'flipbook/' + uri)
            img = imread(uri).astype('uint8')
            if writer is None:
                if size is None:
                    size = img.shape[1], img.shape[0] 
                writer = BACKEND('out.avi', size)
            if size[0] != img.shape[1] or size[1] != img.shape[0]:
                resize_size = size[1], size[0]
                img = resize(img, resize_size) 
            for _ in xrange(duration / int(1000 * (1/FPS))):
                writer.write(img)
        writer.close() 
        subprocess.call(["ffmpeg", "-i", "out.avi", "-i", "audio.mp3", "-c", "copy", dest]) 
    os.chdir(os.path.join('..', '..')) 
    #os.remove(os.path.join(lecture_name, 'build'))