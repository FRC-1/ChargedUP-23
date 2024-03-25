import cv2
import numpy as np
from pupil_apriltags import Detector
import math

def GetHull(cnts):
    largest_cnt = []
    largest_area = 1000
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if(area > largest_area):
            largest_cnt = cnt
            largest_area = area
    hull = cv2.convexHull(largest_cnt)
    return [hull]

def DrawBoundingRect(img,rect,color = (255,255,255)):
    x,y,w,h = rect
    return cv2.rectangle(img.copy(),(x,y),(x+w,y+h),color,10)

def GetBoundingRect(cnts):
    x,y,w,h = cv2.boundingRect(GetHull(cnts)[0])
    return (x,y,w,h)

def GetCenter(rect):
    x,y,w,h = rect
    return (int(x+w/2),int(y+h/2))

def FindCone(cone_img):
    cone_HSV = cv2.cvtColor(cone_img,cv2.COLOR_BGR2HSV)
    cone_H, cone_S, cone_V = cv2.split(cone_HSV)

    cone_V_Map = cv2.inRange(cone_V,np.array([100]),np.array([255]))
    cone_S = cv2.bitwise_and(cone_S,cone_S,mask=cone_V_Map)
    cone_S_Map = cv2.inRange(cone_S,np.array([100]),np.array([255]))
    cone_H = cv2.bitwise_and(cone_H,cone_H,mask=cone_S_Map)
    cone_H_Map = cv2.inRange(cone_H,np.array([int((5/360)*255)]),np.array([int((60/360)*255)]))

    cnts, _ = cv2.findContours(cone_H_Map,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if(len(cnts) > 0):
        try:
            return GetBoundingRect(cnts)
        except:
            return (0,0,0,0)
    else:
        return (0,0,0,0)

def FindCube(cone_img):
    cube_HSV = cv2.cvtColor(cone_img,cv2.COLOR_BGR2HSV)
    cube_H, cube_S, cube_V = cv2.split(cube_HSV)

    cube_V_Map = cv2.inRange(cube_V,np.array([60]),np.array([255]))
    cube_S = cv2.bitwise_and(cube_S,cube_S,mask=cube_V_Map)
    cube_S_Map = cv2.inRange(cube_S,np.array([60]),np.array([255]))
    cube_H = cv2.bitwise_and(cube_H,cube_H,mask=cube_S_Map)
    cube_H_Map = cv2.inRange(cube_H,np.array([int((170/360)*255)]),np.array([int((220/360)*255)]))

    cnts, _ = cv2.findContours(cube_H_Map,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if(len(cnts) > 0):
        try:
            return GetBoundingRect(cnts)
        except:
            return (0,0,0,0)
    else:
        return (0,0,0,0)

def Calibration_Calibrate(capture,x_size = 9,y_size = 6):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((y_size*x_size,3), np.float32)
    objp[:,:2] = np.mgrid[0:x_size,0:y_size].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    counter = 0
    drop_counter = 0
    while capture.isOpened():
        ret, frame = capture.read()

        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        
        ret, corners = cv2.findChessboardCorners(gray, (x_size,y_size), None)
        # If found, add object points, image points (after refining them)
        drop_counter += 1
        if ret == True and drop_counter >= 10:
            drop_counter = 0
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            cv2.drawChessboardCorners(frame, (x_size,y_size), corners2, ret)
            counter += 1
            print("FOUND",counter)
        cv2.imshow('img', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.savez('camera_calib.npz',ret=ret,mtx=mtx,dist=dist,rvecs=rvecs,tvecs=tvecs)
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    print( "total error: {}".format(mean_error/len(objpoints)) )

def Calibration_GetOptimalNewCameraMTX(frame,mtx,dist):
    h,  w = frame.shape[:2]
    return cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

def Calibration_Undistort(frame,mtx,dist,newcameramtx = None, roi = None):
    h,  w = frame.shape[:2]
    if(newcameramtx is None and roi is None):
        newcameramtx, roi = Calibration_GetOptimalNewCameraMTX(frame,mtx,dist)

    # undistort
    dst = cv2.undistort(frame, mtx, dist, None, newcameramtx) 
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def Calibration_GetCameraParams(mtx):
    return (mtx[0][0],mtx[0][2],mtx[1][1],mtx[1][2])

def Marker_OBJP(real_marker_size):
    halfsize = real_marker_size/2
    TL = (-halfsize,-halfsize,0)
    TR = (halfsize,-halfsize,0)
    BL = (-halfsize,halfsize,0)
    BR = (halfsize,halfsize,0)

    return np.array([BL,BR,TR,TL])

def rotationMatrixToEulerAngles(R, degrees = True) :
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
 
    x = math.atan2(R[2,1] , R[2,2])
    y = math.atan2(-R[2,0], sy)
    z = math.atan2(R[1,0], R[0,0])
    
    if(degrees):
        return np.array([x*(180/math.pi),y*(180/math.pi),z*(180/math.pi)])
    return np.array([x, y, z])

def GetPitchYawRoll(RotationMatrix):
    Pitch = math.atan2(RotationMatrix[2][1], RotationMatrix[2][2])
    Yaw = math.atan2(-RotationMatrix[2][0], math.sqrt(RotationMatrix[2][1] * RotationMatrix[2][1] + RotationMatrix[2][2] * RotationMatrix[2][2]))
    Roll = math.atan2(RotationMatrix[1][0], RotationMatrix[0][0])
    return math.degrees(Pitch), math.degrees(Yaw)+90, math.degrees(Roll)

def GetPointAtDistanceAndAngle(distance,degrees):
    x = distance * math.cos(math.radians(degrees))
    y = distance * math.sin(math.radians(degrees))
    return (x,y)

def PythagoreanTheorem(a,b):
    return math.sqrt(a**2 + b**2)

def FindAprilTags(detector, undistorted):
    gray = cv2.cvtColor(undistorted,cv2.COLOR_BGR2GRAY)
    results = detector.detect(gray)
    final_detections = []
    for tag in results:
        if(tag.tag_id <= 8 and tag.hamming <= 0):
            final_detections.append(tag)
    return final_detections

def GetTagTransform(tag,objp,new_mtx,dist):
    ret, rvec,tvec = cv2.solvePnP(objp,tag.corners,new_mtx,dist)
    transform = ((-1,-1,-1),(-1,-1,-1))
    if(ret):
        x = tvec[0]
        y = tvec[2]
        z = tvec[1]

        rotation_matrix, _ = (cv2.Rodrigues(rvec))
        pitch, yaw, roll = GetPitchYawRoll(rotation_matrix)

        transform = ((x,y,z),(pitch,yaw,roll))
    return transform

def DrawCameraRelativeMap(frame,coords,multiplier=100):
    x = int(coords[0][0]*multiplier)
    y = int(coords[0][1]*multiplier)
    heading_angle = int(coords[1][1])
    map_target = (x+int(frame.shape[1]/2),int(frame.shape[0])-y)
    map = cv2.circle(np.zeros_like(frame,dtype=np.uint8),map_target,5,(0,0,255),-1)
    map = cv2.arrowedLine(map,(int(frame.shape[1]/2),int(frame.shape[0])),(int(frame.shape[1]/2),0),(255,0,0),2)
    target_heading = GetPointAtDistanceAndAngle(200,heading_angle)
    map = cv2.arrowedLine(map,map_target,(map_target[0]+int(target_heading[0]),map_target[1]+int(target_heading[1])),(0,255,0),3)
    return map

def GetCameraTransform(target_coords):
    target_x = target_coords[0][0]
    target_y = target_coords[0][1]
    target_yaw = target_coords[1][1]
    
    my_transform = (-1,-1,-1)
    distance_to_target = PythagoreanTheorem(target_x,target_y)
    if(distance_to_target > 0):
        if(int(target_x < 0)):
            gamma = math.degrees(math.asin(target_y/distance_to_target))
        else:
            gamma = 90 + (90-math.degrees(math.asin(target_y/distance_to_target)))
        camera_position = GetPointAtDistanceAndAngle(distance_to_target,gamma + 270-target_yaw)
        camera_position = (-(camera_position[0]),-(camera_position[1]))
        my_transform = (camera_position[0],camera_position[1],180-target_yaw)
    return my_transform

def DrawTargetRelativeMap(frame,camera_transform,multiplier=100):
    position_X = int(camera_transform[0]*multiplier)
    position_Y = int(camera_transform[1]*multiplier)
    rotation_Yaw = int(camera_transform[2])

    my_position = (position_X+int(frame.shape[1]/2),position_Y)
    my_heading = (GetPointAtDistanceAndAngle(200,rotation_Yaw))
    my_heading = (int(my_heading[0]),int(my_heading[1]))
    world_map = np.zeros_like(frame,dtype=np.uint8)
    world_map = cv2.arrowedLine(world_map,(int(frame.shape[1]/2),0),(int(frame.shape[1]/2),int(frame.shape[0])),(0,255,0),2)
    world_map = cv2.arrowedLine(world_map,my_position,(my_position[0]-my_heading[0],my_position[1]-my_heading[1]),(255,0,0),3)
    world_map = cv2.circle(world_map,(my_position),5,(0,0,255),-1)
    return world_map

tag_detector = Detector("tag16h5",decode_sharpening=10.0)
marker_objp = Marker_OBJP(0.15)

capture = cv2.VideoCapture('http://192.168.1.25:4747/video')

my_transform = (-1,-1,-1)
with np.load('camera_calib_1.npz') as X:
    mtx, dist, rvecs, tvecs = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
    new_mtx, roi = Calibration_GetOptimalNewCameraMTX(capture.read()[1],mtx,dist)
    params = Calibration_GetCameraParams(mtx)

    while capture.isOpened():
        ret, frame = capture.read()
        undistorted = Calibration_Undistort(frame,mtx,dist,new_mtx,roi)

        # rect_cube = FindCube(undistorted)
        # cv2.imshow('Cube',cv2.circle(DrawBoundingRect(frame,rect_cube),GetCenter(rect_cube),25,(0,0,0),2))
        # rect_cone = FindCone(undistorted)
        # cv2.imshow('Cone',cv2.circle(DrawBoundingRect(frame,rect_cone),GetCenter(rect_cone),25,(0,0,0),2))
        
        results = FindAprilTags(tag_detector,undistorted)
        for tag in results:
            for corner in tag.corners:
                cv2.circle(frame,(int(corner[0]),int(corner[1])),5,(0,0,255),-1)

            if(tag.tag_id == 7):
                tag_transform = GetTagTransform(tag,marker_objp,new_mtx,dist)
                my_transform = GetCameraTransform(tag_transform)
                print(my_transform[0],my_transform[1],my_transform[2])

        cv2.imshow('frame',frame)
        cv2.imshow('worldmap',DrawTargetRelativeMap(frame,my_transform))
        if(cv2.waitKey(1) == ord('q')):
            break