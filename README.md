![Python Versions][pyversion-button]
![Blender Versions][blender-version]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
<p align="center">
  <img src="https://github.com/wenchien/blender-material-to-vtf/blob/master/images/installation_2.PNG">
</p>

Blender Source Tools allows Blender to import and export Studiomdl Data and DMX model files. However, in order to streamline the process of material exporting, .QC compilation and HLMV previewing, it's not exactly convenient especially the material exporting part.

I don't want to click through VTFEdit or any other VTF editing software anymore. I want an add-on with simple GUI that quickly export materials in batch. This is my first blender add-on that tackles this problem. You can say this is pretty much a Blender GUI for VTFLib


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* ![Python Versions][pyversion-button]
* ![Blender Versions][blender-version]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get started, download the .zip file from the release page
* ![Latest Release](https://github.com/wenchien/blender-material-to-vtf/releases/latest)

### Prerequisites

* Blender v2.93+
* Blender v2.80 may or may not work
* Blender v2.79 or any version below will NOT work

### Installation


1. Open up Blender (See prerequisites) and go to **Edit > Preferences > Add-ons > Install...**
2. Select the downloaded .zip
3. Enable it. You should have something similar to the following:

<p align="center">
  <img src="https://github.com/wenchien/blender-material-to-vtf/blob/master/images/isntallation_1.PNG">
</p>

4. Now, go to your side panel **"Scene"** and scroll to **"VTFLibConverter"** section. You should have something like the following:

<p align="center">
  <img src="https://github.com/wenchien/blender-material-to-vtf/blob/master/images/installation_2.PNG">
</p>

5. Under **VTFCmd Path**, enter the path to ![VTFCmd.exe](https://github.com/NeilJed/VTFLib). Note: This textfield cannot be empty
6. Under *Material Output Path*, enter the path to your materials folder (i.e _game-full-name_\ _game-folder_\ _materials_). Note: it must be materials folder and this textfield cannot be empty


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

1. Follow the installation and setup guide from the previous section
2. Make sure all your materials have the following node setup: As of right now, only "Principled BSDF" is supported

<p align="center">
  <img src="https://github.com/wenchien/blender-material-to-vtf/blob/master/images/node_setup.PNG">
</p>

3. When you're ready to export your materials, click on the *Refresh Material List* first. By default, all materials will be selected for exporting (indicated by highlight). You may manually deselect the materials that you wish to ignore for exporting. The example below will only export the material **Material.001**

<p align="center">
  <img src="https://github.com/wenchien/blender-material-to-vtf/blob/master/images/example_1.PNG">
</p>

4. After that, choose your format, alpha format and vtf version by using the dropdown menus
5. If the **Resize?** checkbox is ticked, values in the following dropdown menus will be used for exporting:

<p align="center">
  <img src="https://github.com/wenchien/blender-material-to-vtf/blob/master/images/example_2.PNG">
</p>

6. If you wish to generate corresponding .VMT file, tick the **Generate .VMT** checkbox and select your desired _shader_. Note: the VMT will be generated and placed under your materials folder that you've selected earlier

<p align="center">
  <img src="https://github.com/wenchien/blender-material-to-vtf/blob/master/images/example_3.PNG">
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Version 1.0.0 code clean-ups
- [ ] GUI label alignment and adjustments
- [ ] Capture STDOUT and STDERR
- [ ] Support for relative path for both _VTFCMD Path_ and _Material Output Path_
- [ ] Support for different types of shaders
    - [ ] Diffuse BSDF
    - [ ] Mix Shader
- [ ] Automatic exporting Normal maps
- [ ] Automatic baking if a material has a shader but without TEX_IMAGE (Pure color) and export it
- [ ] Allow custom .VMT parameters
- [ ] Additional support for format and alpha format

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[blender-version]: https://img.shields.io/badge/Blender-2.93%2B-yellowgreen
[pyversion-button]: https://img.shields.io/badge/Python-3.10-green
