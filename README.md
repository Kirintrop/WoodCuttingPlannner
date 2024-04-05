# CutList Optimizer

This Python script is designed to optimize the cutting process for materials such as wood material that comes in standard-sized sheets or boards.
It reads a list of required cuts from a text file, optimizes the cutting layout to minimize waste, and outputs the results in both text and DXF format
for further use in CAD software or cutting machinery. 

## Features

- **File Selection Dialog**: Utilizes tkinter's `filedialog` to select the input file.
- **Cut List Optimization**: Reads required cuts from a file and calculates how to make those cuts from standard-sized materials with minimal waste.
- **Output Formats**: Generates a text file summarizing the cutting process and a DXF file for CAD applications.
- **Material Efficiency**: Sorts and prioritizes cuts to ensure the most efficient use of material.
- **User Feedback**: Provides immediate feedback through the console, including the number of raw boards used, products cut, remaining boards, and execution time.

## Requirements

- Python 3.x
- tkinter (for the file dialog)
- ezdxf (for generating DXF files)

## How to Use

1. **Prepare the Cut List**: Create a text file with each line representing a cut. Each line should contain the width, height, and quantity of each piece required, separated by commas (e.g., `500,600,2` for two pieces of 500x600 units).

2. **Run the Script**: Execute the script. A file dialog will appear for you to select the cut list file.

3. **Select the Cut List File**: Navigate to the location of your cut list file, select it, and confirm.

4. **Review the Output**: The script will output the number of raw boards used, the list of products cut, remaining boards, and the total execution time. Additionally, it generates a text file with a summary of these results and a DXF file for CAD or cutting machinery.

5. **DXF and Text Files**: The DXF file contains detailed layouts of the cuts, including dimensions and labels for easy reference. The text file summarizes the cutting process, including the number of pieces cut and the sizes of any remaining material.

## Notes

- The efficiency of the cutting optimization depends on the size of the raw materials and the dimensions of the required cuts. Adjusting these parameters may yield better results.
- The script is designed for simplicity and may need modifications to suit specific cutting requirements or material constraints.

## Conclusion

This script is a valuable tool for workshops, DIY enthusiasts, or manufacturing processes where material efficiency and waste reduction are crucial. By automating the cut list optimization, it saves time, reduces material waste, and facilitates a more efficient cutting process.
