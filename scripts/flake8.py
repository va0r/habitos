import os

if __name__ == "__main__":

    executive_string = 'flake8 ../. --ignore=E501,F401,F811 > ../data/flake8_report.txt 2>&1'
    os.system(executive_string)
