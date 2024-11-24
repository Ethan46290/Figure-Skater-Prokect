from vpython import *
import skater
#
# Assumed Body Constants
#
torso_radius = 0.15
torso_length = 0.50

thigh_length =.4
calf_length =.4
thigh_radius = 0.085
calf_radius = .0607
thigh_spring_constant =7000
calf_spring_constant =7000

leg_spring_constant = 14000

#Arm parameters
brachium_length = .23*1.5
brachium_radius = .04

forearm_length = brachium_length
forearm_radius = .03

leg_length = thigh_length+calf_length

body_mass = 80
g = 9.8

#
scene = canvas(title= "Figure Skater Simulation", background = color.white)
figure = skater.Skater(torso_radius=torso_radius, torso_length=torso_length, thigh_length= thigh_length, thigh_radius=thigh_radius, calf_length= calf_length, calf_radius=calf_radius, leg_spring_constant=leg_spring_constant,forearm_length=forearm_length, brachium_length=brachium_length, brachium_radius=brachium_radius, forearm_radius= forearm_radius)
scene.camera.pos = vector(-scene.camera.pos.z, scene.camera.pos.y+1, scene.camera.pos.x)
scene.camera.axis = (figure.torso.pos - scene.camera.pos)
scene.autoscale = False
scene.range = 5

#making lower body
# left_calf = cylinder(pos = vector(-torso_radius/2,0,0), axis = vector(0,calf_length,0), radius = calf_radius, color = color.green)
# left_thigh = cylinder(pos = vector(left_calf.pos + vector(0,calf_length,0)), axis = vector(0,thigh_length,0), radius  = thigh_radius, color = color.red)
#
# right_calf = cylinder(pos = vector(torso_radius/2,0,0), axis = vector(0,calf_length,0), radius = calf_radius, color = color.green)
# right_thigh = cylinder(pos = vector(right_calf.pos + vector(0,calf_length,0)), axis = vector(0,thigh_length,0), radius  = thigh_radius, color = color.red)

#ground
ground = box(pos = vector(0,-0.1/2,0), length = 2, width = 100, height = 0.1, color = color.black)






#initial stretch

initial_compression  = vector(0,.3,0)

horizontal_velocity = 7
figure.mom = vector(0,0,horizontal_velocity*body_mass)
figure.squat(initial_compression)
figure.spring_force = vector(0,0,0)

dt = 0.005
t = 0.0
while(True):
    rate(50)
    t += dt

    #this assumes massless legs
    gravityforce = body_mass*g*vector(0,-1,0)

    figure.spring_force = -leg_spring_constant*(figure.left_leg.axis-vector(0,leg_length,0))
    netforce = gravityforce + figure.spring_force
    # netforce = vector(0,0,0)
    figure.mom += netforce*dt
    pos_delta = (figure.mom/body_mass)*dt
    figure.move_body_y(pos_delta, range(4))
    figure.move_body_z(pos_delta, range(6))

    if figure.left_leg.axis.y >= leg_length:
        if figure.left_leg.pos.y + pos_delta.y <= 0:
            figure.stretch(pos_delta.y)
        else:
            figure.move_body_y(pos_delta, (4,5))
    else:
        figure.stretch(pos_delta.y)










    # if mag(skater.left_leg.axis) < leg_length:
    #     skater.stretch(pos_delta)
    #     if skater.left_leg.axis + pos_delta > leg_length:
    # else:
    #     if skater.left_leg.pos.y + pos_delta.y <0:
    #         skater.left_leg.pos.y = 0
    #         skater.right_leg.pos.y= 0
    #         skater.stretch(pos_delta)
    #     else:
    #         skater.move_body(pos_delta, (4, 5))

    if(t >10):
        break




