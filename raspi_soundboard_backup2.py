


import pygame
from pygame.locals import *
import sys
import os
import subprocess
import xlrd





#==========Configuration=============
#increase this number to make the legend font bigger
# fontmultipler = 1.5
size = [800, 480]
rows = 4  # 10 max
columns = 8
spacing_rows = int(size[0]/(1+2*rows))
spacing_columns = int(size[1]/(1+2*columns))
text_spacing = spacing_columns
fadein = 1000
fadeout = 3000
offset12 = spacing_columns + 12
leftB = 1
rightB = 3
asset_folder_name = 'assets'
config_file_name = 'config.txt'
#to read from excel file, the config file must have xls somewhere in it, ...
# ...or you can force excel mode by setting excel mode = 1. Otherwise, will use text mode if supplied text file
excel_mode = 0 #to FORCE excel file mode, set this to 1, only use if excel file isnt working

#this font must be included in asset folder!
font_name = 'IBMPlexMono-Medium.otf'
exit_shuts_down = 0 #turn this off for debugging purposes


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
pygame.mixer.set_num_channels(rows*columns)

# set screen width/height and caption
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.set_caption('1')




def resource_path(relative_path):


	split_path = relative_path.split('/')
	dir = split_path[0]
	file = split_path[1]
	#relative_path = os.path.join(os.getcwd(),dir, file)

	return os.path.join(os.getcwd(),dir, file)



def readpaths2():

	if config_file_name.find('.xls'):
		return read_paths_excel()
	if excel_mode:
		return read_paths_excel()
    # global banner
    #read rows*columns lines from paths.txt file and create a list of paths
    # lines = []
	sound_data = []
    # data[i]['flag'] == 'US'
	asset_url = resource_path(asset_folder_name + '/' + config_file_name)
	with open(asset_url) as file_object:
		lines = file_object.read().splitlines()
    # lines = [line.rstrip('\n') for line in lines]

    #trucate list if it is too big
    # banner = lines[0]
	lines = lines[1:rows*columns-1]

	i = 0
	for line in lines:
	    line = line.rstrip('\n')
	    entries = line.split(',')
	    thisdict =	{
			"index": entries[0],
			"title": entries[1],
			"paths": line.split(',')[2:len(entries)]
					}
	    sound_data.append(thisdict)
	    i = i+1
	# add extra dummy rows if not enough sound files were added
	if i < rows*columns-1:
	    for j in range(rows*columns-i):
	        thisdict =	{
				"index": i + 1,
				"title": '',
				"paths": ['']
	                    }
	        sound_data.append(thisdict)
	        i = i + 1
	return sound_data

def read_paths_excel():
	# global banner
	#read rows and columns from excel file
	# lines = []
	sound_data = []
	# data[i]['flag'] == 'US'
	asset_url = resource_path(asset_folder_name + '/' + config_file_name)
	# with open(asset_url) as file_object:
	#     lines = file_object.read().splitlines()

	# Give the location of the file
	# loc = ("path of file")

	# To open Workbook
	wb = xlrd.open_workbook(asset_url)
	sheet = wb.sheet_by_index(0)

	# i = 0
	for i in range(sheet.nrows()):
		#skip first entry, it is the banner string
		if i == 0:
			banner = sheet.row_values(i)[0]
			continue
		# for j in range(sheet)
		thisdict =	{
			"banner": banner,
			"index": sheet.row_values(i)[0],
			"title": sheet.row_values(i)[1],
			"paths": sheet.row_values(i)[2:len(sheet.row_values(i))]
					}
		sound_data.append(thisdict)
		if x == list[-1]:
			j = i - 1

	# the first entry of the sound data list will be empty because of the banner string
	# so we will rotate the list to the left and delete the last entry
	rotate_list(sound_data)
	sound_data.pop()
	print(sound_data)
	# lines = lines[1:rows*columns-1]


    # add extra dummy rows if not enough sound files were added
	if j < rows*columns-1:
	    for k in range(rows*columns-j):
	        thisdict =	{
				"banner": banner,
				"index": j + 1,
				"title": '',
				"paths": ['']
	                    }
	        sound_data.append(thisdict)
	        j = j + 1

	print(sound_data)

	# For row 0 and column 0
	# print(sheet.cell_value(0, 0))
	return sound_data


def makebuttons():
    #generate sound button objects according to the number ofrows
    data = []
    n = 0
    for j in range(columns):
        for i in range(rows):
            data.append({
				# 'banner': sound_data[0]['banner'],
                'index': n+1,
                'soundchannel': pygame.mixer.Channel(n),
                # 'soundobj': pygame.mixer.Sound(sound_data[n]['paths']),
                'coord': (spacing_rows*(2*i+1), spacing_columns*(2*j+1)),
                'size': (spacing_rows, spacing_columns),
                'paths': sound_data[n]['paths'],
                'rectobj': pygame.Rect(spacing_rows*(2*i+1), spacing_columns*(2*j+1), spacing_rows, spacing_columns),
                'textobj': fontObj.render(str(n+1), False, black),
                'textname': sound_data[n]['title'],
                'filename': sound_data[n]['paths'],
                'textcoords': (spacing_rows*(2*i+1.3), spacing_columns*(2*j+1.3)),
                'namecoords': (spacing_rows*(2*i+1), spacing_columns*(2*j+2.2)),
                'filecoords': (spacing_rows*(2*i+1), spacing_columns*(2*j+2.6)),
                'color': grey,
                'loop': False,
                'cur_play': sound_data[n]['paths'][0],
                'no_file': 0
            })
            n += 1
    data[rows*columns-2]['textname'] = ''
    data[rows*columns-2]['paths'] = ['']
    data[rows*columns-2]['textobj'] = fontObj.render('RESET', False, white)
    data[rows*columns-1]['textname'] = ''
    data[rows*columns-1]['paths'] = ['']
    data[rows*columns-1]['textobj'] = fontObj.render('EXIT', False, white)

    return data


def makelogo(sound_data):
    # draw logo according to the size of the buttons
    # asset_url = resource_path(asset_folder_name + '/' + config_file_name)
    # with open(asset_url) as file_object:
        # lines = file_object.read().splitlines()
    # banner = lines[0]
	banner = sound_data[0]['banner']
    logo = fontLogo.render(banner, True, white)
    logoRect = logo.get_rect()
    logoRect.midright = (text_spacing*(2*rows), text_spacing/2)
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
fontLogo = pygame.font.Font(font, int(text_spacing/2))
fontObj = pygame.font.Font(font, int(text_spacing/2.5))
fontnames = pygame.font.Font(font, int(fontmultipler*text_spacing/5))
filenames = pygame.font.Font(font, int(fontmultipler*text_spacing/5))

# make the initial set of objects
# paths = readpaths()
sound_data = readpaths2()
# print(len(sound_data))
data = makebuttons()
# print(data[rows]['coord'][0])
logo = makelogo(sound_data)

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
                    if elem['index'] == rows*columns: #exit
                        exit()
						if exit_shuts_down:
							subprocess.Popen(['shutdown','-h','now'])
                    if elem['index'] == rows*columns-1: #reset
                        sound_data = readpaths2()
                        data = makebuttons()
                        logo = makelogo(sound_data)
                    try:
                        # Sound = pygame.mixer.Sound(elem['paths'])
                        asset_path = resource_path(asset_folder_name + '/' + elem['paths'][0])
                        good_path = elem['paths'][0]
                        # print(elem['paths'])
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
                    # pygame.draw.rect(screen, red, (elem['coord'][0]-6,
                                                   # elem['coord'][1]-6, elem['rectobj'].midright, elem['rectobj'].midtop), 5)

    # write game logic here
    pos = pygame.mouse.get_pos()
    for elem in data:
        if elem['soundchannel'].get_busy():
            elem['color'] = greenforest
            elem['cur_play'] = elem['paths'][-1]
        else:
            elem['cur_play'] = elem['paths'][0]
            elem['color'] = white
        # if elem['rectobj'].collidepoint(pos):
            # pygame.draw.rect(screen, green, (elem['coord'][0]-6,
                                              # elem['coord'][1]-6, offset12, offset12), 1)
        if elem['index'] == rows*columns-1: #RESET
            elem['color'] = red
        elif elem['index'] == rows*columns: #EXIT
            elem['color'] = red
        elif elem['no_file']:
            elem['color'] = yellow
    # write draw code here
    screen.blit(logo[0], logo[1])
    # for elem in data:
    for i in range(len(data)):
        elem = data[i]
		#draw rectangle
        pygame.draw.rect(screen, elem['color'], elem['rectobj'])
		#Display number on button
        screen.blit(elem['textobj'], elem['textcoords'])
		#display name from name column
        screen.blit(fontnames.render(elem['textname'], True, white), elem['namecoords'])
		#display file name
        # screen.blit(fontnames.render(elem['cur_play'], True, white), elem['filecoords'])



    # display what’s drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()
