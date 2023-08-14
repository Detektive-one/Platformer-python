# properties/gravity.py



def apply_gravity(obj, gravity, max_fall_speed):
    obj.y_velocity += gravity
    if obj.y_velocity > max_fall_speed:
        obj.y_velocity = max_fall_speed

    obj.rect.y += obj.y_velocity
