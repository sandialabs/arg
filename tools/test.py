import glob

# Values to retrieve
path = "C:/dev/git/test"
template = "licence-template"
extension = "*.py"

# Constants
tmp = "tmp"
header_regex = "#HEADER"

# Method
def make_header(file, out):



print("Running: $path $template $extension")

# Get list of files from provided path
files = glob.glob(path)

# Loop over all files
for file in files:
    temp = "{}.{}".format(file, tmp)
    open(temp, "w") as f:
        print("Processing file {}, {}".format(file, temp))
        in_header = False
        output_header = False
        for line in f:
            if header_regex in line:
                in_header = not in_header
                next
            if in_header:
                print(out)
            else:
                if not output_header:
                    make_header(file, out)
                    output_header = True
        f.close()

    if not output_header:
        out.close()
        temp = "{}.{}".format(temp, tmp)
        open(out, "w") as f_out:
