import os

from groundwork.patterns import GwCommandsPattern
from groundwork_web.patterns import GwWebPattern
from competancy_mgt.patterns.compete_database_pattern.compete_database_pattern import CompeteDatabasePattern

from flask import request, redirect, url_for, session


class CompetencyMgtWebPlugin(CompeteDatabasePattern, GwWebPattern, GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)
        self.db = self.app.databases.get(self.app.config.get('CM_DATABASE_NAME'))

    def activate(self):
        static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "compete", "static")
        template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "compete", "templates")

        self.web.contexts.register("compete",
                                   template_folder=template_folder,
                                   static_folder=static_folder,
                                   url_prefix="/compete_mgt",
                                   description="context for the Competency management WUI")

        self.web.routes.register(url='/login', methods=["GET", "POST"], endpoint=self.__user_login, context="compete",
                                 name="compete_view", description="Login WUI for competency mgmt tool")

        self.web.routes.register(url='/index', methods=["GET", "POST"], endpoint=self.__index_page, context="compete",
                                 name="compete_view_index", description="Index WUI for competency mgmt tool")

        self.web.routes.register(url='/register', methods=["GET", "POST"], endpoint=self.__user_register,
                                 context="compete", name="compete_view_register", description="Registration Page")

        self.web.routes.register(url='/test1', methods=["GET"], endpoint=self.__test1, context="compete")
        self.web.routes.register(url='/update_res', methods=["GET", "POST"], endpoint=self.__update_resource,
                                 context="compete")

    def deactivate(self):
        pass

    def __test1(self):
        return self.web.render("charts.html")

    def __update_resource(self):
        method = request.method
        if method == "GET":
            return self.web.render("tables.html", user_name=session['username'], user_id=session['emp_id'],
                                   user_data=session)

    def __user_login(self):
        method = request.method
        if method == "GET":
            return self.web.render("login.html")
        if method == "POST":
            username = request.form['username']
            password = request.form['password']
            result = self.db.classes.get('Employee').clazz.query.filter_by(name=username).first()
            if result:
                if result.name == username:
                    fet_pass = self.db.classes.get('Access').clazz.query.filter_by(emp_id=result.emp_id).first()
                    if fet_pass.password == password:
                        session['emp_id'] = result.emp_id
                        session['username'] = result.name
                        session['access'] = result.authorization
                        return redirect(url_for('compete.__index_page'))
                    else:
                        return self.web.render("login.html", error="Wrong Password!")
            else:
                return self.web.render("login.html", error="User not registered!")

    def __user_register(self):
        method = request.method
        if method == "GET":
            return self.web.render("register.html")
        if method == "POST":
            username = request.form['username']
            pass1 = request.form['pass1']
            pass2 = request.form['pass2']
            emp_id = request.form['employeeID']
            emp_grade = request.form['employeeGrade']
            if pass1 != pass2:
                return self.web.render("register.html", error="Password doesn't match")
            else:
                self.db_import('Employee', emp_id=emp_id, name=username, grade=emp_grade, authorization='False')
                self.db_import('Access', emp_id=emp_id, password=pass1)
                return self.web.render("register.html", success="Account registered, Please go to the login page")

    def __index_page(self):
        method = request.method
        if method == 'GET':
            if session['emp_id'] != '':
                session['complete_table'], session['default_data'], session['emp_table'] = self.__fill_table(
                    emp_id=session['emp_id'])
                if session['access'] == 'True':
                    return self.web.render("index.html", user_name=session['username'], user_id=session['emp_id'],
                                           user_data=session)
                else:
                    return self.web.render("index.html", user_name=session['username'], user_id=session['emp_id'],
                                           user_data=session)
            else:
                return redirect(url_for('compete.__user_login'))
        else:
            language = self.db.classes.get('Language').clazz.query.filter_by(
                lang_name=request.form['languages']).first()
            practice = self.db.classes.get('Practices').clazz.query.filter_by(name=request.form['practice']).first()
            rdct = self.db.classes.get('RDCT').clazz.query.filter_by(rdct_name=request.form['rdct']).first()
            company = self.db.classes.get('Company').clazz.query.filter_by(text=request.form['Company']).first()
            micro = self.db.classes.get('Microcontroller').clazz.query.filter_by(
                text=request.form['Microcontroller']).first()
            tech = self.db.classes.get('Technology').clazz.query.filter_by(tech=request.form['Technology']).first()
            tools = self.db.classes.get('Tools').clazz.query.filter_by(text=request.form['Tools']).first()
            lvl = self.db.classes.get('levels').clazz.query.filter_by(val=request.form['levels']).first()

            offer_text = request.form['offering'] if len(request.form['offering']) > 0 else "N/A"
            self.db_import('Offering', text=offer_text)
            offering = self.db.classes.get('Offering').clazz.query.filter_by(text=offer_text).first()

            ps1_text = request.form['ps1'] if len(request.form['ps1']) > 0 else "N/A"
            self.db_import('Ps1', text=ps1_text)
            ps1 = self.db.classes.get('Ps1').clazz.query.filter_by(text=ps1_text).first()

            ps2_text = request.form['ps2'] if len(request.form['ps2']) > 0 else "N/A"
            self.db_import('Ps2', text=ps2_text)
            ps2 = self.db.classes.get('Ps2').clazz.query.filter_by(text=ps2_text).first()

            ps3_text = request.form['ps3'] if len(request.form['ps3']) > 0 else "N/A"
            self.db_import('Ps3', text=ps3_text)
            ps3 = self.db.classes.get('Ps3').clazz.query.filter_by(text=ps3_text).first()

            self.db_import('CompetencyHub', emp_id=int(session['emp_id']), emp_lang_id=language.id,
                           emp_practice_id=practice.id, emp_rdct_id=rdct.id, level=lvl.id, company_id=company.id,
                           micro_id=micro.id, tech_id=tech.id, tools_id=tools.id, offering_id=offering.id,
                           ps1_id=ps1.id, ps2_id=ps2.id, ps3_id=ps3.id)

            if session['emp_id'] != '':
                session['complete_table'], session['default_data'], session[
                    'emp_table'] = self.__fill_table(emp_id=session['emp_id'])
            else:
                return redirect(url_for('compete.__user_login'))
            return self.web.render("index.html", user_data=session, success="Data inserted successfully!")

    def db_import(self, table, override=False, **kwargs):
        """
        This will check if table is empty or not before entering data into it.

        :param table: Name of the table
        :param override: If to override the already present values in db
        :param kwargs: Fields of table
        :return: Database model reference of the given table.
        """

        result = self.db.classes.get(table).clazz.query.filter_by(**kwargs).first()
        if not result or override:
            result = self.db.classes.get(table).clazz(**kwargs)
            self.db.session.add(result)
            self.db.session.commit()
            self.log.info("Record Inserted!")

    def __fill_table(self, emp_id):
        table_content = {}
        default_vals = {}
        emp_table = {}
        result = self.db.classes.get('CompetencyHub').clazz.query.filter_by(emp_id=emp_id).all()

        default_data_lang = self.db.classes.get('Language').clazz.query.filter_by().all()
        default_data_practice = self.db.classes.get('Practices').clazz.query.filter_by().all()
        default_data_rdct = self.db.classes.get('RDCT').clazz.query.filter_by().all()
        default_data_levels = self.db.classes.get('levels').clazz.query.filter_by().all()
        default_data_company = self.db.classes.get('Company').clazz.query.filter_by().all()
        default_data_micro = self.db.classes.get('Microcontroller').clazz.query.filter_by().all()
        default_data_tech = self.db.classes.get('Technology').clazz.query.filter_by().all()
        default_data_tool = self.db.classes.get('Tools').clazz.query.filter_by().all()


        default_vals['practice'] = [practice.name for practice in default_data_practice]  #
        default_vals['Company'] = [comp.text for comp in default_data_company]
        default_vals['rdct'] = [rdct_.rdct_name for rdct_ in default_data_rdct]  #
        default_vals['languages'] = [lang.lang_name for lang in default_data_lang]  #
        default_vals['Microcontroller'] = [micro.text for micro in default_data_micro]
        default_vals['Technology'] = [tech.tech for tech in default_data_tech]
        default_vals['Tools'] = [tool.text for tool in default_data_tool]
        default_vals['levels'] = [level.val for level in default_data_levels]  #

        i = 0
        for row in result:
            table_content[i] = [row.prac.name, row.lang.lang_name, row.rdct.rdct_name, row.company.text, row.micro.text,
                                row.tech.tech, row.tools.text, row.offer.text, row.ps1.text, row.ps2.text, row.ps3.text,
                                row.lvl.val]
            i += 1

        all_info = self.db.classes.get('CompetencyHub').clazz.query.filter_by().all()

        i = 0
        for row in all_info:
            emp_table[i] = [row.emp.name, row.emp_id, row.emp.grade, row.prac.name, row.offer.text, row.rdct.rdct_name,
                            row.lang.lang_name, row.lvl.val, row.company.text, row.tools.text, row.micro.text,
                            row.tech.tech, row.ps1.text, row.ps2.text, row.ps3.text]
            i += 1

        return table_content, default_vals, emp_table
