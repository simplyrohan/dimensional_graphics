# Dimensional
A pygame 3D renderer.

# Install
```bash
git clone https://github.com/simplyrohan/dimensional_graphics.git
```

# Usage
Camera:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parameters: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;objs: A list of all `Models` to be rendered.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Methods:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;render(screen): Pass a surface to render all objects (every frame)

Model: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Parameters: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;faces: Face data generated by `dimensional_graphics.loader.load(obj_file_path)`  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;scale: A scaling factor
