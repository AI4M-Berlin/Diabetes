# Diabetes Project
This project aims to explore links between diabetes and cardiovascular diseases. Eventually, this analysis could lead to the development of a future application to follow patients with high risk of cardiovascular diseases through the assessment of their risk and recommendations to lower it.

## Notation 
This project is part of a master's thesis. Notation differs from thesis: 
dataset_1 is mentionned as "stroke dataset"
dataset_2 as "perfusion dataset"


## Organization
```
.
├── data 
├── data_cleaning
├── data_mining
├── datasets_exploration
├── diabetes_project.yml
├── requirements.txt
├── environment.yml
├── module
└── README.md
```

**data/**: data & documentation (source, link, etc) 

**data_cleaning/**: datasets cleaned for later purposes.

**data_mining/**: dataset analysis (Random Forest, SHAP, etc.)

**data_exploration/**: overview of found datasets for this project. The objective was to analyze the relevance of multiple datasets for our use case

**module/**: contains custom module CSV_cleaner integrating functions for checking consistency and clean dataframe. The documentation is available in docs/build/html/

## Environment
Two ways, if you want to have the exact same environment as the one used during this project you should use the **environment.yml** file that includes dependancies. On the other hand if you just want the main librairies used **requirements.txt**


You can create a conda environment from it with the following command:
```
conda create --name <env> --file <your choice>
```


author: Victoria FATHI 
