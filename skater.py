from vpython import *
import math

class Skater:
    def __init__(self, torso_radius, torso_length, torso_mass, torso_angle,thigh_length, thigh_radius, calf_length, calf_radius, leg_spring_constant, leg_mass,brachium_length, brachium_radius, leg_angle, forearm_length, forearm_radius, arm_mass):

        # self.forearm_radius = forearm_radius
        # self.forearm_length = forearm_length
        # self.brachium_radius = brachium_radius
        # self.leg_spring_constant = leg_spring_constant
        # self.brachium_length = brachium_length
        # self.calf_length = calf_length
        # self.thigh_radius = thigh_radius
        # self.thigh_length = thigh_length
        # self.torso_length = torso_length
        self.leg_length = calf_length + thigh_length
        self.leg_angle = leg_angle

        self.leg_length = calf_length + thigh_length
        length = vector(0, self.leg_length, 0)
        self.left_leg = cylinder(pos=vector(-torso_radius / 2, 0, 0), axis=length, radius=thigh_radius, mass = leg_mass,
                                 color=color.red,
                                 ks=leg_spring_constant)
        self.right_leg = cylinder(pos=vector(torso_radius / 2, self.leg_length, 0) + self.leg_length*vector(0, -cos(leg_angle), sin(leg_angle)), axis=self.leg_length * vector(0, cos(leg_angle), -sin(leg_angle)), radius=thigh_radius, mass = leg_mass,
                                  color=color.green,
                                  ks=leg_spring_constant)

        self.head_radius = .1
        self.head_length = .23
        self.head_mass = 4

        # Upper body
        self.torso = cylinder(pos=self.left_leg.axis, axis=torso_length * vector(0, sin(torso_angle), -cos(torso_angle)), radius=torso_radius, mass= torso_mass,color=color.blue)
        self.head = cylinder(pos=self.torso.pos+self.torso.axis, axis=self.head_length * vector(0, sin(torso_angle), -cos(torso_angle)),
                               radius=self.head_radius, color=color.orange, mass = self.head_mass)

        # arms
        # self.left_arm = Arm(pos = self.head.pos + vector(-torso_radius, -brachium_radius, 0), brachium_length= brachium_length, brachium_radius=brachium_radius, forearm_length=forearm_length)
        # self.right_arm = Arm(pos = self.head.pos + vector(torso_radius, -brachium_radius, 0), brachium_length= brachium_length, brachium_radius=brachium_radius, forearm_length=forearm_length)

        self.left_arm = cylinder(pos=self.head.pos + vector(-torso_radius, -brachium_radius, 0), axis=(brachium_length + forearm_length) * vector(-1, 0, 0),
                            radius=brachium_radius, mass = arm_mass,color=color.red)
        self.right_arm = cylinder(pos = self.head.pos + vector(torso_radius, -brachium_radius, 0), axis=(brachium_length + forearm_length) * vector(1, 0, 0),
                            radius=brachium_radius, mass = arm_mass, color=color.yellow)
        self.arm_length = brachium_length + forearm_length
        # self.left_brachium = cylinder(pos=, axis = brachium_length*vector(),radius= brachium_radius, color = color.magenta)
        # self.right_brachium = cylinder(pos=self.head.pos + vector(torso_radius, -brachium_radius, 0), radius= brachium_radius, color = color.red)


        # legs


        self.body_components = [self.head, self.torso, self.left_arm, self.right_arm, self.left_leg, self.right_leg]

    def move_body_y(self, pos_delta, indexes):
        for index, component in enumerate(self.body_components):
            if index in indexes:
                component.pos.y += pos_delta.y

    def move_body_z(self, pos_delta, indexes):
        for index, component in enumerate(self.body_components):
            if index in indexes:
                component.pos.z += pos_delta.z

    def squat(self, compression, index):
        self.body_components[index].axis -= compression
        # self.body_components[5].axis -= compression
        indicies = [0,1,2,3]
        if index == 4:
            indicies += [5]
        else:
            indicies.append(index)
        self.move_body_y(-compression, indicies)


    def  stretch(self, pos_delta, right_leg = False):
        self.body_components[4].axis.y += pos_delta
        if right_leg:
            self.body_components[5].axis.y += pos_delta

    def rotate_cm(self, angle):
        for component in self.body_components:
            component.rotate(axis = vector(0, 1,0), angle = angle, origin = self.torso.pos)

    def moi(self):
        moi = 0
        for component in self.body_components:
            segment_cm = component.pos+component.axis/2
            r = mag(cross(self.torso.pos - segment_cm,self.torso.axis))/mag(self.torso.axis)


            moi += component.mass * r**2
        return moi

    def arms_in(self, length):
        if mag(self.body_components[2].axis)  > 0.1:
            self.body_components[2].axis -= length * norm(self.body_components[2].axis)
            self.body_components[3].axis -= length * norm(self.body_components[3].axis)

    def arms_out(self, length):
        if mag(self.body_components[2].axis) < self.arm_length:
            self.body_components[2].axis -= length * norm(self.body_components[2].axis)
            self.body_components[3].axis -= length * norm(self.body_components[3].axis)

    def prerotate(self, angle):
        for index, component in enumerate(self.body_components):
            if index < 4:
                component.rotate(axis = self.torso.axis, angle = angle, origin = self.torso.pos)

    def straighten(self, angle, amount = 0):
        rotation_axis = (self.left_leg.pos+self.left_leg.axis) -self.torso.pos
        # self.torso.rotate(axis = rotation_axis, angle = -angle, origin = self.torso.pos)
        for index, component in enumerate(self.body_components):
            if not index == 4:
                component.rotate(axis = rotation_axis, angle = -angle, origin = self.torso.pos)
        if self.right_leg.pos.y <=0:
            self.jump(vector(0,amount,0))

    def jump(self, height):
        if(mag(self.left_leg.axis) <= self.leg_length):
            self.left_leg.axis += height
        else:
            self.left_leg.pos += height
        for index, component in enumerate(self.body_components):
            if not index == 4:
                component.pos += height

    def straight(self):
        return (dot(self.torso.axis, vector(0, 0, -1))) <=  0.001

    def leg_theta(self):
        return self.leg_angle - self.leg_theta_orth()

    def leg_theta_orth(self):
        return math.acos(mag(self.left_leg.axis)/mag(self.right_leg.axis))