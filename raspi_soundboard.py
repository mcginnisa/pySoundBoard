
import pygame
from pygame.locals import *
import sys
import os



# variables
#increase this number to make the legend font bigger
fontmultipler = 1.5
size = [480, 480]
rows = 6  # 10 max
spacing = int(size[0]/(1+2*rows))
fadein = 1000
fadeout = 3000
offset12 = spacing + 12
leftB = 1
rightB = 3
asset_folder_name = 'assets'
config_file_name = 'config.txt'
#this font must be included in asset folder!
font_name = 'IBMPlexMono-Medium.otf'



# colors
red = (237, 85, 101)
orange = (252, 110, 81)
yellow = (255, 206, 84)
yellow2 = (246, 187, 66)
green = (160, 212, 104)
green2 = (140, 193, 82)
greenforest = (34,139,34)
turquoise = (72, 207, 173)
blue = (79, 193, 233)
purple = (93, 156, 236)
black = (0, 0, 0)
white = (255, 255, 255)
dark = (30, 30, 30)
grey = (150, 150, 150)
grey2 = (20, 20, 20)

# initialize game engine
pygame.mixer.pre_init(44100, -16, 1, 512)  # fixes delay in play
pygame.init()
# global banner

# init channels
pygame.mixer.set_num_channels(rows**2)

# set screen width/height and caption
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.set_caption('1')




def resource_path(relative_path):


	split_path = relative_path.split('/')
	dir = split_path[0]
	file = split_path[1]
	#relative_path = os.path.join(os.getcwd(),dir, file)
	'''
	try:
	# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = os.path.join(sys._MEIPASS,
	except Exception:
		base_path = os.path.abspath(".")
		'''
	'''
	split_path = relative_path.split('/')
	dir = split_path[0]
	file = split_path[1]
	'''
	return os.path.join(os.getcwd(),dir, file)

# def readpaths():
#     '''read rows**2 lines from paths.txt file
#     and create a list of paths'''
#     paths = []
#     with open("paths.txt") as myfile:
#         paths = [next(myfile) for x in range(rows**2)]
#     # remove white space
#     paths = [line.rstrip('\n') for line in paths]
#     return paths

def readpaths2():
    # global banner
    '''read rows**2 lines from paths.txt file
    and create a list of paths'''
    # lines = []
    sound_data = []
    # data[i]['flag'] == 'US'
    asset_url = resource_path(asset_folder_name + '/' + config_file_name)
    with open(asset_url) as file_object:
        lines = file_object.read().splitlines()
    # lines = [line.rstrip('\n') for line in lines]

    #trucate list if it is too big
    # banner = lines[0]
    lines = lines[1:rows**2-1]

    i = 0
    for line in lines:
        line = line.rstrip('\n')
        entries = line.split(',')
        thisdict =	{
					  "index": entries[0],
					  "title": entries[1],
					  "paths": line.split(',')[2:len(entries)]
					}
		#[string[7:][:-4] for string in thisdict['paths']]
        sound_data.append(thisdict)
        i = i+1
    # add extra dummy rows if not enough sound files were added
    if i < rows**2-1:
        for j in range(rows**2-i):
            thisdict =	{
                          "index": i + 1,
                          "title": 'empty',
                          "paths": ['empty']
                        }
            sound_data.append(thisdict)
            i = i + 1
    return sound_data


def makebuttons():
    '''generate sound button objects according to the number of
    rows'''
    data = []
    n = 0
    for j in range(rows):
        for i in range(rows):
            data.append({
                'index': n+1,
                'soundchannel': pygame.mixer.Channel(n),
                # 'soundobj': pygame.mixer.Sound(sound_data[n]['paths']),
                'coord': (spacing*(2*i+1), spacing*(2*j+1)),
                'size': (spacing, spacing),
                'paths': sound_data[n]['paths'],
                'rectobj': pygame.Rect(spacing*(2*i+1), spacing*(2*j+1), spacing, spacing),
                'textobj': fontObj.render(str(n+1), False, black),
                'textname': sound_data[n]['title'],
                'filename': sound_data[n]['paths'],
                'textcoords': (spacing*(2*i+1.3), spacing*(2*j+1.3)),
                'namecoords': (spacing*(2*i+1), spacing*(2*j+2.2)),
                'filecoords': (spacing*(2*i+1), spacing*(2*j+2.6)),
                'color': grey,
                'loop': False,
                'cur_play': sound_data[n]['paths'][0][7:][:-4],
                'no_file': 0
            })
            n += 1
    data[rows**2-2]['textname'] = 'RESET'
    data[rows**2-2]['paths'] = ['']
    data[rows**2-2]['textobj'] = fontnames.render('', True, red)
    data[rows**2-1]['textname'] = 'EXIT'
    data[rows**2-1]['paths'] = ['']
    data[rows**2-1]['textobj'] = fontnames.render('', True, red)

        # 'soundchannel': pygame.mixer.Channel(n),
        # # 'soundobj': pygame.mixer.Sound(sound_data[n]['paths']),
        # 'coord': (spacing*(2*i+1), spacing*(2*j+1)),
        # 'size': (spacing, spacing),
        # 'paths': 'empty',
        # 'rectobj': pygame.Rect(spacing*(2*i+1), spacing*(2*j+1), spacing, spacing),
        # 'textobj': fontObj.render(str(n+1), False, black),
        # 'textname': fontnames.render('STOP', True, red),
        # 'filename': fontnames.render('', True, red),
        # 'textcoords': (spacing*(2*i+1.3), spacing*(2*j+1.3)),
        # 'namecoords': (spacing*(2*i+1), spacing*(2*j+2.2)),
        # 'filecoords': (spacing*(2*i+1), spacing*(2*j+2.6)),
        # 'color': red,
        # 'loop': False

    return data


def makelogo():
    # draw logo according to the size of the buttons
    asset_url = resource_path(asset_folder_name + '/' + config_file_name)
    with open(asset_url) as file_object:
        lines = file_object.read().splitlines()
    banner = lines[0]
    logo = fontLogo.render(banner, True, white)
    logoRect = logo.get_rect()
    logoRect.midright = (spacing*(2*rows), spacing/2)
    return (logo, logoRect)

# def rotate_list(list):
def rotate_list(list, num=1):
    return list[num:] + list[:num]
    # output_list = []
    #
    # # Will add values from n to the new list
    # for item in range(len(lists) - num, len(lists)):
    #     output_list.append(lists[item])
    #
    # # Will add the values before
    # # n to the end of new list
    # for item in range(0, len(lists) - num):
    #     output_list.append(lists[item])
    #
    # return output_list

#pygame.font.init()
#all_fonts = pygame.font.get_fonts()
#print(all_fonts)
#font = pygame.font.SysFont(all_fonts[0], 20) # just use the first font.
#font = pygame.font.Sy
# init fonts
font = resource_path(asset_folder_name + '/' + font_name)
fontLogo = pygame.font.Font(font, int(spacing/2))
fontObj = pygame.font.Font(font, int(spacing/2.5))
fontnames = pygame.font.Font(font, int(fontmultipler*spacing/5))
filenames = pygame.font.Font(font, int(fontmultipler*spacing/5))

# make the initial set of objects
# paths = readpaths()
sound_data = readpaths2()
# print(len(sound_data))
data = makebuttons()
# print(data[rows]['coord'][0])
logo = makelogo()

# initialize clock. used later in the loop.
clock = pygame.time.Clock()

paused = False

# Loop until the user clicks close button
done = False
while done == False:

    # clear the screen before drawing
    screen.fill(dark)
    # draw border
    pygame.draw.rect(screen, grey2, (0, 0, size[0], size[1]), 1)
    # write event handlers here
    # mousepress = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == leftB:
            pos = pygame.mouse.get_pos()
            # mousepress = 1
            for i in range(len(data)):
                elem = data[i]
                if elem['rectobj'].collidepoint(pos):
                    pygame.mixer.stop()
                    if elem['textname'] == 'EXIT':
                        exit()
                    if elem['textname'] == 'RESET':
                        sound_data = readpaths2()
                        data = makebuttons()
                        logo = makelogo()
                    try:
                        # Sound = pygame.mixer.Sound(elem['paths'])
                        asset_path = resource_path(elem['paths'][0])
                        good_path = elem['paths'][0]
                        # elem['cur_play'] = elem['paths'][0][7:][:-4]
                        # print(elem['paths'])
                        #screen.blit(fontnames.render(elem['paths'][0][7:][:-4], True, white), elem['filecoords'])
                        #pygame.display.update()
                        elem['paths'] = rotate_list(elem['paths'])
                        # print(elem['paths'])
                        elem['no_file'] = 0
                        elem['soundchannel'].play(pygame.mixer.Sound(asset_path))
                        #print(data['paths'])
                        #elem['paths'] = rotate_list(elem['paths'])
                    except:
                        elem['no_file'] = 1
                        pass
                    pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                   elem['coord'][1]-6, offset12, offset12), 5)

    # write game logic here
    pos = pygame.mouse.get_pos()
    for elem in data:
        if elem['soundchannel'].get_busy():
            elem['color'] = greenforest
            elem['cur_play'] = elem['paths'][-1][7:][:-4]
        else:
            elem['cur_play'] = elem['paths'][0][7:][:-4]
            elem['color'] = white
        if elem['rectobj'].collidepoint(pos):
            pygame.draw.rect(screen, green, (elem['coord'][0]-6,
                                              elem['coord'][1]-6, offset12, offset12), 1)
        if elem['textname'] == 'EXIT':
            elem['color'] = red
        if elem['textname'] == 'RESET':
            elem['color'] = red
        if elem['no_file']:
            elem['color'] = yellow
    # write draw code here
    screen.blit(logo[0], logo[1])
    # for elem in data:
    for i in range(len(data)):
        elem = data[i]
        pygame.draw.rect(screen, elem['color'], elem['rectobj'])
        screen.blit(elem['textobj'], elem['textcoords'])
        screen.blit(fontnames.render(elem['textname'], True, white), elem['namecoords'])
        screen.blit(fontnames.render(elem['cur_play'], True, white), elem['filecoords'])



    # display what’s drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()
