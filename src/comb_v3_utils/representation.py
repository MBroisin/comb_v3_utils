import numpy
import cv2
import json
import os

__size_i = 0
__size_j = 0
__resolution = 0
__offset_x = 0
__offset_y = 0

def __convert_to_image_coordinates(x, y, max_x, max_y):
    new_j = max_y - y
    new_i = x
    return new_i, new_j

def convert_to_image_coordinates(x, y):
    """
    This function converts x,y coordinates of the frame (origin bottom-left corner, excluding the ear)
    to image coordinates (origin top-left corner taking the ear into account)
    :param x: x coordinate to be converted
    :param y: y coordinate to be converted
    :return: (i, j) the new coordinates to apply to the image
    """
    i = int( (x + __offset_x) / __resolution)
    j = int( (y + __offset_y) / __resolution)
    new_i, new_j = __convert_to_image_coordinates(i, j, __size_i, __size_j)
    return new_i, new_j


def get_frame_layout(resolution=0.1, padding=0, show_outline=True, show_comb_outline=True, show_screws=True, show_grooves=True, show_actuators=True, show_accelerometers=True, show_vleds=True, show_irleds=True, display_names=True, show_cells=False):
    try :
        package_path = os.path.dirname(__file__)
        f = open(package_path + '/frame_layout.json', "r")
        config = json.load(f)
        f.close()
    except :
        print('No layout provided. Quitting')
        return None
    img = _draw_frame_layout(
        config,
        resolution=resolution,
        padding=padding,
        show_outline=show_outline,
        show_comb_outline=show_comb_outline, 
        show_screws=show_screws, 
        show_grooves=show_grooves, 
        show_actuators=show_actuators, 
        show_accelerometers=show_accelerometers, 
        show_vleds=show_vleds, 
        show_irleds=show_irleds, 
        display_names=display_names,
        show_cells=show_cells
    )
    return img

def get_accelerometers_specifics():
    try :
        package_path = os.path.dirname(__file__)
        f = open(package_path + '/frame_layout.json', "r")
        config = json.load(f)
        f.close()
    except :
        print('No layout provided. Quitting')
        return None
    return config['accelerometers']

def get_actuators_specifics():
    try :
        package_path = os.path.dirname(__file__)
        f = open(package_path + '/frame_layout.json', "r")
        config = json.load(f)
        f.close()
    except :
        print('No layout provided. Quitting')
        return None
    return config['actuators']

def get_leds_specifics():
    try :
        package_path = os.path.dirname(__file__)
        f = open(package_path + '/frame_layout.json', "r")
        config = json.load(f)
        f.close()
    except :
        print('No layout provided. Quitting')
        return None
    return {'vleds' : config['led_red'], 'irleds' : config['led_ir']} 

def _draw_frame_layout(layout, resolution=0.1, padding=0, show_outline=True, show_comb_outline=True, show_screws=True, show_grooves=True, show_actuators=True, show_accelerometers=True, show_vleds=True, show_irleds=True, display_names=True, show_cells=False):

    CV2_FILLED_SHAPE        = -1
    LINES_THICKNESS         = 3

    OUTLINE_COLOR           = (255, 255, 255)
    OUTLINE_THICKNESS       = LINES_THICKNESS

    SCREW_COLOR             = (128, 128, 128)
    SCREW_THICKNESS         = CV2_FILLED_SHAPE

    GROOVE_COLOR            = (0, 0, 255)
    GROOVE_THICKNESS        = CV2_FILLED_SHAPE

    ACTUATOR_COLOR          = (255, 255, 0)
    ACTUATOR_THICKNESS      = LINES_THICKNESS

    ACCELEROMETER_COLOR     = (0, 255, 0)
    ACCELEROMETER_THICKNESS = CV2_FILLED_SHAPE

    VLEDS_COLOR             = (255, 0, 0)
    VLEDS_THICKNESS         = CV2_FILLED_SHAPE

    IRLEDS_COLOR            = (180, 0, 200)
    IRLEDS_THICKNESS        = CV2_FILLED_SHAPE

    CELLS_COLOR            = (128, 128, 128)
    CELLS_THICKNESS        = 1
    CELLS_RADIUS           = int( 5 / resolution / 2)
    CELLS_H_PITCH          = int( 6 / resolution )
    CELLS_V_PITCH          = int( 5.2 / resolution )
    CELLS_H_SHIFT          = int( 3 / resolution )

    TEXT_SIZE               = 2
    TEXT_THICKNESS          = 1

    # Outer image size
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for outline_pt in layout['outline']:
        min_x = min(min_x, outline_pt['pos'][0])
        min_y = min(min_y, outline_pt['pos'][1])
        max_x = max(max_x, outline_pt['pos'][0])
        max_y = max(max_y, outline_pt['pos'][1])

    MARGIN_SIZE = 4
    HALF_MARGIN = int( MARGIN_SIZE / 2 )

    offset_x = -min_x + HALF_MARGIN
    offset_y = -min_y + HALF_MARGIN

    size_x = max_x - min_x + MARGIN_SIZE
    size_y = max_y - min_y + MARGIN_SIZE
    
    size_i = int( size_x / resolution )
    size_j = int( size_y / resolution )
    frame_image = numpy.zeros((size_j, size_i, 3), dtype=numpy.uint8)

    # Screws
    if show_screws:
        for screw in layout['screws']:
            # fetch physical coordinates
            coord_x = screw['pos'][0] + offset_x
            coord_y = screw['pos'][1] + offset_y
            radius  = screw['radius']

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution ) 
            radius  = int( radius  / resolution / 2) 
            
            coord_x, coord_y = __convert_to_image_coordinates(coord_x, coord_y, size_i, size_j)
            frame_image = cv2.circle(frame_image, (coord_x,coord_y), radius, SCREW_COLOR, SCREW_THICKNESS)

    # IR leds
    if show_irleds:
        for irled in layout['led_ir']:
            # fetch physical coordinates
            coord_x = irled['pos'][0] + offset_x
            coord_y = irled['pos'][1] + offset_y
            radius  = irled['radius']

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution ) 
            radius  = int( radius  / resolution / 2) 
            
            coord_x, coord_y = __convert_to_image_coordinates(coord_x, coord_y, size_i, size_j)
            frame_image = cv2.circle(frame_image, (coord_x,coord_y), radius, IRLEDS_COLOR, IRLEDS_THICKNESS)
            if display_names:
                frame_image = cv2.putText(frame_image,'IR{}'.format(irled['id']), (coord_x,coord_y-int(1.5*radius)), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, IRLEDS_COLOR, TEXT_THICKNESS, cv2.LINE_AA)


    # Visible leds
    if show_vleds:
        for vled in layout['led_red']:
            # fetch physical coordinates
            coord_x = vled['pos'][0] + offset_x
            coord_y = vled['pos'][1] + offset_y
            width   = vled['wh'][0]
            height  = vled['wh'][1]

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution ) 
            width   = int( width   / resolution / 2 ) 
            height  = int( height  / resolution / 2 ) 

            coord2_x, coord2_y = __convert_to_image_coordinates(coord_x + width, coord_y + height, size_i, size_j)
            coord_x, coord_y = __convert_to_image_coordinates(coord_x - width, coord_y - height, size_i, size_j)
            frame_image = cv2.rectangle(frame_image, (coord_x,coord_y), (coord2_x,coord2_y), VLEDS_COLOR, VLEDS_THICKNESS)
            if display_names:
                frame_image = cv2.putText(frame_image,'D{}'.format(vled['id']), (coord_x,coord_y-3*height), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, VLEDS_COLOR, TEXT_THICKNESS, cv2.LINE_AA)

    # Grooves
    if show_grooves:
        for groove in layout['grooves']:
            # fetch physical coordinates
            coord_x = groove['pos'][0] + offset_x
            coord_y = groove['pos'][1] + offset_y
            width  = groove['wh'][0]
            height  = groove['wh'][1]

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution ) 
            width   = int( width   / resolution ) 
            height  = int( height  / resolution ) 

            coord2_x, coord2_y = __convert_to_image_coordinates(coord_x + width, coord_y + height, size_i, size_j)
            coord_x, coord_y = __convert_to_image_coordinates(coord_x, coord_y, size_i, size_j)
            frame_image = cv2.rectangle(frame_image, (coord_x,coord_y), (coord2_x,coord2_y), GROOVE_COLOR, GROOVE_THICKNESS)

    # Actuators
    if show_actuators:
        for act in layout['actuators']:
            # fetch physical coordinates
            coord_x = act['pos'][0] + offset_x
            coord_y = act['pos'][1] + offset_y
            radius  = act['radius']

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution ) 
            radius  = int( radius  / resolution / 2 ) 

            coord_x, coord_y = __convert_to_image_coordinates(coord_x, coord_y, size_i, size_j)
            frame_image = cv2.circle(frame_image, (coord_x,coord_y), radius, ACTUATOR_COLOR, ACTUATOR_THICKNESS)
            if display_names:
                frame_image = cv2.putText(frame_image,'A{}'.format(act['id']), (coord_x-int(radius/2),coord_y-int(radius/2)), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, ACTUATOR_COLOR, TEXT_THICKNESS, cv2.LINE_AA)
    
    # Accelererometers
    if show_accelerometers:
        for acc in layout['accelerometers']:
            # fetch physical coordinates
            coord_x = acc['pos'][0] + offset_x
            coord_y = acc['pos'][1] + offset_y
            width  = acc['wh'][0]
            height  = acc['wh'][1]

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution ) 
            width   = int( width   / resolution / 2 ) 
            height  = int( height  / resolution / 2 ) 

            coord2_x, coord2_y = __convert_to_image_coordinates(coord_x + width, coord_y + height, size_i, size_j)
            coord_x, coord_y = __convert_to_image_coordinates(coord_x - width, coord_y - height, size_i, size_j)
            frame_image = cv2.rectangle(frame_image, (coord_x,coord_y), (coord2_x,coord2_y), ACCELEROMETER_COLOR, ACCELEROMETER_THICKNESS)
            if display_names:
                frame_image = cv2.putText(frame_image,'Acc{}'.format(acc['id']), (coord_x+3*width,coord_y+3*height), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SIZE, ACCELEROMETER_COLOR, TEXT_THICKNESS, cv2.LINE_AA)

    # Outline
    if show_outline:
        outline_vertices = []
        vertices_index = []
        for outline_pt in layout['outline']:
            # fetch physical coordinates
            coord_x = outline_pt['pos'][0] + offset_x
            coord_y = outline_pt['pos'][1] + offset_y

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution )

            outline_vertices.append([coord_x, coord_y])
            vertices_index.append(outline_pt['id'])
        
        outline_vertices = [__convert_to_image_coordinates(vert[0], vert[1], size_i, size_j) for _,vert in sorted(zip(vertices_index,outline_vertices))]
        outline_vertices = numpy.array(outline_vertices).reshape((-1, 1, 2))
        frame_image = cv2.polylines(frame_image,[outline_vertices], True, OUTLINE_COLOR, OUTLINE_THICKNESS)

    # Outline of the comb
    if show_comb_outline:
        comb_outline_vertices = []
        vertices_index = []
        for outline_pt in layout['outline_comb']:
            # fetch physical coordinates
            coord_x = outline_pt['pos'][0] + offset_x
            coord_y = outline_pt['pos'][1] + offset_y

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution )

            comb_outline_vertices.append([coord_x, coord_y])
            vertices_index.append(outline_pt['id'])
        
        comb_outline_vertices = [__convert_to_image_coordinates(vert[0], vert[1], size_i, size_j) for _,vert in sorted(zip(vertices_index,comb_outline_vertices))]
        comb_outline_vertices = numpy.array(comb_outline_vertices).reshape((-1, 1, 2))
        frame_image = cv2.polylines(frame_image,[comb_outline_vertices], True, OUTLINE_COLOR, OUTLINE_THICKNESS)

    # Cells
    if show_cells:
        for acc in layout['accelerometers']:
            if acc['id'] in [5,7]:
                continue
            # fetch physical coordinates
            coord_x = acc['pos'][0] + offset_x
            coord_y = acc['pos'][1] + offset_y

            # Apply resolution factor and transformation
            coord_x = int( coord_x / resolution )
            coord_y = int( coord_y / resolution )
            coord_x, coord_y = __convert_to_image_coordinates(coord_x, coord_y, size_i, size_j)

            CELLS_HORIZONTAL_NUMBER = 7
            CELLS_VERTICAL_NUMBER = 9
            for i in range(CELLS_HORIZONTAL_NUMBER+1):
                for j in range(CELLS_VERTICAL_NUMBER+1):
                    frame_image = cv2.circle(frame_image, (coord_x+CELLS_H_PITCH*i+CELLS_H_SHIFT*(j%2),coord_y+CELLS_V_PITCH*j), CELLS_RADIUS, CELLS_COLOR, CELLS_THICKNESS)
                    frame_image = cv2.circle(frame_image, (coord_x+CELLS_H_PITCH*i+CELLS_H_SHIFT*(j%2),coord_y-CELLS_V_PITCH*j), CELLS_RADIUS, CELLS_COLOR, CELLS_THICKNESS)
                    frame_image = cv2.circle(frame_image, (coord_x-CELLS_H_PITCH*i+CELLS_H_SHIFT*(j%2),coord_y+CELLS_V_PITCH*j), CELLS_RADIUS, CELLS_COLOR, CELLS_THICKNESS)
                    frame_image = cv2.circle(frame_image, (coord_x-CELLS_H_PITCH*i+CELLS_H_SHIFT*(j%2),coord_y-CELLS_V_PITCH*j), CELLS_RADIUS, CELLS_COLOR, CELLS_THICKNESS)


    # Padding of the image to see the outline
    padding = int( padding / resolution )
    frame_image = numpy.pad(frame_image, ((padding, padding),(padding, padding),(0,0)))
    
    global __size_i, __size_j, __resolution, __offset_x, __offset_y
    __size_i = size_i
    __size_j = size_j
    __resolution = resolution
    __offset_x = offset_x
    __offset_y = offset_y
    return frame_image
