import meshcat
import numpy as np
import math

models = {
    "drivetrain" : meshcat.geometry.ObjMeshGeometry.from_file("I:\TomerSoftware\Code\Personal-Code\-1\Simulation\Robot Systems\Drivetrain.obj"),
    "arm base" : meshcat.geometry.ObjMeshGeometry.from_file("I:\TomerSoftware\Code\Personal-Code\-1\Simulation\Robot Systems\Arm Base.obj"),
    "arm stage 1" : meshcat.geometry.ObjMeshGeometry.from_file("I:\TomerSoftware\Code\Personal-Code\-1\Simulation\Robot Systems\Arm First Stage.obj"),
    "arm stage 2" : meshcat.geometry.ObjMeshGeometry.from_file("I:\TomerSoftware\Code\Personal-Code\-1\Simulation\Robot Systems\Arm Second Stage.obj"),
    "arm stage 3" : meshcat.geometry.ObjMeshGeometry.from_file("I:\TomerSoftware\Code\Personal-Code\-1\Simulation\Robot Systems\Arm Third Stage.obj"),
    "gripper" : meshcat.geometry.ObjMeshGeometry.from_file("I:\TomerSoftware\Code\Personal-Code\-1\Simulation\Robot Systems\Gripper.obj"),
}

class Robot():
    def __init__(self,visualizer):
        self.adjust_origin_location_drivetrain = np.array([0.0,-0.4,0.13160])
        self.adjust_origin_location_arm_base = np.array([0.0,0.0,0.2234])
        self.adjust_origin_location_arm_stage1_left = self.adjust_origin_location_arm_base + np.array([0.098016,0.21,0.094])
        self.adjust_origin_rotation_arm_stage1_Z = math.radians(90)
        self.adjust_origin_rotation_arm_stage1_X = math.radians(-90)
        
        self.adjust_origin_location_arm_stage1_right = self.adjust_origin_location_arm_base + np.array([-0.098016,0.21,0.094])
        self.adjust_origin_location_arm_gripper = self.adjust_origin_location_arm_base + np.array([-0.05,-0.38,0.03266])

        self.robot_location = np.array([0,0,0])
        self.robot_rotation = 0
        self.robot_arm_angle = 0
        self.robot_arm_distance = 0
        self.robot_turret_angle = 0

        self.gripper_angle = 30

        self.vis = visualizer

        visualizer["robot"]["drivetrain"]["mesh"].set_object(models["drivetrain"],meshcat.geometry.MeshLambertMaterial(color=0x212121))
        visualizer["robot"]["drivetrain"]["mesh"].set_transform(meshcat.transformations.translation_matrix(self.adjust_origin_location_drivetrain))

        visualizer["robot"]["arm"]["base"]["mesh"].set_object(models["arm base"],meshcat.geometry.MeshLambertMaterial(color=0x312121))    
        visualizer["robot"]["arm"]["base"]["mesh"].set_transform(meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_base))

        visualizer["robot"]["arm"]["left"]["stage1"]["mesh"].set_object(models["arm stage 1"],meshcat.geometry.MeshLambertMaterial(color=0x412121))    
        visualizer["robot"]["arm"]["left"]["stage1"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_left)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"]["arm"]["left"]["stage2"]["mesh"].set_object(models["arm stage 2"],meshcat.geometry.MeshLambertMaterial(color=0x512121))    
        visualizer["robot"]["arm"]["left"]["stage2"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_left)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"]["arm"]["left"]["stage3"]["mesh"].set_object(
            models["arm stage 3"],meshcat.geometry.MeshLambertMaterial(color=0x612121))    
        visualizer["robot"]["arm"]["left"]["stage3"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_left)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"]["arm"]["right"]["stage1"]["mesh"].set_object(
            models["arm stage 1"],meshcat.geometry.MeshLambertMaterial(color=0x412121))    
        visualizer["robot"]["arm"]["right"]["stage1"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_right)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"]["arm"]["right"]["stage2"]["mesh"].set_object(
            models["arm stage 2"],meshcat.geometry.MeshLambertMaterial(color=0x512121))    
        visualizer["robot"]["arm"]["right"]["stage2"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_right)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"]["arm"]["right"]["stage3"]["mesh"].set_object(
            models["arm stage 3"],meshcat.geometry.MeshLambertMaterial(color=0x612121))    
        visualizer["robot"]["arm"]["right"]["stage3"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_right)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"]["arm"]["right"]["gripper"]["mesh"].set_object(
            models["gripper"],meshcat.geometry.MeshLambertMaterial(color=0x712121))    
        visualizer["robot"]["arm"]["right"]["gripper"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_gripper)).dot(meshcat.transformations.rotation_matrix(np.radians(180+self.gripper_angle),[1,0,0])))

        self.set_rotation(0)

    def set_location(self,location):
        self.robot_location = location
        self.vis["robot"].set_transform(meshcat.transformations.translation_matrix(self.robot_location).dot(meshcat.transformations.rotation_matrix(self.robot_rotation,[0,0,1])))

    def set_rotation(self,degrees):
        self.robot_rotation = math.radians(degrees+90)
        self.vis["robot"].set_transform(meshcat.transformations.translation_matrix(self.robot_location).dot(meshcat.transformations.rotation_matrix(self.robot_rotation,[0,0,1])))

    def set_turret_angle(self,degrees):
        self.robot_turret_angle = math.radians(degrees)
        self.vis["robot"]["arm"].set_transform(meshcat.transformations.rotation_matrix(self.robot_turret_angle,[0,0,1]))

    def set_arm_angle(self,degrees):
        self.robot_arm_angle = math.radians(-degrees)
        self.vis["robot"]["arm"]["left"].set_transform(meshcat.transformations.rotation_matrix(self.robot_arm_angle,[1,0,0],self.adjust_origin_location_arm_stage1_left + np.array([0,0,-0.034])))
        self.vis["robot"]["arm"]["right"].set_transform(meshcat.transformations.rotation_matrix(self.robot_arm_angle,[1,0,0],self.adjust_origin_location_arm_stage1_right + np.array([0,0,-0.034])))

    def set_arm_distance(self,distance):
        distance = min(max(distance,0),0.45)
        self.robot_arm_distance = distance
        self.vis["robot"]["arm"]["left"]["stage2"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance,0]))
        self.vis["robot"]["arm"]["right"]["stage2"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance,0]))
        self.vis["robot"]["arm"]["left"]["stage3"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance*2,0]))
        self.vis["robot"]["arm"]["right"]["stage3"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance*2,0]))
        self.vis["robot"]["arm"]["right"]["gripper"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance*2,0]))

class Ghostbot():
    def __init__(self,visualizer,color = 0x00FF00,opacity = 0.25,id=1):
        self.adjust_origin_location_drivetrain = np.array([0.0,-0.4,0.13160])
        self.adjust_origin_location_arm_base = np.array([0.0,0.0,0.2234])
        self.adjust_origin_location_arm_stage1_left = self.adjust_origin_location_arm_base + np.array([0.098016,0.25,0.094])
        self.adjust_origin_rotation_arm_stage1_Z = math.radians(90)
        self.adjust_origin_rotation_arm_stage1_X = math.radians(-90)
        
        self.adjust_origin_location_arm_stage1_right = self.adjust_origin_location_arm_base + np.array([-0.098016,0.25,0.094])
        self.adjust_origin_location_arm_gripper = self.adjust_origin_location_arm_base + np.array([-0.05,-0.38,0.06266])

        self.robot_location = np.array([0,0,0])
        self.robot_rotation = 0
        self.robot_arm_angle = 0
        self.robot_arm_distance = 0
        self.robot_turret_angle = 0

        self.vis = visualizer
        self.id = id
        visualizer["robot"+str(id)]["drivetrain"]["mesh"].set_object(models["drivetrain"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))
        visualizer["robot"+str(id)]["drivetrain"]["mesh"].set_transform(meshcat.transformations.translation_matrix(self.adjust_origin_location_drivetrain))

        visualizer["robot"+str(id)]["arm"]["base"]["mesh"].set_object(models["arm base"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["base"]["mesh"].set_transform(meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_base))

        visualizer["robot"+str(id)]["arm"]["left"]["stage1"]["mesh"].set_object(models["arm stage 1"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["left"]["stage1"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_left)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"+str(id)]["arm"]["left"]["stage2"]["mesh"].set_object(models["arm stage 2"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["left"]["stage2"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_left)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"+str(id)]["arm"]["left"]["stage3"]["mesh"].set_object(models["arm stage 3"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["left"]["stage3"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_left)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"+str(id)]["arm"]["right"]["stage1"]["mesh"].set_object(models["arm stage 1"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["right"]["stage1"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_right)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"+str(id)]["arm"]["right"]["stage2"]["mesh"].set_object(models["arm stage 2"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["right"]["stage2"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_right)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"+str(id)]["arm"]["right"]["stage3"]["mesh"].set_object(models["arm stage 3"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["right"]["stage3"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_stage1_right)).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_Z,[0,0,1])).dot(meshcat.transformations.rotation_matrix(self.adjust_origin_rotation_arm_stage1_X,[0,1,0],[0,0,-0.034])))

        visualizer["robot"+str(id)]["arm"]["right"]["gripper"]["mesh"].set_object(models["gripper"],meshcat.geometry.MeshLambertMaterial(color=color,opacity=opacity))    
        visualizer["robot"+str(id)]["arm"]["right"]["gripper"]["mesh"].set_transform((meshcat.transformations.translation_matrix(self.adjust_origin_location_arm_gripper)).dot(meshcat.transformations.rotation_matrix(np.radians(180),[1,0,0])))

    def set_location(self,location):
        self.robot_location = location
        self.vis["robot"+str(self.id)].set_transform(meshcat.transformations.translation_matrix(self.robot_location).dot(meshcat.transformations.rotation_matrix(self.robot_rotation,[0,0,1])))

    def set_rotation(self,degrees):
        self.robot_rotation = math.radians(degrees)
        self.vis["robot"+str(self.id)].set_transform(meshcat.transformations.translation_matrix(self.robot_location).dot(meshcat.transformations.rotation_matrix(self.robot_rotation,[0,0,1])))

    def set_turret_angle(self,degrees):
        self.robot_turret_angle = math.radians(degrees)
        self.vis["robot"+str(self.id)]["arm"].set_transform(meshcat.transformations.rotation_matrix(self.robot_turret_angle,[0,0,1]))

    def set_arm_angle(self,degrees):
        self.robot_arm_angle = math.radians(-degrees)
        self.vis["robot"+str(self.id)]["arm"]["left"].set_transform(meshcat.transformations.rotation_matrix(self.robot_arm_angle,[1,0,0],self.adjust_origin_location_arm_stage1_left + np.array([0,0,-0.034])))
        self.vis["robot"+str(self.id)]["arm"]["right"].set_transform(meshcat.transformations.rotation_matrix(self.robot_arm_angle,[1,0,0],self.adjust_origin_location_arm_stage1_right + np.array([0,0,-0.034])))

    def set_arm_distance(self,distance):
        self.robot_arm_distance = distance
        self.vis["robot"+str(self.id)]["arm"]["left"]["stage2"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance/2,0]))
        self.vis["robot"+str(self.id)]["arm"]["right"]["stage2"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance/2,0]))
        self.vis["robot"+str(self.id)]["arm"]["left"]["stage3"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance,0]))
        self.vis["robot"+str(self.id)]["arm"]["right"]["stage3"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance,0]))
        self.vis["robot"+str(self.id)]["arm"]["right"]["gripper"].set_transform(meshcat.transformations.translation_matrix([0,-self.robot_arm_distance,0]))

    def set_visibility(self,visible = True):
        self.vis["robot"+str(self.id)].set_property("visible",visible)

class Field():
    def __init__(self,visualizer):
        self.vis = visualizer
        # Field should be STL because its easier to load (smaller file size)
        self.field_path = "I:\TomerSoftware\Code\Personal-Code\-1\Simulation\Field\\2023Field.stl"
        visualizer["field"]["mesh"].set_object(
            meshcat.geometry.StlMeshGeometry.from_file(self.field_path),meshcat.geometry.MeshLambertMaterial(color=0x909090))

def Init():
    vis = meshcat.Visualizer()
    vis.open()
    print("Loading Simulation")

    return vis

def move_camera(vis,pos = [0,0,0]):
    vis["/meshcat"].set_transform(meshcat.transformations.translation_matrix([-pos[0],-pos[1],-pos[2]]))