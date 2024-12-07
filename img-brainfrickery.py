from PIL import Image
import cv2
import sys
from math import sqrt
import time
import os
import subprocess
import platform
if platform.system() == 'Windows':
    from winsound import PlaySound, SND_FILENAME
    import threading
else:
    from playsound import playsound
from _brainfrick.lib import interpret_code, init_bf, end_bf, init_display, set_frame_size
import atexit
import multiprocessing
import pathlib
atexit.register(end_bf)

ascii_luminosity_chars =  r" `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
ascii_luminosity_vals = [0, 0.0751, 0.0829, 0.0848, 0.1227, 0.1403, 0.1559, 0.185, 0.2183, 0.2417, 0.2571, 0.2852, 0.2902, 0.2919, 0.3099, 0.3192, 0.3232, 0.3294, 0.3384, 0.3609, 0.3619, 0.3667, 0.3737, 0.3747, 0.3838, 0.3921, 0.396, 0.3984, 0.3993, 0.4075, 0.4091, 0.4101, 0.42, 0.423, 0.4247, 0.4274, 0.4293, 0.4328, 0.4382, 0.4385, 0.442, 0.4473, 0.4477, 0.4503, 0.4562, 0.458, 0.461, 0.4638, 0.4667, 0.4686, 0.4693, 0.4703, 0.4833, 0.4881, 0.4944, 0.4953, 0.4992, 0.5509, 0.5567, 0.5569, 0.5591, 0.5602, 0.5602, 0.565, 0.5776, 0.5777, 0.5818, 0.587, 0.5972, 0.5999, 0.6043, 0.6049, 0.6093, 0.6099, 0.6465, 0.6561, 0.6595, 0.6631, 0.6714, 0.6759, 0.6809, 0.6816, 0.6925, 0.7039, 0.7086, 0.7235, 0.7302, 0.7332, 0.7602, 0.7834, 0.8037, 0.9999]

squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]
factors = dict({
        0: [0],
        1: [1],
        2: [1, 2],        
        3: [1, 3],        
        4: [1, 2, 4],     
        5: [1, 5],        
        6: [1, 2, 3, 6],  
        7: [1, 7],        
        8: [1, 2, 4, 8],  
        9: [1, 3, 9],     
        10: [1, 2, 5, 10],
        11: [1, 11],      
        12: [1, 2, 3, 4, 6, 12],
        13: [1, 13],
        14: [1, 2, 7, 14],
        15: [1, 3, 5, 15],
        16: [1, 2, 4, 8, 16],
        17: [1, 17],
        18: [1, 2, 3, 6, 9, 18],
        19: [1, 19],
        20: [1, 2, 4, 5, 10, 20],
        21: [1, 3, 7, 21],
        22: [1, 2, 11, 22],
        23: [1, 23],
        24: [1, 2, 3, 4, 6, 8, 12, 24],
        25: [1, 5, 25],
        26: [1, 2, 13, 26],
        27: [1, 3, 9, 27],
        28: [1, 2, 4, 7, 14, 28],
        29: [1, 29],
        30: [1, 2, 3, 5, 6, 10, 15, 30],
        31: [1, 31],
        32: [1, 2, 4, 8, 16, 32],
        33: [1, 3, 11, 33],
        34: [1, 2, 17, 34],
        35: [1, 5, 7, 35],
        36: [1, 2, 3, 4, 6, 9, 12, 18, 36],
        37: [1, 37],
        38: [1, 2, 19, 38],
        39: [1, 3, 13, 39],
        40: [1, 2, 4, 5, 8, 10, 20, 40],
        41: [1, 41],
        42: [1, 2, 3, 6, 7, 14, 21, 42],
        43: [1, 43],
        44: [1, 2, 4, 11, 22, 44],
        45: [1, 3, 5, 9, 15, 45],
        46: [1, 2, 23, 46],
        47: [1, 47],
        48: [1, 2, 3, 4, 6, 8, 12, 16, 24, 48],
        49: [1, 7, 49],
        50: [1, 2, 5, 10, 25, 50],
        51: [1, 3, 17, 51],
        52: [1, 2, 4, 13, 26, 52],
        53: [1, 53],
        54: [1, 2, 3, 6, 9, 18, 27, 54],
        55: [1, 5, 11, 55],
        56: [1, 2, 4, 7, 8, 14, 28, 56],
        57: [1, 3, 19, 57],
        58: [1, 2, 29, 58],
        59: [1, 59],
        60: [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60],
        61: [1, 61],
        62: [1, 2, 31, 62],
        63: [1, 3, 7, 9, 21, 63],
        64: [1, 2, 4, 8, 16, 32, 64],
        65: [1, 5, 13, 65],
        66: [1, 2, 3, 6, 11, 22, 33, 66],
        67: [1, 67],
        68: [1, 2, 4, 17, 34, 68],
        69: [1, 3, 23, 69],
        70: [1, 2, 5, 7, 10, 14, 35, 70],
        71: [1, 71],
        72: [1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72],
        73: [1, 73],
        74: [1, 2, 37, 74],
        75: [1, 3, 5, 15, 25, 75],
        76: [1, 2, 4, 19, 38, 76],
        77: [1, 7, 11, 77],
        78: [1, 2, 3, 6, 13, 26, 39, 78],
        79: [1, 79],
        80: [1, 2, 4, 5, 8, 10, 16, 20, 40, 80],
        81: [1, 3, 9, 27, 81],
        82: [1, 2, 41, 82],
        83: [1, 83],
        84: [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84],
        85: [1, 5, 17, 85],
        86: [1, 2, 43, 86],
        87: [1, 3, 29, 87],
        88: [1, 2, 4, 8, 11, 22, 44, 88],
        89: [1, 89],
        90: [1, 2, 3, 5, 6, 9, 10, 15, 18, 30, 45, 90],
        91: [1, 7, 13, 91],
        92: [1, 2, 4, 23, 46, 92],
        93: [1, 3, 31, 93],
        94: [1, 2, 47, 94],
        95: [1, 5, 19, 95],
        96: [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 96],
        97: [1, 97],
        98: [1, 2, 7, 14, 49, 98],
        99: [1, 3, 9, 11, 33, 99],
        100: [1, 2, 4, 5, 10, 20, 25, 50, 100],
        101: [1, 101],
        102: [1, 2, 3, 6, 17, 34, 51, 102],
        103: [1, 103],
        104: [1, 2, 4, 8, 13, 26, 52, 104],
        105: [1, 3, 5, 7, 15, 21, 35, 105],
        106: [1, 2, 53, 106],
        107: [1, 107],
        108: [1, 2, 3, 4, 6, 9, 12, 18, 27, 36, 54, 108],        
        109: [1, 109],
        110: [1, 2, 5, 10, 11, 22, 55, 110],
        111: [1, 3, 37, 111],
        112: [1, 2, 4, 7, 8, 14, 16, 28, 56, 112],
        113: [1, 113],
        114: [1, 2, 3, 6, 19, 38, 57, 114],
        115: [1, 5, 23, 115],
        116: [1, 2, 4, 29, 58, 116],
        117: [1, 3, 9, 13, 39, 117],
        118: [1, 2, 59, 118],
        119: [1, 7, 17, 119],
        120: [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120],
        121: [1, 11, 121],
        122: [1, 2, 61, 122],
        123: [1, 3, 41, 123],
        124: [1, 2, 4, 31, 62, 124],
        125: [1, 5, 25, 125],
        126: [1, 2, 3, 6, 7, 9, 14, 18, 21, 42, 63, 126],        
        127: [1, 127],
        128: [1, 2, 4, 8, 16, 32, 64, 128],
        129: [1, 3, 43, 129],
        130: [1, 2, 5, 10, 13, 26, 65, 130],
        131: [1, 131],
        132: [1, 2, 3, 4, 6, 11, 12, 22, 33, 44, 66, 132],       
        133: [1, 7, 19, 133],
        134: [1, 2, 67, 134],
        135: [1, 3, 5, 9, 15, 27, 45, 135],
        136: [1, 2, 4, 8, 17, 34, 68, 136],
        137: [1, 137],
        138: [1, 2, 3, 6, 23, 46, 69, 138],
        139: [1, 139],
        140: [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140],       
        141: [1, 3, 47, 141],
        142: [1, 2, 71, 142],
        143: [1, 11, 13, 143],
        144: [1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 36, 48, 72, 144],
        145: [1, 5, 29, 145],
        146: [1, 2, 73, 146],
        147: [1, 3, 7, 21, 49, 147],
        148: [1, 2, 4, 37, 74, 148],
        149: [1, 149],
        150: [1, 2, 3, 5, 6, 10, 15, 25, 30, 50, 75, 150],       
        151: [1, 151],
        152: [1, 2, 4, 8, 19, 38, 76, 152],
        153: [1, 3, 9, 17, 51, 153],
        154: [1, 2, 7, 11, 14, 22, 77, 154],
        155: [1, 5, 31, 155],
        156: [1, 2, 3, 4, 6, 12, 13, 26, 39, 52, 78, 156],       
        157: [1, 157],
        158: [1, 2, 79, 158],
        159: [1, 3, 53, 159],
        160: [1, 2, 4, 5, 8, 10, 16, 20, 32, 40, 80, 160],       
        161: [1, 7, 23, 161],
        162: [1, 2, 3, 6, 9, 18, 27, 54, 81, 162],
        163: [1, 163],
        164: [1, 2, 4, 41, 82, 164],
        165: [1, 3, 5, 11, 15, 33, 55, 165],
        166: [1, 2, 83, 166],
        167: [1, 167],
        168: [1, 2, 3, 4, 6, 7, 8, 12, 14, 21, 24, 28, 42, 56, 84, 168],
        169: [1, 13, 169],
        170: [1, 2, 5, 10, 17, 34, 85, 170],
        171: [1, 3, 9, 19, 57, 171],
        172: [1, 2, 4, 43, 86, 172],
        173: [1, 173],
        174: [1, 2, 3, 6, 29, 58, 87, 174],
        175: [1, 5, 7, 25, 35, 175],
        176: [1, 2, 4, 8, 11, 16, 22, 44, 88, 176],
        177: [1, 3, 59, 177],
        178: [1, 2, 89, 178],
        179: [1, 179],
        180: [1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 18, 20, 30, 36, 45, 60, 90, 180],
        181: [1, 181],
        182: [1, 2, 7, 13, 14, 26, 91, 182],
        183: [1, 3, 61, 183],
        184: [1, 2, 4, 8, 23, 46, 92, 184],
        185: [1, 5, 37, 185],
        186: [1, 2, 3, 6, 31, 62, 93, 186],
        187: [1, 11, 17, 187],
        188: [1, 2, 4, 47, 94, 188],
        189: [1, 3, 7, 9, 21, 27, 63, 189],
        190: [1, 2, 5, 10, 19, 38, 95, 190],
        191: [1, 191],
        192: [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96, 192],
        193: [1, 193],
        194: [1, 2, 97, 194],
        195: [1, 3, 5, 13, 15, 39, 65, 195],
        196: [1, 2, 4, 7, 14, 28, 49, 98, 196],
        197: [1, 197],
        198: [1, 2, 3, 6, 9, 11, 18, 22, 33, 66, 99, 198],
        199: [1, 199],
        200: [1, 2, 4, 5, 8, 10, 20, 25, 40, 50, 100, 200],
        201: [1, 3, 67, 201],
        202: [1, 2, 101, 202],
        203: [1, 7, 29, 203],
        204: [1, 2, 3, 4, 6, 12, 17, 34, 51, 68, 102, 204],
        205: [1, 5, 41, 205],
        206: [1, 2, 103, 206],
        207: [1, 3, 9, 23, 69, 207],
        208: [1, 2, 4, 8, 13, 16, 26, 52, 104, 208],
        209: [1, 11, 19, 209],
        210: [1, 2, 3, 5, 6, 7, 10, 14, 15, 21, 30, 35, 42, 70, 105, 210],
        211: [1, 211],
        212: [1, 2, 4, 53, 106, 212],
        213: [1, 3, 71, 213],
        214: [1, 2, 107, 214],
        215: [1, 5, 43, 215],
        216: [1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 27, 36, 54, 72, 108, 216],
        217: [1, 7, 31, 217],
        218: [1, 2, 109, 218],
        219: [1, 3, 73, 219],
        220: [1, 2, 4, 5, 10, 11, 20, 22, 44, 55, 110, 220],
        221: [1, 13, 17, 221],
        222: [1, 2, 3, 6, 37, 74, 111, 222],
        223: [1, 223],
        224: [1, 2, 4, 7, 8, 14, 16, 28, 32, 56, 112, 224],
        225: [1, 3, 5, 9, 15, 25, 45, 75, 225],
        226: [1, 2, 113, 226],
        227: [1, 227],
        228: [1, 2, 3, 4, 6, 12, 19, 38, 57, 76, 114, 228],
        229: [1, 229],
        230: [1, 2, 5, 10, 23, 46, 115, 230],
        231: [1, 3, 7, 11, 21, 33, 77, 231],
        232: [1, 2, 4, 8, 29, 58, 116, 232],
        233: [1, 233],
        234: [1, 2, 3, 6, 9, 13, 18, 26, 39, 78, 117, 234],
        235: [1, 5, 47, 235],
        236: [1, 2, 4, 59, 118, 236],
        237: [1, 3, 79, 237],
        238: [1, 2, 7, 14, 17, 34, 119, 238],
        239: [1, 239],
        240: [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 30, 40, 48, 60, 80, 120, 240],
        241: [1, 241],
        242: [1, 2, 11, 22, 121, 242],
        243: [1, 3, 9, 27, 81, 243],
        244: [1, 2, 4, 61, 122, 244],
        245: [1, 5, 7, 35, 49, 245],
        246: [1, 2, 3, 6, 41, 82, 123, 246],
        247: [1, 13, 19, 247],
        248: [1, 2, 4, 8, 31, 62, 124, 248],
        249: [1, 3, 83, 249],
        250: [1, 2, 5, 10, 25, 50, 125, 250],
        251: [1, 251],
        252: [1, 2, 3, 4, 6, 7, 9, 12, 14, 18, 21, 28, 36, 42, 63, 84, 126, 252],
        253: [1, 11, 23, 253],
        254: [1, 2, 127, 254],
        255: [1, 3, 5, 15, 17, 51, 85, 255]
})

framerate = 60
height = -1
width = -1
inverted = False
loop = False
extract_audio = False
img_path = ''
out_path = ''
replay = ''
audio_track = ''
processes = multiprocessing.cpu_count()

for i, a in enumerate(sys.argv):
    if a in ['-h', '--help'] or len(sys.argv) == 1:
        print('''
usage: python(3) img-brainfrickery.py [options]
Options:
    -h                  : Display these options
    -i [path]           : Input image/video path
    -o [path]           : Output brainfrick code file
    -r [path]           : Input brainfrick code file
    -w [int]            : Set video width  (Only applicable with -i)
    -h [int]            : Set video height (Only applicable with -i)
    -f [float]          : Set video framerate
    -x                  : Invert luminosity values (Only applicable with -i)
    -p [int]            : Number of threads to use to process video (Only applicable with -i)
    -l                  : Loop video playback
    -a                  : Extract audio from video and play (Only applicable with -i)
    --play-track [path] : Set playback track (Useful with -r)
              ''')
        sys.exit(0)
    elif a in ['-f', '--framerate']:
        framerate = float(sys.argv[i+1])
    elif a in ['-w', '--width']:
        width = int(sys.argv[i+1])
    elif a in ['-h', '--height']:
        height = int(sys.argv[i+1])
    elif a in ['-x', '--invert']:
        inverted = True
    elif a in ['-l', '--loop']:
        loop = True
    elif a in ['-i', '--infile']:
        img_path = sys.argv[i+1]
    elif a in ['-o', '--outfile']:
        out_path = sys.argv[i+1]
    elif a in ['-a', '--audio']:
        extract_audio = True
    elif a in ['--play-track']:
        audio_track = sys.argv[i+1]
    elif a in ['-r', '--replay']:
        replay = sys.argv[i+1]
    elif a in ['-p', '--processes']:
        processes = int(sys.argv[i+1])

if img_path == '' and replay == '':
    print('No image/video path supplied!')
    sys.exit(1)


def nearest_match(val, supply):
    lowest_diff = 99999
    index = -1
    for i, v in enumerate(supply):
        if abs(val - v) < lowest_diff:
            lowest_diff = abs(val - v)
            index = i
    return index

frame_count = 0

def process_video(image_path, frame_count, w, h, process_number, processes, frame_lists):
    cap = cv2.VideoCapture(image_path, cv2.CAP_FFMPEG)
    start = int(frame_count / processes * process_number)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)

    while start < int(frame_count / processes * (process_number + 1)):
        ret, frame = cap.read()
        if not ret:
            break
        frame_lists[process_number].append(image_to_ascii(frame, True))
        start += 1

def image_to_ascii(image_path, arr=False):
    global width
    global height
    if isinstance(image_path, str) and image_path[-4:] in ['.mp4', '.avi', '.mov', '.mkv', '.gif']:
        print('Processing frames...')
        
        global processes
        global frame_count

        with multiprocessing.Manager() as manager:  
            start = time.time_ns()
            frame_lists = manager.list()
            for p in range(processes):
                frame_lists.append(manager.list())

            cap = cv2.VideoCapture(image_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                
            process_list = []
            for p in range(processes if processes < frame_count else frame_count):
                process_list.append(multiprocessing.Process(target=process_video, args=(image_path, frame_count, width, height, p, processes, frame_lists)))

            for p in process_list:
                p.start()

            for p in process_list:
                p.join()

            ascii_frames = []
            for frame_list in frame_lists:
                ascii_frames.extend(list(frame_list))

            end = time.time_ns()

            print(f'Completed in {(end - start) / 1000000000} seconds!')

            return ascii_frames

    else:
        global inverted
        image = None
        if arr:
            image = Image.fromarray(image_path)
        else:
            image = Image.open(image_path)
        iwidth, iheight = image.size
        aspect_ratio = iheight / iwidth
        if height == -1 and width > 0:
            height = int(aspect_ratio * width * 0.55)
            image = image.resize((width, height))
        elif width == -1 and height > 0:
            width = int(aspect_ratio * height * 0.55)
            image = image.resize((width, height))
        elif width > 0 and height > 0:
            image = image.resize((width, height))
        else:
            width = 100
            height = int(aspect_ratio * width * 0.55)
            image = image.resize((100, height))
        image = image.convert('L')

        pixels = image.getdata()
        ascii_image = ""
        for pixel in pixels:
            ascii_image += ascii_luminosity_chars[nearest_match(abs(1 * inverted - pixel / 255), ascii_luminosity_vals)]
        
        ascii_image = '\n'.join(ascii_image[i:i + width] for i in range(0, len(ascii_image), width))

        return ascii_image

prev_c = 0

def ascii_to_brainfrick(ascii):
    if isinstance(ascii, list):
        print('Brainfrick-ifying frames...')
        frames = []
        
        for frame in ascii:
            frames.append(ascii_to_brainfrick(frame))
        print('Done!')
        return frames
    else:
        ascii = '\n' + ascii
        code = '>'
        global prev_c
        for c in ascii:
            step = ''
            c = ord(c)
            f1 = 0
            f2 = 0

            dc = c - prev_c
            if len(factors[abs(dc)]) > 1:
                if not abs(dc) in squares:
                    f1 = factors[abs(dc)][len(factors[abs(dc)]) // 2 - 1]
                    f2 = factors[abs(dc)][len(factors[abs(dc)]) // 2]
                else:
                    f1 = f2 = int(sqrt(abs(dc)))
            else:
                f1 = f2 = factors[abs(dc)][0]

            if dc != 0:
                if code[-1] != '>':
                    code += '>'
                step += '+' * f1
                
                if dc < 0:
                    step += '[<' + ('-' * f2) + '>-]<.>'
                elif dc > 0:
                    step += '[<' + ('+' * f2) + '>-]<.>'
            else:
                step = '.'
                if code[-1] == '>':
                    code = code[:-1]

            code += step
            prev_c = c
    return (code + ('<' if code[-1] == '>' else '')).replace(']', ']\n').split('\n')


if __name__ == '__main__':
    t = None
    path = pathlib.Path(__file__).parent.resolve()
    init_bf()
    if replay == '':
        im = ascii_to_brainfrick(image_to_ascii(img_path))

        if out_path != '':
            with open(out_path, 'w') as file:
                if isinstance(im[0], list):
                    for frame in im:
                        file.write(''.join(frame))
                        file.write('\n')
                else:
                    file.write(''.join(im))

        if isinstance(im[0], list):
            set_frame_size(''.join(im[0]).count('.'))
            if extract_audio:
                print('Extracting audio...')
                with open(os.devnull, 'w') as fp:
                    subprocess.run(['ffmpeg', '-y', '-i', str(path / img_path), '-ab', '160k', '-ac',  '2', '-ar',  '44100', '-vn', str(path / img_path)[:str(path / img_path).rfind('.')] + '.wav'], stdout=fp, stderr=fp)
                print('Done!')
            init_display()

            while True:
                if extract_audio:
                    if platform.system() == 'Windows':
                        t = threading.Thread(target=PlaySound, args=(str(path / img_path)[:str(path / img_path).rfind('.')].replace('\\', '/') + '.wav', SND_FILENAME))
                        t.start()
                    else:
                        playsound(str(path / img_path)[:str(path / img_path).rfind('.')].replace('\\', '/') + '.wav', False)
                for frame in im:
                    for line in frame:
                        interpret_code(line.encode('ascii'), True, framerate)
                if t:
                    t.join()
                if not loop:
                    break
                init_bf()
        else:
            set_frame_size(''.join(im).count('.'))
            for line in im:
                interpret_code(line.encode('ascii'), False, 0)

    else:
        with open(replay, 'r') as file:
            frames = file.read().split('\n')
            set_frame_size(frames[0].count('.'))
            if len(frames) > 1:
                init_display()
                
            while True:
                if audio_track != '':
                    if platform.system() == 'Windows':
                        t = threading.Thread(target=PlaySound, args=(str(path / audio_track).replace('\\', '/'), SND_FILENAME))
                        t.start()
                    else:
                        playsound(str(path / audio_track).replace('\\', '/'),  False)
                for frame in frames:
                    interpret_code(frame.encode('ascii'), (True if len(frames) > 1 else False), framerate)
                if t:
                    t.join()
                if not loop or len(frames) == 1:
                    break
                init_bf()