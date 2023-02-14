import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from pathlib import Path
import pandas as pd
from Gene_Family_Analysis.GFA_package.GFA.GFA import family
import matplotlib.image as mpimg
from PIL import Image
import requests 


pathhome = Path.home()
project = os.path.join(pathhome, 'Gene_Family_Analysis')
front = os.path.join(project, 'frontend')
static = os.path.join(front, 'static')
image = os.path.join(static, 'result.jpg') 


app = Flask(__name__)

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
    api_query = f"http://rest.genenames.org/fetch/symbol/{name}"
    response = requests.get(api_query, headers={"Accept": "application/json"})
    data= response.json()
    id= data['response']
    if id['numFound']==0:
        error = f"<h4>No results found for the gene: <b>{name.upper()}</b></h4>"
        return render_template('template.html', name=name.upper(), t = error)
    
    
    
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
        text = f"<h4>Phylogenetic tree for the family of the gene: <b>{name.upper()}</b></h4><br><a href = '/tree'>See the tree</a>"
        analysis.phylogeny()
        
    else:
        text = f"<h4>Not enough sequences to build a tree, should be more than 5 sequences</h4>"
        tree = f' '
        
        global buttons
        buttons = f' '
       
    
    return render_template('template.html', name=name.upper(), data=table_html, button = button, mat = matrix_html, tr = f' ', t = text, buttons = f' ')
    
    
@app.route('/see_seq', methods=['POST'])
def see_seq():
    df = pd.DataFrame()
    df['Gene name'] = listval
    df['Sequence'] = sequence_list
    df_seq = df.to_html(header="true", index=False, table_id = 'table_id')
    return render_template('template.html', name=name.upper(), data=table_html, button = button, sequences = df_seq, mat = matrix_html, t = text, buttons = buttons)
    

@app.route('/get_jpg', methods=['GET'])
def save_jpg():
    im1 = Image.open(image)
    im1.save(Path(pathhome, 'phylogenetic_tree.jpg'))
    fin_text = f"<h4>Phylogenetic tree saved to </h4>" + str(pathhome) + ' as phylogenetic_tree.jpg'
    return render_template('phylogenetic_tree.html', buttons = buttons, fin_text = fin_text)



@app.route('/get_png', methods=['GET'])
def save_png():
    im1 = Image.open(image)
    im1.save(Path(pathhome, 'phylogenetic_tree.png'))
    fin_text = f"<h4>Phylogenetic tree saved to </h4>" + str(pathhome) + ' as phylogenetic_tree.png'
    return render_template('phylogenetic_tree.html', buttons = buttons, fin_text = fin_text)


@app.route('/get_pdf', methods=['GET'])
def save_pdf():
    im1 = Image.open(image)
    im1 = im1.convert('RGB')
    im1.save(Path(pathhome, 'phylogenetic_tree.pdf'))
    fin_text = f"<h4>Phylogenetic tree saved to </h4>" + str(pathhome) + ' as phylogenetic_tree.pdf'
    return render_template('phylogenetic_tree.html', buttons = buttons, fin_text = fin_text)
    
    
@app.route('/tree')
def see_tree():
    return render_template('phylogenetic_tree.html', buttons = buttons)
    






if __name__ == "__main__":
    app.run(debug=True)


