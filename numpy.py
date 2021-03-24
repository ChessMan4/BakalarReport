import os
import sys

import jinja2
import numpy as np
from numpy import genfromtxt
from tex import latex2pdf
import pdfkit

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
options = {"enable-local-file-access": None}

filename = "test.csv"

with open(filename, 'r') as csvfile:
    # creating a csv reader object
    my_data = genfromtxt(filename, delimiter=',', dtype=float)

    a = my_data[1:,1]
    b = my_data[1:,2]
    c = my_data[1:,3]
    d = my_data[1:,4]
    v = my_data[1:,5]
    amean = np.mean(a)
    bmean = np.mean(b)
    cmean = np.mean(c)
    dmean = np.mean(d)
    vmean = np.mean(v)
    num_rows = np.size(my_data,0)
    num_rows = num_rows-1
    nejistotaa = 1/(num_rows*(num_rows-1))

    aneja = np.sqrt(nejistotaa*np.square(np.sum(a-amean)))
    bneja = np.sqrt(nejistotaa*np.square(np.sum(b-bmean)))
    cneja = np.sqrt(nejistotaa*np.square(np.sum(c-cmean)))
    dneja = np.sqrt(nejistotaa*np.square(np.sum(d-dmean)))
    vneja = np.sqrt(nejistotaa*np.square(np.sum(v-vmean)))
    osobchyb = 0.1/np.sqrt(3)
    prist1chyba = 0.01/np.sqrt(3)
    prist2chyba = 0.05 / np.sqrt(3)

    kombchyba = np.sqrt(np.square(aneja) + np.square(prist1chyba))
    kombchybb = np.sqrt(np.square(bneja) + np.square(prist2chyba))
    kombchybc = np.sqrt(np.square(cneja) + np.square(prist2chyba))
    kombchybd = np.sqrt(np.square(dneja) + np.square(prist1chyba))
    kombchybv = np.sqrt(np.square(vneja) + np.square(prist2chyba))

    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    )

    template = latex_jinja_env.get_template('template.tex')
    picovina = template.render(stroj1='Osobni chyba', chyba1='0.001', stroj2="stroj1",
                          chyba2=prist1chyba, stroj3="stroj2", chyba3=prist2chyba,
                          table1=my_data, vys1=kombchyba, vys2=kombchybb, vys3=kombchybc,
                          vys4=kombchybd, vys5=kombchybv)
    with open("sadad.tex", "w") as output:
        output.write(picovina)

    #pdfl = latex2pdf("sadad.tex")
    pdfkit.from_file('sadad.tex', 'brmbrm.pdf', configuration=config, options=options)


sys.exit()