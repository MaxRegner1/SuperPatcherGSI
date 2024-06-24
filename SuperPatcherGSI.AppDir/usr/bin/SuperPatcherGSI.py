import os
import argparse
import shutil
import pathlib
import platform
import binascii

# Determine platform (Linux or Windows)
platform = 1 if platform.system() == 'Linux' else 0 if platform.system() == 'Windows' else 2

# Set temporary directory based on platform
TempDIR = (os.getcwd() + "/" + ".temp") if platform == 1 else (os.getcwd() + "\\" + ".temp") if platform == 0 else None

# Find script directory
HERE = os.path.realpath(os.path.dirname(__file__))

# Decide if input is a path or file
def mod_path(string):
    if os.path.isfile(string):
        return string
    elif os.path.isdir(string):
        return os.path.realpath(string)

# Initialize argparse
parser = argparse.ArgumentParser(add_help=True)
# Add flags
parser.add_argument('-i1', '--input1', type=mod_path, help='Input the first super.img file or directory.')
parser.add_argument('-i2', '--input2', type=mod_path, help='Input the second super.img file or directory.')
parser.add_argument('-o', '--output', help="Directs the output to a name of your choice")
parser.add_argument('-s', '--SLOT', type=int, help="Number of slots on the device: 1 (A) or 2 (A/B)")
args = parser.parse_args()

# Error check
def check():
    err = ""
    try:
        if args.SLOT == 1 or args.SLOT == 2:
            pass
        else:
            print("Invalid Slot number ({slot})".format(slot=args.SLOT))
            err += " &SLOT"

        if args.input1.endswith(".img") and os.path.isfile(args.input1) and args.input2.endswith(".img") and os.path.isfile(args.input2):
            pass
        else:
            print("Invalid Format at INPUT please use .img files")
            err += " &InvalidFormatINPUT"

        if args.output.endswith(".img"):
            pass
        else:
            print("Invalid Format at OUTPUT please use .img file")
            err += " &InvalidFormatOUTPUT"

        if err == "":
            err = "OK"
    except ValueError:
        err = "Flag ValueError"
    except AttributeError:
        err = "Flag AttributeError"
    return err

# Unpack/replacing
def lpunpack(input_img):
    if platform == 1:
        os.system("python3 '{dir}/lpunpack.py' {superimg} '{tempdir}'".format(superimg=input_img, tempdir=TempDIR, dir=HERE))
    elif platform == 0:
        os.system("powershell {command}".format(command=repr(".\'{dir}\\lpunpack.exe' {superimg} '{tempdir}'".format(superimg=input_img, tempdir=TempDIR, dir=HERE))))

# Hex mode analysis
def hex_analyze(input_img1, input_img2, output):
    with open(input_img1, 'rb') as f1, open(input_img2, 'rb') as f2, open(output, 'wb') as out:
        data1 = f1.read()
        data2 = f2.read()
        hex_diff = binascii.hexlify(data1) if len(data1) > len(data2) else binascii.hexlify(data2)
        out.write(hex_diff)

def main():
    err = check()

    if err != "OK":
        print("Error code ({error}) exiting...!".format(error=err))
        return err
    else:
        print("Flags successfully verified and appear to be correct, error code ({error})".format(error=err))

    if args.input1.endswith(".img") and args.input2.endswith(".img"):
        print("============================")
        print("     Performing analysis")
        print("============================")
        hex_analyze(args.input1, args.input2, args.output)

    print("============================")
    print("        Cleaning...")
    print("============================")
    shutil.rmtree(TempDIR) # Clean temp directory
    return err

try:
    err = main()
except KeyboardInterrupt:
    print("\n============================")
    print("        Cleaning...")
    print("============================")
    shutil.rmtree(TempDIR)
exit(err)
