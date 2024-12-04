from operator import truediv

from numpy.ma.core import angle
from vpython import *
import skater
import math
#
# Assumed Body Constants
#

#torso
torso_radius = 0.225
torso_length = 0.525
torso_mass = 35.4
#measured from the vertical
torso_angle = radians(30)

#leg
thigh_length =.45
calf_length =.432
thigh_radius = 0.088
calf_radius = .0617
thigh_spring_constant =7000
calf_spring_constant =7000
leg_mass= 9.888
leg_length = thigh_length+calf_length
leg_spring_constant = 20000
#measured from the vertical
leg_angle = radians(90) - torso_angle



#Arm parameters
brachium_length = .34
brachium_radius = .061

forearm_length = .36
forearm_radius = .035

arm_length = forearm_length + brachium_length
arm_mass = 3.32


leg_strength = 2000
torque = vector(0,203,0)


# other parameters
body_mass = 65.2
g = 9.8
t_jump = 0.6

prerotation_angle = radians(-90)

#Setting up scene
scene = canvas(title= "Figure Skater Simulation", background = color.white)
figure = skater.Skater(torso_radius=torso_radius, torso_length=torso_length, torso_mass= torso_mass, torso_angle = torso_angle, thigh_length=thigh_length, thigh_radius = thigh_radius, calf_length= calf_length, calf_radius=calf_radius, leg_mass = leg_mass, leg_spring_constant=leg_spring_constant,leg_angle = leg_angle, forearm_length=forearm_length, brachium_length=brachium_length, brachium_radius=brachium_radius, forearm_radius= forearm_radius, arm_mass= arm_mass)
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
figure.squat(initial_compression, 4)
figure.spring_force = vector(0,0,0)
figure.prerotate(prerotation_angle)


dt = 0.005
t = 0.0

#Some small initial angular momentum generated by the body
figure.angmom = vector(0, 0, 0)
k = 0
controlled_rate = 10

angle_tot = 0
straightened_tot = 0



# angle between leg in the air and leg at first contact in ground
theta = figure.leg_theta()

#angle between leg in first contact in ground and left leg
theta_orth = figure.leg_theta_orth()
t_1 = 0


while(True):
    rate(controlled_rate)
    figure.move_body_z(figure.mom/body_mass*dt, range(6))
    t += dt
    figure.angmom += torque*dt
    angle_delta = mag(figure.angmom / figure.moi()) * dt


    if not figure.straight() and t > 0.2:
        figure.prerotate(angle_delta)

        angle_tot += angle_delta

        needed_omega = theta * angle_delta / -prerotation_angle
        # delta_omega = needed_omega - straightened_tot
        figure.straighten(needed_omega)
        # straightened_tot = needed_omega

    if angle_tot >= -prerotation_angle - 0.1:
        t_1 = t
        break

p = 0
while(True):
    rate(controlled_rate)
    t += dt

    #this assumes massless legs
    gravityforce = body_mass*g*vector(0,-1,0)
    # figure.spring_force = -leg_spring_constant*(figure.left_leg.axis-vector(0,leg_length,0))
    ground_reaction_force = leg_strength*(1-(t-t_1)/t_jump)   *vector(0,1,0)
    if (t-t_1)>t_jump or figure.left_leg.pos.y > 0:
        ground_reaction_force = vector(0,0,0)

    netforce = gravityforce + ground_reaction_force

    if(not mag(ground_reaction_force) == 0):
        figure.angmom += torque*dt


    figure.mom += netforce*dt
    pos_delta = (figure.mom/body_mass)*dt

    figure.move_body_z(pos_delta, range(6))

    angle_delta = mag(figure.angmom / figure.moi()) * dt
    figure.rotate_cm(angle_delta)

    if not figure.straight() and p ==0:
        # figure.prerotate(angle_delta)

        angle_tot += angle_delta

        needed_omega = theta_orth * angle_delta / -prerotation_angle
        # delta_omega = needed_omega - straightened_tot
        figure.straighten(needed_omega, pos_delta.y)
        # figure.stretch(pos_delta.y)
        # straightened_tot = needed_omega


    else:
        p = 1
        figure.move_body_y(pos_delta, range(4))
        figure.move_body_y(pos_delta, [5])


        if figure.left_leg.axis.y >= leg_length:
            if figure.left_leg.pos.y + pos_delta.y <= 0:
                figure.stretch(pos_delta.y, True)
                k = 1
                print(t)
            else:
                figure.move_body_y(pos_delta, [4])
        else:
            figure.stretch(pos_delta.y)
            if pos_delta.y > 0 and k ==1:
                print(t)
                break

    if figure.left_leg.pos.y > 0:
        figure.arms_in(arm_length*dt/.1)
    if k==1:
        figure.arms_out(-arm_length*dt/.1)





