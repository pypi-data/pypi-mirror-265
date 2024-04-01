# EITpyLab - An open-source education tool for Electral Impedance Tomograph learning in Python

![PyPI - License](https://img.shields.io/pypi/l/EITpyLab%20)
![PyPI - Version](https://img.shields.io/pypi/v/EITpyLab)
![GitHub repo size](https://img.shields.io/github/repo-size/barbaractong/py-eit)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fgithub.com%2Fbarbaractong%2Fpy-eit%2Fblob%2Fmaster%2Fpyproject.toml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/EITpyLab%20)


EITpyLab is an innovative open-source project designed to serve as an educational tool for learning Electral Impedance Tomography (EIT) using the Python programming language. Developed initially for educational purposes at UFABC university, EITpyLab is poised to become a valuable resource for students, researchers, and professionals worldwide interested in the field of EIT in medical applications.

## 🦾 Backlog implemetation

- [x] Set the global cache for forward problem variables that should be used in all program 
- [x] Check getters and setters for fem_modeling class
- [x] Implements the observation model
- [ ] Validate the model with openSAHE result
- [ ] Fix the testing pipeline in gitflow
- [ ] Review documentation text in mkdocs
- [ ] Review inverse problem topics

## 🔬 What is Electral Impedance Tomography (EIT)?

Electrical Impedance Tomography (EIT) is a non-invasive tomographic imaging technique that estimates the distribution of electrical properties 
within a target. EIT systems make electrical stimulations using surface electrodes and measure the resulting voltages at the surface at 
combinations of the same electrodes, from which tomographic images of electrical impeditivity distribution are generated.

Although EIT is no longer a new technology, new uses are developed all the time. Global research has drastically increased after its 
commercial availability, and has slowly begun to make its way into industry and some areas of medicine.

EIT is a promising method for the development of noninvasive diagnostic medicine, as it is able to provide functional imaging of the body without 
ionizingg radiation. EIT has several applications in medicine, including but not limited to: functional imaging of the lungs, diagnosis of 
pulmonary embolism, detection of tumors, diagnosis and distinction of normal and suspected abnormal tissue within the same 
organ, bedside monitoring of lung perfusion and respiratory function, cerebral circulation, and stroke monitoring.

## 🔎 Why EITpyLab?

EITpyLab is designed to provide an intuitive platform for learning and experimenting with EIT algorithms. By offering a user-friendly Python 
environment, EITpyLab empowers users to explore the theoretical and practical concepts behind EIT, implement algorithms, and visualize results. 
Whether you're a student gaining a foundational understanding of EIT principles or a researcher developing advanced reconstruction algorithms, 
EITpyLab  offers a flexible and customizable framework for your learning journey.

## 🦾 Key Features of EITpyLab:

- **Python-Based Environment:** EITpyLab is built entirely in Python, leveraging its simplicity, versatility, and extensive scientific libraries. Python's intuitive syntax and rich ecosystem make it an ideal choice for beginners and experienced users alike.

- **Educational Resources:** EITpyLab provides comprehensive educational resources, including documentation, tutorials, and sample datasets, to support users at every stage of their learning journey. From introductory concepts to advanced topics, EITpyLab aims to foster a supportive learning environment for users of all backgrounds.

- **Modular Design:** EITpyLa badopts a modular design, allowing users to easily extend and customize the tool according to their specific requirements. Whether you're experimenting with different reconstruction algorithms or integrating EIT into larger projects, EITLearn's modular architecture facilitates seamless integration and collaboration.

- **Real-Time Visualization:** EITpyLab offers real-time visualization capabilities, enabling users to interactively visualize and analyze EIT reconstructions as they evolve. Through dynamic visualizations, users gain deeper insights into the principles of tomographic reconstruction and the behavior of different algorithms.

- **Open-Source Community:** EITpyLab is developed as an open-source project, fostering a vibrant community of contributors, collaborators, and users. By embracing open-source principles, EITpyLab encourages knowledge sharing, collaboration, and continuous improvement, ensuring its relevance and impact in the field of EIT education.

## 💻 Getting Started 

To get started with EITpyLab, follow these steps:

1. Clone the repository: `git clone https://github.com/yourusername/EITpyLab.git`
2. Create a virtual enviroment (recommended):
    Following the guidelines provided by PEP 405, you can create a virtual enviroment by executing the command venv:

    a. Install virtualenv lib: ````pip install virtualenv````
    
    b. Run venv command in your root directory with the path name that should be created

    ````bash
    python3 -m venv ./venv/
    `````

    This command will create your virtual env in the root's project.

2. Install the required dependencies: `pip install -r requirements.txt`

> :bulb: **Tip:** This project also supports Poetry for dependence management. You can you the venv created by Poetry or crete one by yourself. After configure you enviroment, you can run ```poetry install``` in your terminal to install all dependencies needed.

> :warning: **Warning:** Do not upload your machine poetry.lock file to the repo. Our .gitignore prevents this to not happen. But, be careful :grimacing:

3. You can explore the documentation and tutorials provided in the `py_eit` branch. To run it, in development mode, you will need to use ```mkdocs``` lib (already a requirement in .toml file :smile:).
To build it in your local machine, you will need to run the command below in your terminal

````
mkdocs serve
````

> :warning: **Attention:** Check if the you're in the same directory as the mkdocs.yml. You should run the command in the root folder in the py_eit branch!

4. Experiment with the sample datasets and reconstruction algorithms included in the `examples/` directory.
5. Contribute to the project by reporting issues, submitting pull requests, or sharing your feedback with the community.

## :pushpin: Basic usage

The EITpyLab lib uses parameters file as inputs to create a <i>session</i> for your development. The files used are listed next. For a deep documentation, please access the mkdocs local version of it.

- <b>Electrical properties</b>:This file contains general information regarding voltage and input current. It defines the methods of injection, units of measurement, amplitude, and electrodes used in the injection of electrical current.

````yaml
version: '0.1'
current:
  frequency: 1000.0
  value: 5
  unit: mA
  direction: +-
  method: bipolar_skip_full
  skip: 8
  injectionPairs: [[5, 32], [2, 32], [1, 32], [6, 32], [4, 32], [5, 31], [5, 30], [2, 27], [1, 28], [1, 25], [6, 26], [4, 29], [2, 23], [10, 30], [9, 31], [3, 32], [7, 32], [1, 24], [3, 21], [7, 18], [4, 22], [6, 17], [8, 31], [11, 30], [1, 20], [13, 31], [15, 30], [2, 19], [14, 31], [16, 18], [12, 21],]
voltage:
  method: differential_skip
  removeInjectingPair: False 
  direction: -+
  skip: 4
  referenceVoltageNode:
    method: coords
    node: [127.937, 123.356, 70.7998]
    unit: mm
````

- <b>Properties of the finite element model:<b> This file consolidates the parameters used in constructing the connectivity matrices of the FEM model, as well as contains the description of the domain and the dimension of the mesh used.

````yaml
version: '0.1'
path: './mesh_files/mesh_head_05.msh'
unit: mm
dimentions: 3
heigthElement: None
eletrodes:
  numberElectrodes: 32
  meshTag: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
  model: completeHua
  rho_t: 0.02
regions:
  - label: scalp
    isActive: True
    meshTag: [36]
    dimentions: 3
    rho_0: 2.5
  - label: skull
    isActive: True
    meshTag: [37]
    dimentions: 3
    rho_0: 47.94
  - label: CSF+GM+WM
    isActive: True
    meshTag: [38]
    dimentions: 3
    rho_0: 0.5
````

- <b>Direct problem properties:</b> This file consolidates the parameters used in solving the direct problem related to EIT.

````yaml
version: '0.1'
numberElectrodes: 32
nodalVoltages: 
  active: False
  filePath: ./mesh_nodal_voltages.txt
exportGmsh: True
measurementOutputPath: ./mesh_head_measurements_forwardProblem.txt
objects: # None or properties
  - type: sphere
    regionTags: [38]
    unit: mm
    center: [125.0, 50.0, 145.0]
    radius: 10
    rho: [-1.0, 20.0]
  - type: sphere
    regionTags: [40]
    unit: mm
    center: [125.0, 50.0, 145.0]
    radius: 10
    rho: [-1.0, 5.0]
````

2. Starting yout EITpyLab session

First, import the lib and initialize the session

````python
# Importing the lib
import py_eit as eit

# Starting you session to load the parameter files
parameterFile = eit.ParameterFile()

# Loading all the parameter files that uses the pattern above
parameterFile.set_parameter(fileEnum=eit.Parameters.GENERAL, file_path='../py-eit/param_files/electral-properties.yml')
parameterFile.set_parameter(fileEnum=eit.Parameters.FORWARD_PROBLEM, file_path='../py-eit/param_files/foward-problem.yml')
parameterFile.set_parameter(fileEnum=eit.Parameters.FEM_MODEL, file_path='../py-eit/param_files/fem-model.yml')

# Loads the mesh file using our mesh reader module
mesh = eit.MeshGenerator()

mesh.open(file = './mesh_files/mesh_head_05.msh')

# Based on your needs, invokes the method to return the information desired
fem = eit.FemModeling(outputBasePath='.', filePrefix='teste')
fem.get_domain_element_quality('teste.txt')

fem.set_k_global()

# Returns the k-global for your mesh file
print(fem.KglobalSp)
````


## 🪄 Contributing

Contributions to EITpyLab are welcome and encouraged! Whether you're a developer, educator, or enthusiast, there are many ways to contribute to the project:

- Report issues and suggest enhancements: [Create an Issue](https://github.com/barbaractong/EITpyLab/issues)
- Submit pull requests: [Contribution Guidelines](CONTRIBUTING.md)
- Share your feedback and ideas: [Join the Discussion](https://github.com/barbaractong/EITpyLab/discussions)

## 📝 License

This project is licensed under the [MIT License](LICENSE).


Join us in our mission to democratize EIT education and empower learners worldwide with the tools and knowledge to explore the fascinating field of Electral Impedance Tomography. Whether you're a student, educator, researcher, or enthusiast, your contributions and feedback are invaluable in shaping the future of EITLearn.

Explore EITpyLab today and embark on your journey of discovery in Electral Impedance Tomography with Python!
