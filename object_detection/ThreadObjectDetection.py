import json
import cv2
import threading

import numpy as np
import requests
from pyzbar.pyzbar import decode
from domain.PlantEntity import Plant
from vehicle.ThreadVehicle import VehicleControlling

API_KEY = '2b10glUixSPZOunMJ952kc5Pe'
API_URL = f'https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}'
IMAGES_PER_PLANT = 3


def calc_center(rect):
    x = (rect[0][0][0] + rect[2][0][0]) / 2
    y = (rect[0][0][1] + rect[2][0][1]) / 2
    return int(x), int(y)


def calc_qr_code_len(rect):
    x_1 = abs(rect[0][0][0] + rect[1][0][0])
    x_2 = abs(rect[0][0][0] + rect[2][0][0])
    return max([x_1, x_2])


def cut_image(img, qrc_len, qrc_center):
    plant_img = img[0]
    return plant_img


class ObjectDetection(threading.Thread):
    def __init__(self, vehicle_controller: VehicleControlling, src: int = 0, piCam: bool = False,
                 frame_height: int = 640,
                 frame_width: int = 480,
                 framerate: int = 32, exposure_mode: str = "sport"):
        super().__init__()
        self.vehicle_controller = vehicle_controller
        self.CAMERA_LOCK = threading.Lock()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, frame_height)
        self.cap.set(4, frame_width)
        # self.stream = PiVideoStream(resolution=(640, 480), framerate=60, exposure_mode="sport").start()
        # sleep(1)
        self.attempts = 3
        self.plants = []
        self.detect_positions = []

    def qr_code_scanner(self):
        while True:
            success, img = self.cap.read()
            for barcode in decode(img):
                # Add Rectangle around QR - Code
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                img_arr = np.array(img)

                # len_qr_code = calc_qr_code_len(pts)
                center_qr_code = calc_center(pts)
                dist = center_qr_code[0] - img_arr.shape[1] / 2

                cv2.putText(img, str(dist), center_qr_code, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.polylines(img, [pts], True, (255, 0, 255), 5)

                if abs(dist) <= (img_arr.shape[1] / 5):
                    # plant_img = cut_image(img, len_qr_code, center_qr_code)
                    # Read QR - Code
                    tempData = barcode.data.decode('utf-8')
                    img = cut_image(img=img, qrc_center=center_qr_code, qrc_len=calc_qr_code_len)

                    if (not ObjectDetection.has_numbers(tempData)) and (1 not in self.detect_positions):
                        if self.detect_plant(1, img):
                            self.detect_positions.append(1)
                            print(f"\nDie Pflanzen an Position {self.detect_positions} sind erkannt.")

                    elif ("1" in tempData) and (2 not in self.detect_positions):
                        if self.detect_plant(2, img):
                            self.detect_positions.append(2)
                            print(f"\nDie Pflanzen an Position {self.detect_positions} sind erkannt.")

                    elif ("2" in tempData) and (3 not in self.detect_positions):
                        if self.detect_plant(3, img):
                            self.detect_positions.append(3)
                            print(f"\nDie Pflanzen an Position {self.detect_positions} sind erkannt.")

                    elif ("3" in tempData) and (4 not in self.detect_positions):
                        if self.detect_plant(4, img):
                            self.detect_positions.append(4)

                    elif ("4" in tempData) and (5 not in self.detect_positions):
                        if self.detect_plant(5, img):
                            self.detect_positions.append(5)
                            print(f"\nDie Pflanzen an Position {self.detect_positions} sind erkannt.")

                    elif ("5" in tempData) and (6 not in self.detect_positions):
                        if self.detect_plant(6, img):
                            self.detect_positions.append(6)
                            print(f"\nDie Pflanzen an Position {self.detect_positions} sind erkannt.")
                            self.find_similar_plants()

            cv2.imshow('Result', img)
            cv2.waitKey(1)

    def make_image(self, img, len_qr_code):
        pass

    def detect_plant(self, position, frame):
        print(f"Probiere Pflanze an Position {position} zu erkennen.")
        # cv2.imwrite(f'../plant_images/plant_{position}.jpg', frame)
        img = open(f'../plant_images/plant_{position}.jpg', 'rb')
        if img:
            image_path = f'plant_images/plant_{position}.jpg'
            image_data = open(image_path, 'rb')
            data = {
                'organs': ['leaf']
            }

            files = [
                ('images', (image_path, image_data))
            ]

            for i in range(self.attempts):
                req = requests.Request('POST', url=API_URL, files=files, data=data)
                prepared = req.prepare()

                s = requests.Session()
                response = s.send(prepared)
                json_result = json.loads(response.text)

                if response.status_code == 200:
                    print(json_result[list(json_result.keys())[4]][1])
                    score_1 = json_result[list(json_result.keys())[4]][0]['score']
                    scientificNameWithoutAuthor_1 = json_result[list(json_result.keys())[4]][0]['species'][
                        'scientificNameWithoutAuthor']
                    genus_1 = json_result[list(json_result.keys())[4]][0]['species']['genus'][
                        'scientificNameWithoutAuthor']
                    family_1 = json_result[list(json_result.keys())[4]][0]['species']['family'][
                        'scientificNameWithoutAuthor']
                    scientificName_1 = json_result[list(json_result.keys())[4]][0]['species']['scientificName']
                    commonNames_1 = json_result[list(json_result.keys())[4]][0]['species']['commonNames']

                    scientificNameWithoutAuthor_2 = None
                    genus_2 = None
                    family_2 = None
                    scientificName_2 = None
                    commonNames_2 = None

                    if len(json_result[list(json_result.keys())[4]]) > 1:
                        score_2 = json_result[list(json_result.keys())[4]][1]['score']
                        scientificNameWithoutAuthor_2 = json_result[list(json_result.keys())[4]][1]['species'][
                            'scientificNameWithoutAuthor']
                        genus_2 = json_result[list(json_result.keys())[4]][1]['species']['genus'][
                            'scientificNameWithoutAuthor']
                        family_2 = json_result[list(json_result.keys())[4]][1]['species']['family'][
                            'scientificNameWithoutAuthor']
                        scientificName_2 = json_result[list(json_result.keys())[4]][1]['species']['scientificName']
                        commonNames_2 = json_result[list(json_result.keys())[4]][1]['species']['commonNames']

                    self.plants.append(
                        Plant(position=position, scientificNameWithoutAuthor=scientificNameWithoutAuthor_1,
                              genus=genus_1, family=family_1, scientificName=scientificName_1,
                              commonNames=commonNames_1, scientificNameWithoutAuthor_2=scientificNameWithoutAuthor_2,
                              genus_2=genus_2, family_2=family_2, scientificName_2=scientificName_2,
                              commonNames_2=commonNames_2))
                    self.vehicle_controller.update_plant_website(self.plants[-1])

                    return True
                else:
                    print(
                        f"Fehler beim erkennen von Pflanze an Position: {position} Fehler Code API: {response.status_code}. Try Again...")

            return False

    def find_similar_plants(self):
        if 1 in self.detect_positions:
            parc_plant = self.find_plant_by_position(1)
            if parc_plant is not None:
                print("Beginne gleiche Pflanze zu finden.")
                positions = self.detect_positions[1:]

                same_scientificNameWithoutAuthor = []
                same_scientificName = []
                same_genus = []
                same_family = []
                same_commonNames = []

                for plant_pos in positions:
                    plant = self.find_plant_by_position(plant_pos)
                    if plant is not None:
                        if plant.compare_scientificNameWithoutAuthor(parc_plant):
                            same_scientificNameWithoutAuthor.append(plant)
                        elif plant.compare_scientificName(parc_plant):
                            same_scientificName.append(plant)
                        elif plant.compare_genus(parc_plant):
                            same_genus.append(plant)
                        elif plant.compare_family(parc_plant):
                            same_family.append(plant)
                        elif plant.compare_commonNames(parc_plant):
                            same_commonNames.append(plant)

                if len(same_scientificNameWithoutAuthor) > 0:
                    print(f"Pflanze im Parcour war {parc_plant.scientificNameWithoutAuthor}")
                    for plant in same_scientificNameWithoutAuthor:
                        print(f"Die Pflanze 1 ist die Gleiche wie {plant.position}")
                elif len(same_scientificName) > 0:
                    print(f"Pflanze im Parcour war {parc_plant.scientificName}")
                    for plant in same_scientificName:
                        print(f"Die Pflanze 1 ist die Gleiche wie {plant.position}")
                elif len(same_genus) > 0:
                    print(f"Pflanze im Parcour war {parc_plant.genus}")
                    for plant in same_genus:
                        print(f"Die Pflanze 1 ist die Gleiche Gattung wie {plant.position}")
                elif len(same_family) > 0:
                    print(f"Pflanze im Parcour war {parc_plant.family}")
                    for plant in same_family:
                        print(f"Die Pflanze 1 ist die Gleiche Family wie {plant.position}")
                elif len(same_commonNames) > 0:
                    print(f"Pflanze im Parcour war {parc_plant.commonNames}")
                    for plant in same_commonNames:
                        print(f"Die Pflanze 1 hat die Gleichen gängigen Namen wie {plant.position}")
                else:
                    print("Keine Pflanze ist im Ziel ist die selbe wie im Parcour.")
            else:
                print("Pflanze 1 konnte nicht gefunden werden...")

    def find_plant_by_position(self, position) -> Plant:
        for plant in self.plants:
            if plant.position == position:
                return plant
        return None

    @staticmethod
    def has_numbers(inputString):
        return any(char.isdigit() for char in inputString)

    def run(self):
        thread_driving = threading.Thread(target=self.qr_code_scanner, name="Object Detection-Thread")
        thread_driving.start()
