def cyrus_beck_clip(polygon, seg_start, seg_end):
    D = (seg_end[0] - seg_start[0],
         seg_end[1] - seg_start[1])
    signed_area = 0.0
    m = len(polygon)
    for i in range(m):
        x_a, y_a = polygon[i]
        x_b, y_b = polygon[(i + 1) % m] #для замыкания многоугольника
        signed_area += x_a * y_b - x_b * y_a
    orient = 1.0 if signed_area > 0 else -1.0 #для определения по/против чс
    t_lo = 0.0 
    t_hi = 1.0  
    for i in range(m):
        A = polygon[i]                   
        B = polygon[(i + 1) % m]        
        edge = (B[0] - A[0], B[1] - A[1])
        N = (edge[1] * orient, -edge[0] * orient) #нормаль с учетом чс
        denom = N[0] * D[0] + N[1] * D[1]
        numer = N[0] * (A[0] - seg_start[0]) + N[1] * (A[1] - seg_start[1])
        if abs(denom) < 1e-12: #проверка на параллельность
            if numer > 1e-12:
                return None
            continue
        t = numer / denom  
        if denom > 0:
            if t < t_hi: #выходит через грань
                t_hi = t
        else:
            if t > t_lo: #внутри грани
                t_lo = t
        if t_lo > t_hi: #вне многоугольника
            return None
    return t_lo, t_hi
