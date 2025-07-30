init:

    python:
    
        import math

        class Shaker(object):
        
            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }
        
            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                #
                self.start = [ self.anchors.get(i, i) for i in start ]  # central position
                self.dist = dist    # maximum distance, in pixels, from the starting point
                self.child = child
                
            def __call__(self, t, sizes):
                # Float to integer... turns floating point numbers to
                # integers.                
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x

                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

                xpos = xpos - xanchor
                ypos = ypos - yanchor
                
                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

                return (int(nx), int(ny), 0, 0)
        
        def _Shake(start, time, child=None, dist=100.0, **properties):

            move = Shaker(start, child, dist=dist)
        
            return renpy.display.layout.Motion(move, time, child, add_sizes=True, **properties)

        Shake = renpy.curry(_Shake)
    $ sshake = Shake((0, 0, 0, 0), 1.0, dist=15)
init:
    transform flip:
        xzoom -1.0
    transform bounce:
        ease .05 yoffset 20
        ease .05 yoffset -20
        ease .03 yoffset 12
        ease .03 yoffset -12
        ease .01 yoffset 4
        ease .01 yoffset -4
        ease .01 yoffset 0

        
        
    python hide:
        def quad_time_warp(x):
            return -2.0 * x**3 + 3.0 * x**2
        
        def quad_in_time_warp(x):
            return 1.0 - (1.0 - x)**2
        
        def quad_out_time_warp(x):
            return x**2
        
        define.move_transitions("quad", 1.0, quad_time_warp, quad_in_time_warp, quad_out_time_warp)