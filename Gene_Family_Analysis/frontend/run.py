import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd
from GFA import family
import matplotlib.image as mpimg
from PIL import Image


app = Flask(__name__)

pathhome = str(os.path.join(Path.home(), "Downloads"))
frontend = os.path.join(pathhome)
image = os.path.join(pathhome, 'result.jpg')

button = '<form method="POST" action="/see_seq"><button type="submit" name="submit" id="but">See sequences</button></form>'


buttons = '<form method="get" action="/get_jpg"><button type="submit" id="but">Download as .jpeg</button></form> <form method="get" action="/get_png"><button type="submit" id="but">Download as .png</button></form> <form method="get" action="/get_pdf"><button type="submit" id="but">Download as .pdf</button></form>'




@app.route("/")
def home():
    return render_template('template.html')

@app.route('/info', methods=['POST'])
def get_result():
    #name = 'PFKFB1'
    global name
    name = request.form['textbox']
    #text11 = f"<h4>Please wait the analysis will take some time</h4>"
    global analysis
    analysis = family(name, pathhome, 'h', image)
    global result
    result = analysis.main_frame()

    analysis.fasta()

    global filename
    filename = str(name) + '_family.txt'
    global filepath
    filepath = os.path.join(pathhome, filename)
    
    with open(filepath) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        global sequence_list
        sequence_list = []
        sequence = ""
        names=[]
        for line in content:
            if line.startswith(">"):
                names.append(line)
                if sequence:
                    sequence_list.append(sequence)
                    sequence = ""
            else:
                sequence += line
        if sequence:
            sequence_list.append(sequence)
            
        global listval
        
        listval = []
        for x in names:
            var = x.split('(')[1]
            tmp = var.split(')')[0]
            listval.append(tmp)
    
    
    table = pd.DataFrame()
    table['Gene name'] = listval
    global table_html
    table_html = f"<h4>Results for the family of the gene: <b>{name.upper()}</b></h4>" + \
                        table.to_html(header="true", table_id="table", index=False)

    matrix = pd.DataFrame()
    matrix['Gene name'] = listval
    for i in listval:
        matrix[i] = 0*len(listval)
        
    ml = []
    sl = []    
    for x in range(len(listval)):
        for y in range(len(listval)):
            align1, align2, score = analysis.needleman_wunsch(sequence_list[x], sequence_list[y])
            sl.append(score)
            y += 1
        x += 1
        ml.append(sl)
        sl = []
    
    for k in range(len(listval)):
        matrix[listval[k]] = ml[k]
    
            
                
       
    global matrix_html
    matrix_html = f"<h4>Alignment matrix for the family of the gene: <b>{name.upper()}</b></h4>" + \
                 matrix.to_html(header="true", table_id="table", index=False)
    
    if len(listval) > 4:
        global text
        text = f"<h4>Phylogenetic tree for the family of the gene: <b>{name.upper()}</b></h4>"
        analysis.phylogeny()
        global tree
        tree = f'<img src="{image}"/>'
        
    else:
        text = f"<h4>Not enough sequences to build a tree, should be more than 5 sequences</h4>"
        tree = f' '
       
    
    return render_template('template.html', name=name.upper(), data=table_html, button = button, mat = matrix_html, tr = tree, t = text, buttons = buttons)
    
    
@app.route('/see_seq', methods=['POST'])
def see_seq():
    df = pd.DataFrame()
    df['Gene name'] = listval
    df['Sequence'] = sequence_list
    df_seq = df.to_html(header="true", index=False, table_id = 'table_id')
    return render_template('template.html', name=name.upper(), data=table_html, button = button, sequences = df_seq, mat = matrix_html, tr = tree, t = text, buttons = buttons)
    

@app.route('/get_jpg', methods=['GET'])
def save_jpg():
    im1 = Image.open(image)
    im1.save(Path(pathhome, f'{name}_tree.jpg'))
    fin_text = f"<h4>Phylogenetic tree saved to </h4>" + str(pathhome) + f' as {name}_tree.jpg'
    return render_template('template.html', name=name.upper(), data=table_html, button = button, mat = matrix_html, tr = tree, t = text, buttons = buttons, fin_text = fin_text)



@app.route('/get_png', methods=['GET'])
def save_png():
    im1 = Image.open(image)
    im1.save(Path(pathhome, f'{name}_tree.png'))
    fin_text = f"<h4>Phylogenetic tree saved to </h4>" + str(pathhome) + f' as {name}_tree.png'
    return render_template('template.html', name=name.upper(), data=table_html, button = button, mat = matrix_html, tr = tree, t = text, buttons = buttons, fin_text = fin_text)


@app.route('/get_pdf', methods=['GET'])
def save_pdf():
    im1 = Image.open(image)
    im1 = im1.convert('RGB')
    im1.save(Path(pathhome, f'{name}_tree.pdf'))
    fin_text = f"<h4>Phylogenetic tree saved to </h4>" + str(pathhome) + f' as {name}_tree.pdf'
    return render_template('template.html', name=name.upper(), data=table_html, button = button, mat = matrix_html, tr = tree, t = text, buttons = buttons, fin_text = fin_text)





if __name__ == "__main__":
    app.run(debug=True)


