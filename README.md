Final Project - Interactive Data Visualization Research  
===
# Git repository, prospectus, storybook, Project screencast, and final project website 

### Git Repository: 

    - https://github.com/BijeshShrestha/grad-final [Project Submission used for demo and user testing]
    - https://github.com/BijeshShrestha/CQA_DataVis_Project [Working Repository: This repository is a working repository for the project and not clean.]
    
### Prospectus

    The prospectus is included in the repository as `Prospectus_VIS_Group_Project_AI_Charts.pdf` file in "docs_deliverables" folder.

### Process Book 
    The process book is included in the repository as `CS573_Process_Book.pdf` file in "docs_deliverables" folder.


### Project Screen-Cast
    
        The project screen-cast is available at https://www.youtube.com/watch?v=d49uKRn23p0&t=291s 


### Project Website

    The project website is hosted at https://bijeshshrestha.github.io/grad-final/


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
    