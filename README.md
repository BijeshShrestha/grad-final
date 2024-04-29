Final Project - Interactive Data Visualization Research  
===
# Git repository, prospectus, storybook, Project screencast, and final project website 

### Git Repository: 

- [Project Submission](https://github.com/BijeshShrestha/grad-final) used for demo and user testing
- [Working Repository](https://github.com/BijeshShrestha/CQA_DataVis_Project): This repository is a working repository for the project and not clean
    
### Prospectus

    The prospectus is included in the repository as `Prospectus_VIS_Group_Project_AI_Charts.pdf` file in "docs_deliverables" folder.

### Process Book 
    The process book is included in the repository as `CS573_Process_Book.pdf` file in "docs_deliverables" folder.


### Project Screen-Cast
    
The project screen-cast is available at [📀 Youtube](https://www.youtube.com/watch?v=d49uKRn23p0)


### Project Website

The project website is hosted at [▶️ Project Website](https://bijeshshrestha.github.io/grad-final/)


### Chart Question Answering (CQA) Webapp

The CQA tool can be found here at [▶ CQA webapp](https://cqa.shrestha.club/). If the tool is not working, please follow the instructions below to run the project locally. You will need to have the openai api key to run the project locally.

# Instruction to run the project locally
    - Fork the repository from https://github.com/BijeshShrestha/grad-final
    - Navigate to the project directory
    - Run the following command to create a virtual environment
        **In Linux/Unix:**
        - python3 -m venv CQA_venv
        - source CQA_venv/bin/activate
        - pip install -r requirements.txt
        - rename .env.example to .env and update the openai api key and SAVE
        - streamlit run webapp_demo.py
        
        **In Windows:**
        - python -m venv CQA_venv
        - CQA_venv\Scripts\activate
        - pip install -r requirements.txt
        - rename .env.example to .env and update the openai api key and SAVE
        - streamlit run webapp_demo.py
    
