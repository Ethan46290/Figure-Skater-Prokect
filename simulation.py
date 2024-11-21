from email.quoprimime import body_length

from vpython import *
#
# Assumed Body Constants
#
head_radius = .1
head_length = .23

torso_radius = 0.15
torso_length = 0.50

thigh_length =.42
calf_length =.447
thigh_radius = 0.085
calf_radius = .0607
thigh_spring_constant =7000
calf_spring_constant =7000
#
scene = canvas(title= "Figure Skater Simulation", background = color.white)

#making lower body
left_calf = cylinder(pos = vector(-torso_radius/2,0,0), axis = vector(0,calf_length,0), radius = calf_radius, color = color.green)
left_thigh = cylinder(pos = vector(left_calf.pos + vector(0,calf_length,0)), axis = vector(0,thigh_length,0), radius  = thigh_radius, color = color.red)

right_calf = cylinder(pos = vector(torso_radius/2,0,0), axis = vector(0,calf_length,0), radius = calf_radius, color = color.green)
right_thigh = cylinder(pos = vector(right_calf.pos + vector(0,calf_length,0)), axis = vector(0,thigh_length,0), radius  = thigh_radius, color = color.red)

#Upper body
torso = cylinder(pos = vector(0,left_thigh.pos.y+thigh_length,0), axis = vector(0,torso_length,0), radius = torso_radius, color = color.blue)

skater_head = cylinder(pos = vector(0,torso_length +torso.pos.y,0), axis = vector(0,head_length,0), radius = head_radius, color = color.black)


