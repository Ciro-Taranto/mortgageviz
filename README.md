# mortgageviz
A simple project to visualize monthly rate and additional information 
for a data informed decision about mortgage.

Assuming that you have docker installed, the simplest way to use the code is: 

`docker build -t mortgage .` 

and then:

`docker run -v .:/app -p 8501:8501 mortgage`

The first command will build a docker image that is serving a small streamlit dashboard on 
the port `8501`. The second command will run the image. The current working directory
will be mounted in the docker container, hence all the changes that you will make in the code 
will be immediately reflected in the running instance of the dashboard. 

If you know a bit of python, you do not need to use docker, but you can install
the requirements with: 

`python -m pip install -r requirements.txt` 

followed by: 

`pip install -e .`

Finally to run the dahsboard: 

`streamlit run Mortgage_Calculator.py`. 

The scope of this code is to have some fun, while doing something useful (at least for me). 

I can offer no guarantee about the correctness of this code,
 and I welcome any suggestion and comment, in particular about: 
 - formulas for the calculation of the monthly rate; 
 - jargon: I do not know if I have used the correct words. 

 Hope you read up to here, and that you can enjoy!  