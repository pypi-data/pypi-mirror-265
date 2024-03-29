from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

class HandRecognition:
    first_hand_fingers = []
    second_hand_fingers = []
    mpDraw = None
    mpHands = None
    cv2 = None

    def __init__(self, mpDraw, mpHands, cv2):
        self.mpDraw = mpDraw
        self.mpHands = mpHands
        self.cv2 = cv2

    def draw_hands(self, results, img):
        if results:
            FH = []
            SH = []
            for handLms in results:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if len(FH) <= 20:
                        FH.append((cx, cy))
                    else:
                        SH.append((cx, cy))
                    self.cv2.circle(img, (cx, cy), 10, (255, 0, 255), self.cv2.FILLED)
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            self.first_hand_fingers = FH
            self.second_hand_fingers = SH

    def get_fingertips_position(self, hand_id, fingertip_id):
        if not hand_id:
            if len(self.first_hand_fingers) >= 20:
                return self.first_hand_fingers[fingertip_id]
        else:
            if len(self.second_hand_fingers) >= 20:
                return self.second_hand_fingers[fingertip_id]
        return 0, 0


class Volume:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    def set_master_volume(self, volume):
        try:
            self.volume.SetMasterVolumeLevel(volume, None)
        except:
            pass