'''
A simple Program for grabing video from basler camera and converting it to opencv img.
Tested on Basler acA1300-200uc (USB3, linux 64bit , python 3.5)
'''
from pypylon import pylon
import cv2
import time

dummy = cv2.imread("10038.png")
demmy = cv2.rectangle(dummy, (0, 0), (1280, 1024), (0, 0, 0))


class kamera():
    def __init__(self, ip_address='169.254.203.55'):
        info = pylon.DeviceInfo()
        info.SetPropertyValue('IpAddress', ip_address)
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice(info))
        self.camera.ExposureTimeAbs = 500
        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        self.converter = pylon.ImageFormatConverter()

        #        self.camera.PixelFormat = 'BGR8Packed'

        print(self.camera.PixelFormat())
        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        print('Connected')

    def ambilgambar(self):
        try:
            grabresult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            # print("ambil gambar",  grabResult.GrabSucceeded())
            if grabresult.GrabSucceeded():
                # Access the image data
                image = self.converter.Convert(grabresult)
                img = image.GetArray()
                # print(img.shape)
                return img, 1
            else:
                # return np.zeros((1024,1280,3)).astype(np.uint8), 0
                while not grabresult.GrabSucceeded():
                    grabresult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                image = self.converter.Convert(grabresult)
                img = image.GetArray()
                return img, 1

            #     img = np.zeros((3,3,3))            
            # grabResult.Release()
            # camera.StopGrabbing()
        # Releasing the resource    
        # return img
        except Exception as e:
            exit()
            print('gagal ambil gambar')
            print(e)
            return dummy, 0


if __name__ == '__main__':
    cam1 = kamera('192.168.0.234')
    cam2 = kamera('192.168.0.123')
    input('Press Enter')
    while True:
        st = time.time()
        pic1, __ = cam1.ambilgambar()
        pic2, __ = cam2.ambilgambar()
        # print(time.time()-st)
        cv2.imshow('hasil basler', pic1)
        cv2.imshow('hasil basler2', pic2)
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()
# camera.StopGrabbing(),
