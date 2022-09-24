from app import *
from app.pdfToData import cgpa_calculator

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField('Upload File')

class UpdateCGPAForm(FlaskForm):
    course_code = StringField("Course Code", validators=[InputRequired()])
    cgpa = StringField("CGPA", validators=[InputRequired()])
    submit = SubmitField('Update CGPA')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        return redirect(url_for('result', filename=file.filename))
    return render_template('index.html', form=form)


@app.route('/result', methods=['GET', 'POST'])
def result():
    form = UpdateCGPAForm()
    if form.validate_on_submit():
        course_code = form.course_code.data.upper()
        cgpa = form.cgpa.data
        result = cgpa_calculator(filename=request.args.get('filename'), course_code=course_code, cgpa=cgpa)
    else:
        result = cgpa_calculator(filename=request.args.get('filename'))
    return render_template('result.html', result=result, form=form)