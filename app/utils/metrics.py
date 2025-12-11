metrics = {
    "total_creates": 0,
    "total_collisions": 0,
}

def increment_creates():
    metrics["total_creates"] +=1

def increment_collisions():
    metrics["total_collisions"] +=1

def get_metrics():
    collision_rate = 0.0
    if metrics["total_creates"] > 0:
        collision_rate = metrics["total_collisions"]/ metrics["total_creates"]

    return {
        "total_creates": metrics["total_creates"],
        "total_collisions": metrics["total_collisions"],
        "collision_rate": round(collision_rate,4),
    }


def reset_metrics():
    metrics["total_creates"] = 0
    metrics["total_collisions"] = 0
