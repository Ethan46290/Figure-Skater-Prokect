from email.quoprimime import body_length

from vpython import *
#
# Assumed Body Constants
#
head_radius = .1
head_length = .23

torso_radius = 0.15
torso_length = 0.50

thigh_length =.4
calf_length =.4
thigh_radius = 0.085
calf_radius = .0607
thigh_spring_constant =7000
calf_spring_constant =7000

leg_spring_constant = 14000

body_mass = 80
g = 9.8

leg_length = thigh_length+calf_length
#
scene = canvas(title= "Figure Skater Simulation", background = color.white)

#making lower body
# left_calf = cylinder(pos = vector(-torso_radius/2,0,0), axis = vector(0,calf_length,0), radius = calf_radius, color = color.green)
# left_thigh = cylinder(pos = vector(left_calf.pos + vector(0,calf_length,0)), axis = vector(0,thigh_length,0), radius  = thigh_radius, color = color.red)
#
# right_calf = cylinder(pos = vector(torso_radius/2,0,0), axis = vector(0,calf_length,0), radius = calf_radius, color = color.green)
# right_thigh = cylinder(pos = vector(right_calf.pos + vector(0,calf_length,0)), axis = vector(0,thigh_length,0), radius  = thigh_radius, color = color.red)

#ground
ground = box(pos = vector(0,-0.1/2,0), length = 2, width = 2, height = 0.1, color = color.black)


length = vector(0,leg_length,0)
#Upper body
torso = cylinder(pos = length, axis = vector(0,torso_length,0), radius = torso_radius, color = color.blue)
skater_head = cylinder(pos = torso.pos+vector(0,torso_length,0), axis = vector(0,head_length,0), radius = head_radius, color = color.orange)
left_leg = cylinder(pos=vector(-torso_radius/2,0,0),axis = torso.pos, radius=thigh_radius, color=color.green, ks = leg_spring_constant)
right_leg = cylinder(pos=vector(torso_radius/2,0,0),axis = torso.pos, radius=thigh_radius, color=color.green, ks = leg_spring_constant)

#initial stretch

initial_compression  = .3
torso.pos.y = length.y - initial_compression
skater_head.pos.y = torso.pos.y + torso_length
# initial momentum = 0
torso.mom = vector(0,0,0)

dt = 0.0005
t = 0.0
while(True):
    rate(100)
    t += dt

    #this assumes massless legs
    gravityforce = body_mass*g*vector(0,-1,0)

    cylinder.force = -left_leg.ks*(torso.pos-length)
    netforce = gravityforce + cylinder.force

    torso.mom += netforce*dt
    torso.pos += (torso.mom/body_mass)*dt
    skater_head.pos += (torso.mom/body_mass)*dt

    if(torso.pos.y > length.y):
        left_leg.pos += (torso.mom/body_mass)*dt
        right_leg.pos += (torso.mom / body_mass) * dt

    left_leg.axis = torso.pos
    right_leg.axis = torso.pos

