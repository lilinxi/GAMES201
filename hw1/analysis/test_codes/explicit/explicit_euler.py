# author: g1n0st
# Symplectic Euler Method for Mass-Spring System
import sys
sys.path.append('../')
from mass_spring_framework import *

new_v = ti.Vector(2, dt = ti.f32, shape = max_particles)

@ti.kernel
def substep():
    # compute force and new velocity
    n = num_particles[None]
    for i in range(n):
        v[i] = new_v[i]
        new_v[i] *= ti.exp(-dt * damping[None]) # damping
        total_force = ti.Vector(gravity) * particle_mass
        for j in range(n):
            if rest_length[i, j] != 0:
                x_ij = x[i] - x[j]
                total_force += -stiffness[None] * (x_ij.norm() - rest_length[i, j]) * x_ij.normalized()
        new_v[i] += dt * total_force / particle_mass

    collide_with_ground()
    update_position()

init_mass_spring_system()

for frame in range(660):
    process_input(frame)

    if not paused[None]:
        for step in range(10):
            substep()

    process_output(frame)
