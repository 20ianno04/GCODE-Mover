import time
import os


# COSTANTS

CWD = os.getcwd()
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
OFFSET_AXIS = 'Z'

# FUNCTIONS

def IO_dir_ckeck(): # Check/create IO directories
    if not(os.path.exists(OUTPUT_DIR)):
        os.makedirs(OUTPUT_DIR)
    if not(os.path.exists(INPUT_DIR)):
        os.makedirs(INPUT_DIR)
    

def get_input() -> float: # Offset input
    while True:
        offset = input('GCODE MOVER\n\nOffset (mm): ')
        try:
            offset = round(float(offset), 3)
            break
        except:
            print('Offset is not a number!')
            time.sleep(1)
            os.system('cls')
    
    while True:
        axis_choice = input('Select the axis to move (XYZ):')
        if axis_choice == 'X' or axis_choice == 'x':
            axis = axis_choice.upper()
            break
        elif axis_choice == 'Y' or axis_choice == 'y':
            axis = axis_choice.upper()
            break
        elif axis_choice == 'Z' or axis_choice == 'z':
            axis = axis_choice.upper()
            break
        else:
            print('Axis is absent!')
            time.sleep(1)
            os.system('cls')
    return offset, axis


def get_base_gcode() -> str: # Get base file content
    IO_dir_ckeck()
    try:
        file_name = CWD +'\\'+ INPUT_DIR +'\\'+ os.listdir(CWD + '\\' + INPUT_DIR)[0]
        bgc_file = open(file_name, 'r')
        base_gcode_content = bgc_file.readlines()
        bgc_file.close()
    except:
        file_name = 'NA'
        base_gcode_content = 'NA'
    
    return base_gcode_content, file_name


def get_cordinate_positions(g_base_values:list, axis:str) -> list: # Get axes cordinates
    z_data = []
    for i in range(len(g_base_values)):
        z_start = g_base_values[i].find(axis)
        if z_start != -1 and (z_start < g_base_values[i].find(';') or g_base_values[i].find(';') == -1):
            z_end = g_base_values[i].find(' ', z_start)
            z_data.append([i, z_start+1, z_end])
    return z_data


def get_value_num(ranges:list, g_base_values:list) -> list: # Transforms cordinates in numbers
    nums = []
    for i in range(len(ranges)):
        try:
            nums.append(int(g_base_values[ranges[i][0]][ranges[i][1]:ranges[i][2]]))
        except:
            nums.append(float(g_base_values[ranges[i][0]][ranges[i][1]:ranges[i][2]]))
    return nums


def add_offset(base_nums:list, offset:float) -> list: # Add offset to base values
    offset_nums = []
    for val in base_nums:
        val += offset
        offset_nums.append(str(round(val, 3)))
    return offset_nums


def replace_value(offset_nums:list, base_nums:list, content:list, cordinates:list, axis:str) -> list: # Replace base value with offset one
    for i in range(len(base_nums)):
        content[cordinates[i][0]] = content[cordinates[i][0]].replace(f'{axis}{str(base_nums[i])}', f'{axis}{offset_nums[i]}')
    return content



# ------------------------------------ MAIN PROGRAM ------------------------------------


os.system('cls')    #Clear cmd on start

full_input_dir = CWD + '\\' + INPUT_DIR


while True: #Check presence of base file
    base_content, baseF_path = get_base_gcode()
    if base_content != 'NA':
        break
    else:
        print(f"\nNo input file in: '{full_input_dir}'")
        print('Move the file you want to edit in said directory \nClosing program...')
        time.sleep(5)
        exit()

offset, axis = get_input()

full_output_dir = CWD + '\\' + OUTPUT_DIR + f'\\{axis}_{offset}_{os.listdir(full_input_dir)[0]}'

base_nums_range = get_cordinate_positions(base_content, axis)
base_nums = get_value_num(base_nums_range, base_content)
offset_nums = add_offset(base_nums, offset)
offset_content = replace_value(offset_nums, base_nums, base_content,base_nums_range, axis)

output_file = open(full_output_dir, 'w')
for line in offset_content:
    output_file.write(line)

print(f'\nFile created in {full_output_dir}\n')
time.sleep(5)

output_file.close()
