# Import dependencies 
from colored import fore_rgb, back_rgb, style, fore, Style
from .flags import flags
import argparse
import os

# Get terminal size
terminalSize = os.get_terminal_size()

def cli_entry_point():
    parser = argparse.ArgumentParser()

    parser.add_argument('flag', nargs='?', help='Choose what flag to generate in your terminal.')
    parser.add_argument('--char', default='█', help='Specify the character to use for the flag. Default is █.')

    args = parser.parse_args()

    if args.flag:
        handle_flag(args.flag, args.char)
    else:
        help(parser)

# Color / Style mess xd
color: str = f"{fore('red')}"
color2: str = f"{fore('green')}{Style.underline}"
color3: str = f"{fore('yellow')}"
underline: str = f"{Style.underline}"

# Display for help command 'pride' looks nice thanks to b3yc0d3 xd
def help(parser):
    print(f"{Style.BOLD}{color2}Usage:{style('reset')}{color3} pride{style('reset')} {color3}{underline}flag{style('reset')} {underline}{color3}[options]{style('reset')}\n")
    print(f"{Style.BOLD}{color2}Example:{style('reset')}")
    print(f"  {color3}> pride trans # Generates a Transgender flag {style('reset')}")
    print(f"  {color3}> pride bi --char W # Generates a Bisexual flag with W as characters {style('reset')}\n")
    print(f"{Style.BOLD}{color2}Options:{style('reset')}")
    print(f"  {color3}flag: Specific pride flag to display. See Flags section.")
    print(f"  --char: Specify what character do you want pride flag to be generate with.{style('reset')}\n")
    print(f"{Style.BOLD}{color2}Flags:{style('reset')}")
    print(f"  ", end = "")
    for i, flag_entry in enumerate(flags):
        flag_name = list(flag_entry.keys())[0]
        if i < len(flags) - 1:
            print(f"{color3}{flag_name}, ", end="")
        else:
            print(flag_name)
    print(f"{style('reset')}\n")
    print(f"{color3}cli-rpide-flags-python v1.2.0 by ItzSulfur{style('reset')}")

# Generating pride flags
def handle_flag(selected_flag_name, char):
    # Select flag from flags.py
    selected_flag = None
    for flag_entry in flags:
        flag_name = list(flag_entry.keys())[0]
        if flag_name == selected_flag_name:
            selected_flag = flag_entry
            break
    
    if selected_flag is None:
        print(f"{color2}Invalid flag name!{style('reset')}")
    else:
        flag_name = list(selected_flag.keys())[0]

        total_flag_height = sum(int(count) for _, count in selected_flag[flag_name])

        # Calculate the number of rows needed to display the flag within the terminal height
        rows_per_block = max(1, terminalSize.lines // total_flag_height)
        flag_data = []
        # Convert to rgb since colored hex is being funky ;-;
        for color, count in selected_flag[flag_name]:
            color = color.lstrip('#')
            color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            count = int(count)
            rows_needed = rows_per_block * count
            flag_data.append((color, rows_needed))
        
        # Print the flag over the entire terminal height :3
        for color, rows_needed in flag_data:
            for _ in range(rows_needed):
                print(f"{fore_rgb(*color)}{char}{style('reset')}" * terminalSize.columns)
