import os

from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError, Email, NumberRange, URL, Length, Regexp

# placeholders used in scripts.
HOME_ID = "&&home_id"
FI_NAME = "&&fi_name"
SPONSOR_ID = "&&sponsor_id"
BUG_ID = "&&bug_id"
RTN = "&&rtn"
PARTNER_ID = "&&partner_id"
CSR_EMAIL = "&&csr_email"
REPLY_EMAIL = "&&reply_email"
CSR_PHONE = "&&csr_phone"
HOME_PAGE = "&&home_page"
ACH = "&&ach"
QA_ORG = "&&qa_org"
CERT_ORG = "&&cert_org"
STAGE_ORG = "&&stage_org"
PROD_ORG = "&&prod_org"
POD_NUMBER = "&&pod_number"
CERT_DOMAIN = "&&cert_domain"
PROD_DOMAIN = "&&prod_domain"
DANAL = "&&danal"
VERID = "&&verid"
CUSTOM_DOMAIN = "&&custom_domain"
CONNECTIVITY = "&&instant_connectivity"

cf_port = os.getenv("PORT")

# Class Flask Form - RXP decommission.
class RxpForm(FlaskForm):
    home_id = IntegerField(label='HOME_ID', validators=[DataRequired(message='Home ID - This field is required.'),
                                                        NumberRange(min=88830000, max=88839999,
                                                                    message="Incorrect Home ID length/Series.")])
    fi_name = StringField(label='FI NAME', validators=[DataRequired(message='FI NAME - This field is required.')])
    bug_id = IntegerField(label='BUG ID', validators=[DataRequired(message='BUG ID - This field is required.'),
                                                      NumberRange(min=200000, max=500000,
                                                                  message='Incorrect Bug Number, currently we are '
                                                                          'using bug number in 6 digit series.')])
    sponsor_id = StringField(label='SPONSOR ID',
                             validators=[DataRequired(message='SPONSOR ID - This field is required.')])


# Class Flask Form - TN decommission.
class TnForm(FlaskForm):
    home_id = IntegerField(label='HOME_ID', validators=[DataRequired(message='Home ID - This field is required.'),
                                                        NumberRange(min=88100000, max=88199999,
                                                                    message="Incorrect Home ID length/Series.")])
    fi_name = StringField(label='FI NAME', validators=[DataRequired(message='FI NAME - This field is required.')])
    bug_id = IntegerField(label='BUG ID', validators=[DataRequired(message='BUG ID - This field is required.'),
                                                      NumberRange(min=200000, max=500000,
                                                                  message='Incorrect Bug Number, currently we are '
                                                                          'using bug number in 6 digit series.')])


# Class Flask Form - DI decommission.
class DiForm(FlaskForm):
    home_id = IntegerField(label='HOME_ID', validators=[DataRequired(message='Home ID - This field is required.'),
                                                        NumberRange(min=88880000, max=88889999,
                                                                    message="Incorrect Home ID length/Series.")])
    fi_name = StringField(label='FI NAME', validators=[DataRequired(message='FI NAME - This field is required.')])
    bug_id = IntegerField(label='BUG ID', validators=[DataRequired(message='BUG ID - This field is required.'),
                                                      NumberRange(min=200000, max=500000,
                                                                  message='Incorrect Bug Number, currently we are '
                                                                          'using bug number in 6 digit series.')])
    products = ['TN', 'POP', 'TN_POP']
    product = SelectField(label='PRODUCT', choices=products,
                          validators=[DataRequired()])


# Class Flask Form - ROL decommission.
class RolForm(FlaskForm):
    home_id = IntegerField(label='HOME_ID', validators=[DataRequired(message='Home ID - This field is required.'),
                                                        NumberRange(min=88840000, max=88849999,
                                                                    message="Incorrect Home ID length/Series.")])
    fi_name = StringField(label='FI NAME', validators=[DataRequired(message='FI NAME - This field is required.')])
    bug_id = IntegerField(label='BUG ID', validators=[DataRequired(message='BUG ID - This field is required.'),
                                                      NumberRange(min=200000, max=500000,
                                                                  message='Incorrect Bug Number, currently we are '
                                                                          'using bug number in 6 digit series.')])
    rtn = StringField(label='Routing Number',
                      validators=[DataRequired(message='Routing Number - This field is required.'),
                                  Length(min=9, max=9, message="RTN should be at most 9 digits.")])


# Class Flask Form - Zelle default setup.
class ZelleForm(FlaskForm):
    home_id = IntegerField(label='HOME_ID', validators=[DataRequired(message='Home ID - This field is required.'),
                                                        NumberRange(min=88850000, max=88859999,
                                                                    message="Incorrect Home ID length/Series.")])
    fi_name = StringField(label='FI NAME', validators=[DataRequired(message='FI NAME - This field is required.')])
    partner_id = StringField(label='PARTNER ID',
                             validators=[DataRequired(message='PARTNER ID - This field is required.'),
                                         Length(min=4, max=4, message="Partner ID should be at most 4 digits.")])
    rtn = StringField(label='Routing Number',
                      validators=[DataRequired(message='Routing Number - This field is required.'),
                                  Length(min=9, max=9, message="RTN should be at most 9 digits.")])
    bug_id = IntegerField(label='BUG ID', validators=[DataRequired(message='BUG ID - This field is required.'),
                                                      NumberRange(min=200000, max=500000,
                                                                  message='Incorrect Bug Number, currently we are '
                                                                          'using bug number in 6 digit series.')])
    csr_email = EmailField('CSR Email', default='donotreply_banking@fiserv.com',
                           validators=[DataRequired(), Email()])
    reply_email = EmailField('Reply Email', default='donotreply_banking@fiserv.com',
                             validators=[DataRequired(), Email()])
    csr_phone = StringField('CSR Phone', validators=[DataRequired(message='CSR Phone - This field is required.')])
    home_page = StringField('Home Page URL',
                            validators=[DataRequired(message='Home Page URL - This field is required.'),
                                        URL(message='Please enter valid web URL')])
    ach = StringField('ACH Descriptor', validators=[DataRequired(message='ACH Descriptor - This field is required.'),
                                                    Length(min=1, max=16),
                                                    Regexp('^\w+( +\w+)*$',
                                                           message="ACH Descriptor - Special Characters are not allowed")])
    qa_org = StringField('QA ORG ID',
                         validators=[DataRequired(message='QA ORG ID - This field is required.'), Length(min=3, max=3)])
    cert_org = StringField('INTQA/CERT ORG ID',
                           validators=[DataRequired(message='INTQA/CERT ORG ID - This field is required.'),
                                       Length(min=3, max=3)])
    stage_org = StringField('STAGE ORG ID', validators=[DataRequired(message='STAGE ORG ID - This field is required.'),
                                                        Length(min=3, max=3)])
    prod_org = StringField('PRODUCTION ORG ID',
                           validators=[DataRequired(message='PRODUCTION ORG ID - This field is required.'),
                                       Length(min=3, max=3)])
    pod = ['', 1, 2, 3, 4]
    pod_number = SelectField(label='POD Number', choices=pod,
                             validators=[DataRequired(message='POD Number - This field is required.')])
    cert_domain = StringField('CERT Domain URL',
                              validators=[DataRequired(message='CERT Domain URL - This field is required.'),
                                          URL(message='Please enter valid web URL')])
    prod_domain = StringField('PRODUCTION Domain URL',
                              validators=[DataRequired(message='PRODUCTION Domain URL - This field is required.'),
                                          URL(message='Please enter valid web URL')])
    danal = StringField('DANAL ID',
                        validators=[DataRequired(message='DANAL ID - This field is required.')])
    verid = StringField('VERID ACCOUNT NAME',
                        validators=[DataRequired(message='VERID ACCOUNT NAME - This field is required.')])
    domain = ['', 'true', 'false']
    custom_domain = SelectField(label='Custom Domain', choices=domain,
                                validators=[DataRequired(message='Custom Domain - This field is required.')])
    connectivity = ['', 'ESF', 'RTPService', 'DDAToPAN', 'DirectConnectPEPPlus', 'DirectConnectISO', 'FISProfile']
    instant_connectivity = SelectField(label='INSTANT CONNECTIVITY', choices=connectivity,
                                       validators=[
                                           DataRequired(message='INSTANT CONNECTIVITY - This field is required.')])


# Class Flask Form - RXP Zelle default setup.
class RxpZelleForm(FlaskForm):
    home_id = IntegerField(label='HOME_ID', validators=[DataRequired(message='Home ID - This field is required.'),
                                                        NumberRange(min=88830000, max=88839999,
                                                                    message="Incorrect Home ID length/Series.")])
    fi_name = StringField(label='FI NAME', validators=[DataRequired(message='FI NAME - This field is required.')])
    bug_id = IntegerField(label='BUG ID', validators=[DataRequired(message='BUG ID - This field is required.'),
                                                      NumberRange(min=200000, max=500000,
                                                                  message='Incorrect Bug Number, currently we are '
                                                                          'using bug number in 6 digit series.')])
    home_page = StringField('Home Page URL',
                            validators=[DataRequired(message='Home Page URL - This field is required.'),
                                        URL(message='Please enter valid web URL')])
    qa_org = StringField('QA ORG ID',
                         validators=[DataRequired(message='QA ORG ID - This field is required.'), Length(min=3, max=3)])
    cert_org = StringField('INTQA/CERT ORG ID',
                           validators=[DataRequired(message='INTQA/CERT ORG ID - This field is required.'),
                                       Length(min=3, max=3)])
    stage_org = StringField('STAGE ORG ID', validators=[DataRequired(message='STAGE ORG ID - This field is required.'),
                                                        Length(min=3, max=3)])
    prod_org = StringField('PRODUCTION ORG ID',
                           validators=[DataRequired(message='PRODUCTION ORG ID - This field is required.'),
                                       Length(min=3, max=3)])
    pod = ['', 1, 2, 3, 4]
    pod_number = SelectField(label='POD Number', choices=pod,
                             validators=[DataRequired(message='POD Number - This field is required.')])
    cert_domain = StringField('CERT Domain URL',
                              validators=[DataRequired(message='CERT Domain URL - This field is required.'),
                                          URL(message='Please enter valid web URL')])
    prod_domain = StringField('PRODUCTION Domain URL',
                              validators=[DataRequired(message='PRODUCTION Domain URL - This field is required.'),
                                          URL(message='Please enter valid web URL')])
    danal = StringField('DANAL ID',
                        validators=[DataRequired(message='DANAL ID - This field is required.')])
    domain = ['', 'true', 'false']
    custom_domain = SelectField(label='Custom Domain', choices=domain,
                                validators=[DataRequired(message='Custom Domain - This field is required.')])
    connectivity = ['', 'ESF', 'RTPService', 'DDAToPAN', 'DirectConnectPEPPlus', 'DirectConnectISO', 'FISProfile']
    instant_connectivity = SelectField(label='INSTANT CONNECTIVITY', choices=connectivity,
                                       validators=[
                                           DataRequired(message='INSTANT CONNECTIVITY - This field is required.')])


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"


@app.route("/")
def home():
    return render_template("index.html")


# RXP page
@app.route("/RXP", methods=["GET", "POST"])
def rxp_decommission():
    data_form = RxpForm()
    if request.method == "POST" and data_form.validate_on_submit():
        home_id = request.form.get('home_id')
        fi_name = request.form.get('fi_name')
        sponsor_id = request.form.get('sponsor_id')
        bug_id = request.form.get('bug_id')
        download_file = rxp_script(home_id, fi_name, sponsor_id, bug_id)
        return render_template('download.html', filename=download_file)
    return render_template('RXP.html', form=data_form)


# Script creation for RXP decommission
def rxp_script(home_id, fi_name, sponsor_id, bug_id):
    with open("sql_files/rxp.sql") as sql_file:
        file_contents = sql_file.read()
        new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(SPONSOR_ID,
                                                                                             sponsor_id).replace(BUG_ID,
                                                                                                                 bug_id)
        script_file = f"update_decommission_rxp_{home_id}_bug{bug_id}.sql"
        with open(script_file, mode="w") as completed_file:
            completed_file.write(new_file)
            return script_file


# COASP, DNA and Architect page/form
@app.route("/TN", methods=["GET", "POST"])
def tn_decommission():
    data_form = TnForm()
    if request.method == "POST" and data_form.validate_on_submit():
        home_id = request.form.get('home_id')
        fi_name = request.form.get('fi_name')
        bug_id = request.form.get('bug_id')
        if not home_id.startswith(('8812', '8814', '8811')):
            flash("Incorrect home id series.", "error")
        else:
            download_file = tn_script(home_id, fi_name, bug_id)
            return render_template('download.html', filename=download_file)
    return render_template('tn.html', form=data_form)


# Script creation for COASP, DNA and Architect decommission
def tn_script(home_id, fi_name, bug_id):
    with open("sql_files/tn.sql") as sql_file:
        file_contents = sql_file.read()
        new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(BUG_ID, bug_id)
        if home_id.startswith('8812'):
            script_file = f"update_decommission_coasp_{home_id}_bug{bug_id}.sql"
            with open(script_file, mode="w") as completed_file:
                completed_file.write(new_file)
                return script_file
        elif home_id.startswith('8814'):
            script_file = f"update_decommission_architect_{home_id}_bug{bug_id}.sql"
            with open(script_file, mode="w") as completed_file:
                completed_file.write(new_file)
                return script_file
        elif home_id.startswith('8811'):
            script_file = f"update_decommission_dna_{home_id}_bug{bug_id}.sql"
            with open(script_file, mode="w") as completed_file:
                completed_file.write(new_file)
                return script_file


# DI Page/Form
@app.route("/DI", methods=["GET", "POST"])
def di_decommission():
    data_form = DiForm()
    if request.method == "POST" and data_form.validate_on_submit():
        home_id = request.form.get('home_id')
        fi_name = request.form.get('fi_name')
        bug_id = request.form.get('bug_id')
        product = request.form.get('product')
        download_file = di_script(product, home_id, fi_name, bug_id)
        return render_template('download.html', filename=download_file)
    return render_template('DI.html', form=data_form)


# Script creation for DI decommission
def di_script(product, home_id, fi_name, bug_id):
    if product == 'TN_POP':
        with open("sql_files/di_tn_pop.sql") as sql_file:
            file_contents = sql_file.read()
            new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(BUG_ID, bug_id)
            script_file = f"update_decommission_di_tn_pop_{home_id}_bug{bug_id}.sql"
            with open(script_file, mode="w") as completed_file:
                completed_file.write(new_file)
                return script_file
    elif product == 'TN':
        with open("sql_files/di_tn.sql") as sql_file:
            file_contents = sql_file.read()
            new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(BUG_ID, bug_id)
            script_file = f"update_decommission_di_tn_{home_id}_bug{bug_id}.sql"
            with open(script_file, mode="w") as completed_file:
                completed_file.write(new_file)
                return script_file
    elif product == 'POP':
        with open("sql_files/di_pop.sql") as sql_file:
            file_contents = sql_file.read()
            new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(BUG_ID, bug_id)
            script_file = f"update_decommission_di_pop_{home_id}_bug{bug_id}.sql"
            with open(script_file, mode="w") as completed_file:
                completed_file.write(new_file)
                return script_file


# ROL Page/Form
@app.route("/ROL", methods=["GET", "POST"])
def rol_decommission():
    data_form = RolForm()
    if request.method == "POST" and data_form.validate_on_submit():
        home_id = request.form.get('home_id')
        fi_name = request.form.get('fi_name')
        bug_id = request.form.get('bug_id')
        rtn = request.form.get('rtn')
        download_file = rol_script(home_id, fi_name, rtn, bug_id)
        return render_template('download.html', filename=download_file)
    return render_template('rol.html', form=data_form)


# Script creation for ROL decommission
def rol_script(home_id, fi_name, rtn, bug_id):
    with open("sql_files/rol.sql") as sql_file:
        file_contents = sql_file.read()
        new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(RTN, rtn).replace(BUG_ID,
                                                                                                               bug_id)
        script_file = f"update_decommission_ro_{home_id}_bug{bug_id}.sql"
        with open(script_file, mode="w") as completed_file:
            completed_file.write(new_file)
            return script_file


## Custom validator
# def partner_id_check(form, partner_id):
#     partner_id = str(partner_id.data)
#     if len(partner_id) < 4 or len(partner_id) > 4:
#         raise ValidationError("Partner ID should be at most 4 digits")


# Zelle Page/Form
@app.route("/zelle", methods=["GET", "POST"])
def zelle():
    data_form = ZelleForm()
    if request.method == "POST" and data_form.validate_on_submit():
        download_file = zelle_script(request.form.get('home_id'), request.form.get('fi_name'),
                                     request.form.get('partner_id'),
                                     request.form.get('rtn'), request.form.get('bug_id'), request.form.get('csr_email'),
                                     request.form.get('reply_email'), request.form.get('csr_phone'),
                                     request.form.get('home_page'),
                                     request.form.get('ach'), request.form.get('qa_org'), request.form.get('cert_org'),
                                     request.form.get('stage_org'), request.form.get('prod_org'),
                                     request.form.get('pod_number'),
                                     request.form.get('cert_domain'), request.form.get('prod_domain'),
                                     request.form.get('danal'),
                                     request.form.get('verid'), request.form.get('custom_domain'),
                                     request.form.get('instant_connectivity'))
        return render_template('download.html', filename=download_file)
    return render_template('direct_zelle.html', form=data_form)


# Script creation for Zelle Default Setup
def zelle_script(home_id, fi_name, partner_id, rtn, bug_id, csr_email, reply_email, csr_phone, home_page, ach, qa_org,
                 cert_org, stage_org, prod_org, pod_number, cert_domain, prod_domain, danal, verid,
                 custom_domain, instant_connectivity):
    with open("sql_files/zelle_default.sql") as sql_file:
        file_contents = sql_file.read()
        new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(
            PARTNER_ID, partner_id).replace(RTN, rtn).replace(BUG_ID, bug_id).replace(CSR_EMAIL, csr_email).replace(
            REPLY_EMAIL, reply_email).replace(CSR_PHONE, csr_phone).replace(HOME_PAGE, home_page).replace(
            ACH, ach).replace(QA_ORG, qa_org).replace(CERT_ORG, cert_org).replace(STAGE_ORG, stage_org).replace(
            PROD_ORG, prod_org).replace(POD_NUMBER, pod_number).replace(CERT_DOMAIN, cert_domain).replace(
            PROD_DOMAIN, prod_domain).replace(DANAL, danal).replace(VERID, verid).replace(
            CUSTOM_DOMAIN, custom_domain).replace(CONNECTIVITY, instant_connectivity)
        script_file = f"enable_zelle_default_setup_{home_id}_bug{bug_id}.sql"
        with open(script_file, mode="w") as completed_file:
            completed_file.write(new_file)
            return script_file


# RXP Zelle Page/Form
@app.route("/rxp_zelle", methods=["GET", "POST"])
def rxp_zelle():
    data_form = RxpZelleForm()
    if request.method == "POST" and data_form.validate_on_submit():
        download_file = rxp_zelle_script(request.form.get('home_id'), request.form.get('fi_name'),
                                         request.form.get('bug_id'), request.form.get('home_page'),
                                         request.form.get('qa_org'), request.form.get('cert_org'),
                                         request.form.get('stage_org'), request.form.get('prod_org'),
                                         request.form.get('pod_number'),
                                         request.form.get('cert_domain'), request.form.get('prod_domain'),
                                         request.form.get('danal'),
                                         request.form.get('custom_domain'), request.form.get('instant_connectivity'))
        return render_template('download.html', filename=download_file)
    return render_template('rxp_zelle.html', form=data_form)


# Script creation for RXP Zelle Default Setup
def rxp_zelle_script(home_id, fi_name, bug_id, home_page, qa_org, cert_org, stage_org,
                     prod_org, pod_number, cert_domain, prod_domain, danal, custom_domain, instant_connectivity):
    with open("sql_files/rxp_zelle.sql") as sql_file:
        file_contents = sql_file.read()
        new_file = file_contents.replace(HOME_ID, home_id).replace(FI_NAME, fi_name).replace(BUG_ID, bug_id).replace(
            HOME_PAGE, home_page).replace(QA_ORG, qa_org).replace(CERT_ORG, cert_org).replace(
            STAGE_ORG, stage_org).replace(PROD_ORG, prod_org).replace(POD_NUMBER, pod_number).replace(
            CERT_DOMAIN, cert_domain).replace(PROD_DOMAIN, prod_domain).replace(DANAL, danal).replace(
            CUSTOM_DOMAIN, custom_domain).replace(CONNECTIVITY, instant_connectivity)
        script_file = f"enable_zelle_default_configurations_{home_id}_bug{bug_id}.sql"
        with open(script_file, mode="w") as completed_file:
            completed_file.write(new_file)
            return script_file


# Download page common for all
@app.route("/download/<download_filename>", methods=["GET", "POST"])
def download(download_filename):
    return send_file(download_filename, as_attachment=True)


if __name__ == "__main__":
    if cf_port is None:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)