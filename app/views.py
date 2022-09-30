from calendar import c
from cmath import pi
from app import *
from app.pdfToData import cgpa_calculator
from app.pdftodata1 import calculator
import pickle


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
        return redirect(url_for('fileUpload', filename=file.filename))
    return render_template('index.html', form=form)

@app.route('/result', methods=['GET', 'POST'])
def result():
    course_and_grade = pickle.load(open('course_and_grade.pkl', 'rb'))
    return render_template('result.html', result=request.args.get('result'), course_and_grade=course_and_grade)


@app.route('/upload', methods=['GET', 'POST'])
def fileUpload():
    cgpa_calculator = calculator()
    result, course_and_grade = cgpa_calculator.pdfToText(filename=request.args.get('filename'))
    pickle.dump(course_and_grade, open('course_and_grade.pkl', 'wb'))
    return redirect(url_for('result', result=result))
    # result(result=result)
    


@app.route("/update", methods=["POST"])
def update():
    _course_and_grade = pickle.load(open('course_and_grade.pkl', 'rb'))
    course_code = request.form.get("course_code")
    grade = request.form.get("grade")
    cgpa_calculator = calculator()
    result, course_and_grade = cgpa_calculator.update(course_code=course_code, cgpa=grade, course_and_grade=_course_and_grade)
    pickle.dump(course_and_grade, open('course_and_grade.pkl', 'wb'))
    return redirect(url_for('result', result=result))


@app.route("/delete", methods=["POST"])
def delete():
    course_code = request.form.get("course_code")
    print(course_code)
    course_and_grade = pickle.load(open('course_and_grade.pkl', 'rb'))
    del course_and_grade[course_code]
    pickle.dump(course_and_grade, open('course_and_grade.pkl', 'wb'))
    cgpa_calculator = calculator()
    result = cgpa_calculator.caluculate_cgpa(course_and_grade)
    return redirect(url_for('result', result=result))