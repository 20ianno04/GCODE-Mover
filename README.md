# GCODE-Mover

## Description

While trying to create a parametric vase mode gridfinity storage box i stumbled on a problem.
I needed to print the lower part of the box with traditional slicing settings, but i wanted to meke the upper part in vase mode. (I use CURA slicer)
I couldnt print the whole body in vase mode because there would be holes betwheen the bottom squares. 
So i tried to slice the upper part in vase mode and offset it in the slicer, but this ended up in missing base layers and an incorrect offset.

![OffsetErrorVaseMode](/assets/OffsetErrorVaseMode.png)

## How does the program work

Running for the first time the program will create the **_input_** and the **_output_** folders.
Placing the base GCODE in the **_input_** file and running the program will start the procedure.

The program will ask for the offset distance in mm, and for the axis to move the model on.

After that the new modified GCODE will be created in the **_output_** folder
