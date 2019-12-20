import os

from groundwork.patterns import GwCommandsPattern
from groundwork_web.patterns import GwWebPattern
from competancy_mgt.patterns.compete_database_pattern.compete_database_pattern import CompeteDatabasePattern
import competancy_mgt.patterns.compete_database_pattern.models

from flask import request, redirect, url_for


class CompetencyMgtWebPlugin(CompeteDatabasePattern, GwWebPattern, GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)
        self.loggedin_username = ''
        self.loggedin_user_id = ''
        self.access_rights = ''
        self.db = self.app.databases.get(self.app.config.get('CM_DATABASE_NAME'))
        self.user_data = {'username': self.loggedin_username, 'emp_id': self.loggedin_user_id, "access": 'False',
                     "complete_table": {}, "default_data": {}}


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
        self.web.routes.register(url='/update_res', methods=["GET", "POST"], endpoint=self.__update_resource, context="compete")

    def deactivate(self):
        pass

    def __test1(self):
        return self.web.render("charts.html")

    def __update_resource(self):
        method = request.method
        if method == "GET":

            return self.web.render("tables.html", user_data=self.user_data)

    def __user_login(self):
        self.loggedin_user_id = ''
        self.loggedin_username = ''
        self.access_rights = ''
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
                        self.user_data['emp_id'] = result.emp_id
                        self.user_data['username'] = result.name
                        self.user_data['access'] = result.authorization
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
            if pass1 != pass2:
                return self.web.render("register.html", error="Password doesn't match")
            else:
                self.db_import('Employee', emp_id=emp_id, name=username)
                self.db_import('Access', emp_id=emp_id, password=pass1)
                return self.web.render("register.html", success="Account registered, Please go to the login page")

    def __index_page(self):
        method = request.method
        if method == 'GET':
            if self.user_data['emp_id'] != '':
                self.user_data['complete_table'], self.user_data['default_data'] = self.__fill_table(emp_id=self.user_data['emp_id'])
                if self.access_rights == 'True':
                    self.user_data['access'] = 'True'
                    print(self.user_data)
                    return self.web.render("index.html", user_data=self.user_data)
                else:
                    self.user_data['access'] = 'False'
                    return self.web.render("index.html", user_data=self.user_data)
            else:
                return redirect(url_for('compete.__user_login'))
        else:
            language = self.db.classes.get('Language').clazz.query.filter_by(lang_name=request.form['languages']).first()
            practice = self.db.classes.get('Practices').clazz.query.filter_by(name=request.form['practice']).first()
            rdct = self.db.classes.get('RDCT').clazz.query.filter_by(rdct_name=request.form['rdct']).first()
            lvl = self.db.classes.get('levels').clazz.query.filter_by(val=request.form['levels']).first()

            self.db_import('CompetencyHub', emp_id=int(self.user_data['emp_id']), emp_lang_id=language.id, emp_practice_id=practice.id, emp_rdct_id=rdct.id, level=lvl.id)
            if self.user_data['emp_id'] != '':
                self.user_data['complete_table'], self.user_data['default_data'] = self.__fill_table(emp_id=self.user_data['emp_id'])
            else:
                return redirect(url_for('compete.__user_login'))
            return self.web.render("index.html", user_data=self.user_data, success="Data inserted successfully!")

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
        result = self.db.classes.get('CompetencyHub').clazz.query.filter_by(emp_id=emp_id).all()

        default_data_lang = self.db.classes.get('Language').clazz.query.filter_by().all()
        default_data_practice = self.db.classes.get('Practices').clazz.query.filter_by().all()
        default_data_rdct = self.db.classes.get('RDCT').clazz.query.filter_by().all()
        default_data_levels = self.db.classes.get('levels').clazz.query.filter_by().all()

        default_vals['languages'] = [lang.lang_name for lang in default_data_lang]
        default_vals['practice'] = [practice.name for practice in default_data_practice]
        default_vals['rdct'] = [rdct_.rdct_name for rdct_ in default_data_rdct]
        default_vals['levels'] = [level.val for level in default_data_levels]

        i = 0
        for row in result:
            table_content[i] = [row.prac.name, row.lang.lang_name, row.rdct.rdct_name, row.lvl.val]
            i += 1

        return table_content, default_vals
