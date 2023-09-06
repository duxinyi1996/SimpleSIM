# Project Name: Simple_SIM

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
	- [Graphical Interface Guide](#graphical-interface-guide)
	- [Command-line Guide](#command-line-guide)
3. [Project Structure](#project-structure)
    - [HFSS Compiler](hfss-Compiler)
    - [DXF Compiler](dxf-compiler)
4. [Key Features](#key-features)
5. [Getting Started](#getting-started)


## Introduction

Welcome to the Simple_SIM project, a minimalist Python venture tailored to streamline your experience with KLayout and PyAEDT. At its core, Simple_SIM breaks down the foundational concept of graphical representation like lines, arcs, taper lines, curved polyline, and coplanar waveguides into two highly focused Python files: `dxf_compiler.py` and `HFSS_compiler.py`. 

## Installation

### Graphical Interface Guide

#### 1. Download the Simple_SIM Repository

- Visit the [Simple_SIM GitHub repository](https://github.com/Henriksen-Lab/Simple_SIM).
- Click on the green `Code` button on the right.
- Choose `Download ZIP`.
- Once downloaded, extract the ZIP file to a location of your choice.

#### 2. Install Anaconda

Anaconda is a popular distribution of Python that simplifies package management and deployment.

- [Download Anaconda](https://www.anaconda.com/products/distribution) for your operating system.
- Follow the installation instructions for your operating system from the [Anaconda installation guide](https://docs.anaconda.com/anaconda/install/).

#### 3. Setting Up a Virtual Environment with Anaconda Navigator

Anaconda Navigator is a GUI tool that comes with the Anaconda distribution.

1. Open **Anaconda Navigator** from your applications or programs list.
2. Click on `Environments` on the left sidebar.
3. Click on `Create` at the bottom.
4. Name it `simple_sim_env` and choose the Python version you want (e.g., 3.X). Click on the `Create` button.
5. After the environment is created, make sure it's activated (should be highlighted in green).

#### 4. Setting Up Your IDE and Installing Dependencies

##### For PyCharm:

1. Open PyCharm and choose `Open` to load the `Simple_SIM` directory you extracted from the ZIP file.
2. Once the project is open, navigate to `File` > `Settings` (or `Preferences` on macOS) > `Project: Simple_SIM` > `Python Interpreter`.
3. Click on the gear icon and choose 'Add'.
4. From the left pane, select 'Conda Environment' and then 'Existing environment'.
5. Select the interpreter from the `simple_sim_env` environment you created in Anaconda Navigator. The path would typically be in the Anaconda directory under `envs/simple_sim_env/bin/python`.
6. To automatically install the required packages, navigate to `Tools` in the top menu and select `Sync Python Requirements`. This will read the `requirements.txt` file and install all necessary packages.

##### For VSCode:

1. Open the `Simple_SIM` directory (that you extracted from the ZIP file) in VSCode.
2. Press `Ctrl + Shift + P` to open the command palette.
3. Type and select "Python: Select Interpreter".
4. Choose the interpreter from the `simple_sim_env` environment you created in Anaconda Navigator.
5. Open the terminal in VSCode (View > Terminal) and type:

```bash
pip install -r requirements.txt
```

### Command-line Guide

#### 1. Clone the Repository

To get started, first clone the Simple_SIM repository from GitHub:

```bash
git clone https://github.com/Henriksen-Lab/Simple_SIM.git
```

Navigate to the cloned directory:

```bash
cd Simple_SIM
```

#### 2. Set Up a Virtual Environment

**Using Python's built-in venv:**

```bash
# Using venv module for Python
python -m venv venv

# Activate the virtual environment
# For Windows
venv\Scripts\activate

# For macOS and Linux
source venv/bin/activate
```

**Using Anaconda (if installed):**

```bash
conda create --name simple_sim_env python=3.X
conda activate simple_sim_env
```

Replace `3.X` with your desired Python version.


#### 3. Install Dependencies

To install the required packages,

```bash
pip install -r requirements.txt
```


## Project Structure

This project is structured into two primary components, providing an optimized and seamless way to draw various patterns and export them in the appropriate format:

### HFSS Compiler
Defined in the `HFSS_compiler.py` file, the HFSS class acts as the foundation, encapsulating the necessary functionalities to draw specific patterns and ensures the precise exportation of the HFSS model format.

### DXF Compiler
The `dxf_compiler.py` file houses the DXF Compiler class, a subclass of the HFSS Compiler class. This deliberate hierarchy guarantees that the output in the HFSS model mirrors exactly what is depicted in the generated DXF file.

## Key Features

1. **Simplified Drawing**: Easy-to-use methods for drawing fundamental shapes such as lines, circles, and tapered lines.
2. **Unified Output**: Designed to ensure uniformity between the HFSS and DXF outputs, preventing discrepancies and ensuring accuracy.
3. **Expandable**: The structured class hierarchy allows for seamless expansions and additions to the available drawing patterns and functionalities.
