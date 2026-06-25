import cv2 
import numpy as np
import random 
from createPlane import plane 

cars_data = [
    {
        "dosya" : "camauflage_car.png",
        "width" : 100,
        "height" : 130
    },
    {
        "dosya" : "camauflage_car1.png",
        "width" : 45,
        "height" : 70
    }
]

car_templates = []

for data in cars_data:
    img = cv2.imread(data["dosya"], cv2.IMREAD_UNCHANGED)
    if img is not None:
        car_templates.append({
            'original_img' : img,
            'target_width' : data["width"],
            'target_height' : data["height"] 
        })
    else:
        print(f"WARNING! {data['dosya']} is not found.")

plane_height, plane_width, _ = plane.shape 

listOfCars = [] 
numberOfCars = 5

for _ in range(numberOfCars):
    selected_template_index = random.randint(0, len(car_templates) - 1)
    selected_template = car_templates[selected_template_index]

    x = random.randint(0, plane_width - int(selected_template['target_width']))
    y = random.randint(0, plane_height - int(selected_template['target_height']))
    
    hiz = random.uniform(3.0, 5.5) 
    aci = random.uniform(0, 2 * np.pi) 
    salinim = random.uniform(-0.15, 0.15)
    
    listOfCars.append([float(x), float(y), float(hiz), float(aci), float(salinim), selected_template_index]) 

cv2.namedWindow('Simulation', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Simulation', 1400, 800)

selection_done = False
filter_type = 1

def click_event(event, x, y, flags, param):
    global selection_done, filter_type

    if event == cv2.EVENT_LBUTTONDOWN:
        if 150 <= x <= 650 and 450 <= y <= 600:
            filter_type = 1
            selection_done =  True
        elif 750 <= x <= 1250 and 450 <= y <= 600:
            filter_type = 2
            selection_done = True

cv2.setMouseCallback('Simulation', click_event) 

selection_screen = np.zeros((800, 1400, 3), dtype = np.uint8)

cv2.putText(selection_screen, "SIMULATION", (450, 180), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 4, cv2.LINE_AA)
cv2.putText(selection_screen, "Please select the filter you want to apply: ", (250, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (200, 200, 200), 2, cv2.LINE_AA)

cv2.rectangle(selection_screen, (150, 500), (650, 600), (0, 255, 255), -1)
cv2.putText(selection_screen, "Noise Filter", (230, 590), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3, cv2.LINE_AA)

cv2.rectangle(selection_screen, (750, 500), (1250, 600), (0, 0, 255), -1)
cv2.putText(selection_screen, "Noise + Thermal Negative Filter", (765, 590), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (255, 255, 255), 3, cv2.LINE_AA)

while not selection_done:
    cv2.imshow("Simulation", selection_screen)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit()

def nothing(x):
    pass

cv2.createTrackbar("Noise Level", "Simulation", 25, 100, nothing)
cv2.createTrackbar("Car Scale %", "Simulation", 20, 100, nothing)
cv2.createTrackbar("Shake Intensity", "Simulation", 10, 50, nothing)


scroll_x = 0
scroll_y = 0
scroll_speed_x = 3 
scroll_speed_y = 2 

t_counter = 0

while True:
   
    base_plane = plane.copy()

    for car in listOfCars:
        template_index = int(car[5])
        selected_template = car_templates[template_index]
        
        car[3] += car[4] 
        car[0] += np.cos(car[3]) * car[2]
        car[1] += np.sin(car[3]) * car[2]

        if random.random() < 0.03: 
            car[4] = -car[4]

        if car[0] > plane_width:
            car[0] = -selected_template['target_width']
        elif car[0] < -selected_template['target_width']:
            car[0] = plane_width

        if car[1] > plane_height:
            car[1] = -selected_template['target_height']
        elif car[1] < -selected_template['target_height']:
            car[1] = plane_height

        x, y = int(car[0]), int(car[1])

        angle_deg = np.degrees(car[3]) + 180 
        src_h, src_w = selected_template['original_img'].shape[:2]
        center = (src_w / 2, src_h / 2) 
        
        rotation_matrix = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
        rotated_img = cv2.warpAffine(selected_template['original_img'], rotation_matrix, (src_w, src_h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
        rotated_img = cv2.resize(rotated_img, (int(selected_template['target_width']), int(selected_template['target_height'])))
        
        car_bgr = rotated_img[:, :, :3]
        car_mask = rotated_img[:, :, 3] / 255.0

        car_w = int(selected_template['target_width'])
        car_h = int(selected_template['target_height'])

        scale_percentage = cv2.getTrackbarPos("Car Scale %", 'Simulation')
        scale_factor = scale_percentage / 100.0

        

        angle_deg = np.degrees(car[3]) + 180 
        src_h, src_w = selected_template['original_img'].shape[:2]
        center = (src_w / 2, src_h / 2) 

        max_dim =  int(np.sqrt(src_w ** 2 + src_h ** 2))

        if max_dim % 2 != 0:
            max_dim += 1 

        safe_canvas = np.zeros((max_dim, max_dim, 4), dtype = np.uint8)

        x_offset = (max_dim - src_w) // 2
        y_offset = (max_dim - src_h) // 2
        safe_canvas[y_offset : y_offset+src_h, x_offset : x_offset+src_w] = selected_template['original_img']
        center_safe = (max_dim / 2, max_dim / 2)
        
        rotation_matrix = cv2.getRotationMatrix2D(center_safe, angle_deg, 1.0)
        rotated_img = cv2.warpAffine(safe_canvas, rotation_matrix, (max_dim, max_dim), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

        dynamic_width = max(1, int(rotated_img.shape[1] * scale_factor))
        dynamic_height = max(1, int(rotated_img.shape[0] * scale_factor))

        rotated_img = cv2.resize(rotated_img, (dynamic_width, dynamic_height))
        
        car_bgr = rotated_img[:, :, :3]
        car_mask = rotated_img[:, :, 3] / 255.0

        car_w = dynamic_width
        car_h = dynamic_height

        if 0 <= x < plane_width - car_w and 0 <= y < plane_height - car_h:
            area = base_plane[y : y + car_h, x : x + car_w]
            for c in range(0, 3):
                area[:, :, c] = (1.0 - car_mask) * area[:, :, c] + car_mask * car_bgr[:, :, c]
            base_plane[y : y + car_h, x : x + car_w] = area

    scroll_x = (scroll_x + scroll_speed_x) % plane_width
    scroll_y = (scroll_y + scroll_speed_y) % plane_height

    shake_intensity = cv2.getTrackbarPos("Shake Intensity", 'Simulation')

    shake_X = np.sin(t_counter * 1.5) * shake_intensity + np.random.uniform(-shake_intensity / 2, shake_intensity)
    shake_y = np.cos(t_counter * 2.0) * shake_intensity + np.random.uniform(-shake_intensity / 2, shake_intensity) 

    final_offset_x = scroll_x + int(shake_X)
    final_offset_y = scroll_y + int(shake_y)

        
    M = np.float32([[1, 0, final_offset_x], [0, 1, final_offset_y]])
    shifted_plane = cv2.warpAffine(base_plane, M, (plane_width, plane_height), borderMode=cv2.BORDER_WRAP)

    current_noise = cv2.getTrackbarPos("Noise Level", 'Simulation')
    noise = np.random.randint(0, max(1, current_noise), shifted_plane.shape, dtype=np.uint8)

    if filter_type == 2:
        shifted_plane = cv2.add(shifted_plane, noise)
        shifted_plane = cv2.bitwise_not(shifted_plane)
    else:
        shifted_plane = cv2.add(shifted_plane, noise)

    
    cv2.imshow('Simulation', shifted_plane)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


