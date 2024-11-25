from vpython import *
import math

class Skater:
    def __init__(self, torso_radius, torso_length, torso_mass, thigh_length, thigh_radius, calf_length, calf_radius, leg_spring_constant, leg_mass,brachium_length, brachium_radius, forearm_length, forearm_radius, arm_mass):

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
        length = vector(0, self.leg_length, 0)
        self.left_leg = cylinder(pos=vector(-torso_radius / 2, 0, 0), axis=length, radius=thigh_radius, mass = leg_mass,
                                 color=color.green,
                                 ks=leg_spring_constant)
        self.right_leg = cylinder(pos=vector(torso_radius / 2, 0, 0), axis=length, radius=thigh_radius, mass = leg_mass,
                                  color=color.green,
                                  ks=leg_spring_constant)

        self.head_radius = .1
        self.head_length = .23
        self.head_mass = 4

        # Upper body
        self.torso = cylinder(pos=self.left_leg.axis, axis=vector(0, torso_length, 0), radius=torso_radius, mass= torso_mass,color=color.blue)
        self.head = cylinder(pos=self.torso.pos+self.torso.axis, axis=vector(0, self.head_length, 0),
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

    def squat(self, compression):
        self.body_components[4].axis -= compression
        self.body_components[5].axis -= compression
        self.move_body_y(-compression, range(4))

    def  stretch(self, pos_delta):
        self.body_components[4].axis.y += pos_delta
        self.body_components[5].axis.y += pos_delta

    def rotate_cm(self, angle):
        for component in self.body_components:
            component.rotate(axis = self.torso.axis, angle = angle, origin = self.torso.pos)

    def moi(self):
        moi = 0
        for component in self.body_components:
            moi += component.mass * (component.pos+component.axis/2).y - self.torso.pos.y**2
        return moi

    def arms_in(self, length):
        if mag(self.body_components[2].axis)  > 0:
            self.body_components[2].axis -= length * norm(self.body_components[2].axis)
            self.body_components[3].axis -= length * norm(self.body_components[3].axis)

    def arms_out(self, length):
        if mag(self.body_components[2].axis) < self.arm_length:
            self.body_components[2].axis -= length * norm(self.body_components[2].axis)
            self.body_components[3].axis -= length * norm(self.body_components[3].axis)

# class Arm:
#     def __init__(self, pos, brachium_length, brachium_radius, forearm_length):
#         self.pos = pos
#



# , forearm_radius, brachium_theta, brachium_phi, forearm_theta, forearm_phi

