def detect_collision(points, target_rect):
    for pt in points:
        if target_rect.collidepoint(pt):
            return True
    return False
