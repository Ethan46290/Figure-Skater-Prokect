from vpython import *
import skater
import math
#
# Assumed Body Constants
#
torso_radius = 0.15
torso_length = 0.50
torso_mass = 50

thigh_length =.4
calf_length =.4
thigh_radius = 0.085
calf_radius = .0607
thigh_spring_constant =7000
calf_spring_constant =7000
leg_mass= 10

leg_spring_constant = 20000
leg_angle = radians(60)


#Arm parameters
brachium_length = .23*1.5
brachium_radius = .04

forearm_length = brachium_length
forearm_radius = .03

arm_length = forearm_length + brachium_length
arm_mass = 5

leg_length = thigh_length+calf_length

body_mass = 80
g = 9.8

#Setting up scene
scene = canvas(title= "Figure Skater Simulation", background = color.white)
figure = skater.Skater(torso_radius=torso_radius, torso_length=torso_length, torso_mass= torso_mass, thigh_length = thigh_length, thigh_radius=thigh_radius, calf_length= calf_length, calf_radius=calf_radius, leg_mass = leg_mass, leg_spring_constant=leg_spring_constant,leg_angle = leg_angle, forearm_length=forearm_length, brachium_length=brachium_length, brachium_radius=brachium_radius, forearm_radius= forearm_radius, arm_mass= arm_mass)
scene.camera.pos = vector(-scene.camera.pos.z, scene.camera.pos.y+1, scene.camera.pos.x)
print(scene.camera.pos)
# scene.camera.pos -= vector(10,0,0)
# print(scene.camera.pos)

scene.camera.axis = (figure.torso.pos - scene.camera.pos)
scene.autoscale = False
scene.range = 6

#ground
ground = box(pos = vector(0,-0.1/2,0), length = 2, width = 100, height = 0.1, color = color.black)

#initial conditions
initial_compression  = vector(0,.3,0)

horizontal_velocity = 7
figure.mom = vector(0,0,horizontal_velocity*body_mass)
figure.squat(initial_compression)
figure.spring_force = vector(0,0,0)

dt = 0.005
t = 0.0

#Some small initial angular momentum generated by the body
figure.angmom = vector(0, 2*math.pi*4*body_mass, 0)
k = 0
controlled_rate = 50

while(True):
    rate(controlled_rate)
    figure.move_body_z(figure.mom/body_mass*dt, range(6))



    if t>10:
        break

# while(True):
#     rate(controlled_rate)
#     t += dt
#
#     #this assumes massless legs
#     gravityforce = body_mass*g*vector(0,-1,0)
#     figure.spring_force = -leg_spring_constant*(figure.left_leg.axis-vector(0,leg_length,0))
#     netforce = gravityforce + figure.spring_force
#
#
#
#     angle_delta = mag(figure.angmom / figure.moi()) * dt
#     figure.rotate_cm(angle_delta)
#
#     figure.mom += netforce*dt
#     pos_delta = (figure.mom/body_mass)*dt
#     figure.move_body_y(pos_delta, range(4))
#     figure.move_body_z(pos_delta, range(6))
#
#     if figure.left_leg.axis.y >= leg_length:
#         if figure.left_leg.pos.y + pos_delta.y <= 0:
#             figure.stretch(pos_delta.y)
#             k = 1
#             print(t)
#         else:
#             figure.move_body_y(pos_delta, (4,5))
#     else:
#         figure.stretch(pos_delta.y)
#         if(pos_delta.y > 0 and k ==1):
#             print(t)
#             break
#
#     if figure.left_leg.pos.y > ground.pos.y:
#         figure.arms_in(arm_length*dt/.1)
#     if k==1:
#         figure.arms_out(-arm_length*dt/.1)
#
#
# while(True):
#     rate(controlled_rate)
#     figure.arms_out(-arm_length*dt/.1)
#     figure.move_body_z(pos_delta, range(6))
#
#     t += dt




