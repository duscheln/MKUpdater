from PyQt5 import QtGui, uic
from PyQt5.QtCore import *

from ui.design import Ui_Dialog  # This file holds our MainWindow and all design related things
# it also keeps events etc that we defined in Qt Designer
import requests
from bs4 import BeautifulSoup
import re
import tablib
import json
import dateutil.parser as dparser

qtCreatorFile = "ui/design.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class UnitClubThread(QThread):

    progressText = pyqtSignal(str)

    def __init__(self,username,password):
        QThread.__init__(self)
        self.username = username
        self.password = password

    def __del__(self):
        self.wait()

    def run(self):

        # Unit-Club
        loginload = {
            'uid': self.username,
            'pwd': self.password
        }
        loginUrl = 'http://www.unit-club.net/up/unitclub/_login.php?'

        payload = {
            'doaction': 'loadnlfile',
            'btnsavenlfile': '   ***   Exportdatei hochladen   ***   ',
        }

        filetype = ['ph', 'ex', 'ta', 'tp', 'bs', 'sc']
        fileName = ['files/PeopleAndAdresses.xls',
                    'files/MonthlySales.xls',
                    'files/TeamAnalysisSales.xls',
                    'files/RecruitersCommission.xls',
                    'files/LadderOfSuccessCurrentQuarter.xls',
                    'files/LadderOfSuccessPreviousQuarter.xls']

        with requests.session() as c:
            self.progressText.emit('Connecting to Unit Club')
            #print('Connecting to Unit Club')

            # log in to website and get all the cookies
            loginResponse = c.post(loginUrl, data=loginload)
            self.progressText.emit(str(loginResponse.status_code))
            #print(str(loginResponse.status_code))
            peasoup = BeautifulSoup(c.get('http://www.unit-club.net/up/unitclub/_ps.php?').text, 'lxml')
            unitLink = peasoup.find('div', id='maintext').find_all('a', title='Zur eigenen Unit-Homepage wechseln')[0][
                'href']
            m = re.search('.*up\/(.*)\/wettbewerb.*', unitLink)
            if m:
                found = m.group(1)

            # prepare the payload indivdual to the corresponding files
            for i, number in enumerate(filetype):
                uploadUrl = 'http://www.unit-club.net/up/{}/_nlupload.php?nlupdatelogin={}&upload=1&'.format(found,
                                                                                                             number)
                # print(response.headers)
                payload['loadfiletype'] = number
                payload['nb_load{}'.format(number)] = 'true'
                self.progressText.emit('Uploading {}'.format(fileName[i]))
                #print('Uploading {}'.format(fileName[i]))
                uploadResponse = c.post(uploadUrl, files={'nlfile': open(fileName[i], 'rb')}, data=payload)
                self.progressText.emit(str(uploadResponse.status_code))
                #print(str(uploadResponse.status_code))
                soup = BeautifulSoup(uploadResponse.text, 'lxml')
                if 'erfolgreich geladen!' in soup.text:
                    self.progressText.emit('erfolgreich geladen!')

                del payload['nb_load{}'.format(number)]

            self.progressText.emit('Closing up the Unit Club Session!')

            c.close()

class InTouchThread(QThread):

    progressText = pyqtSignal(str)


    def __init__(self,username,password):
        QThread.__init__(self)
        self.username = username
        self.password = password

    def __del__(self):
        self.wait()

    def run(self):
        ## MaryKay Intouch
        startURL = 'https://www.marykayintouch.de'
        loginUrl = 'https://www.marykayintouch.de/Login/Login.aspx'
        self.progressText.emit('Läuft')
        #print('läuft')
        # define Username and Password
        loginload = {
            'txtConsultantID': self.username,
            'txtPassword': self.password,
            '__EVENTTARGET': 'btnSubmit'
        }

        url = []
        path = []
        payload = []

        # 'Adressen und Karrierestufen' is a GET Request
        adress_url = 'http://www.marykayintouch.de/InTouchWeb/myBusiness/api/Member/GetMemberData?dataType=Unit&_=14684277701' #&_=1468427770186
        # define header for excel file
        header = ('Linie',
                  'Unit',
                  'Länderkennzeichen',
                  'Consultantnummer',
                  'Nachname',
                  'Vorname',
                  'Aktivitätsstatus',
                  'Startdatum',
                  'Geburtsdatum',
                  'Level',
                  'Datum letzter Auftrag',
                  'Warenwert letzte Bestellung',
                  'Straße',
                  'Straße 2',
                  'Stadt',
                  'Staat',
                  'PLZ',
                  'Land',
                  'Mobilnummer',
                  'Festnetznummer',
                  'Arbeit',
                  'E-Mail',
                  'Anwerber/in',
                  'Anwerber/in Nachname',
                  'Anwerber/in Vorname',
                  # 'Startdatum',
                  # 'Datum letzter Auftrag',
                  # 'Warenwert letzte Bestellung',
                  'Level ID')

        excelData = tablib.Dataset()
        excelData.headers = header
        excelPath = 'files/PeopleAndAdresses.xls'

        # url.append('http://www.marykayintouch.de/InTouchWeb/myBusiness/api/Member/GetSelectedMembers?format=xls')
        # path.append('/Users/Lennart/PyCharmProjects/MaryKay_Updater/Adressen_Karrierestufen.xls')
        # payload.append({
        #     'ctl00$ContentPlaceHolder1$Default$DefaultUnit$ViewPanelHeader$CommandBar$CommandExport$ctl00' : 'Übersicht exportieren',
        #     'ctl00$ContentPlaceHolder1$Default$DefaultUnit$ViewPanelHeader$GridColumnPager1$ctl01$ctl00' :'Retail'
        # })

        # 'Monats Umsatz' is a POST Request
        url.append(
            'http://www.marykayintouch.de/InTouchWeb/Reports/Report.aspx?Path=/Sales_and_Recruiting/MonthlySales')
        path.append('files/MonthlySales.xls')
        payload.append({
            'ctl00$ContentPlaceHolder1$MonthlySales$MonthlySalesUnit$ViewPanelHeader$CommandBar$CommandExport$ctl00': 'Übersicht exportieren',
            'ctl00$ContentPlaceHolder1$MonthlySales$MonthlySalesUnit$ViewPanelHeader$ConfigFilter$CareerLevel$CareerLevel': 'Alle',
            # 'ctl00$ContentPlaceHolder1$MonthlySales$MonthlySalesUnit$ViewPanelHeader$ConfigFilter$ProductionYear$ProductionYear' : '01.07.2016 00:00:00',
            'ctl00$ContentPlaceHolder1$MonthlySales$MonthlySalesUnit$ViewPanelHeader$GridColumnPager1$ctl01$ctl00': 'Retail'
        })

        # 'Erfolgsleiter aktuelles Quartal' is a POST request
        url.append(
            'http://www.marykayintouch.de/InTouchWeb/Reports/Report.aspx?Path=/Contest_and_Challenges/LadderOfSuccessCurrentQuarter')
        path.append('files/LadderOfSuccessCurrentQuarter.xls')
        payload.append({
            'ctl00$ContentPlaceHolder1$LadderOfSuccessCurrentQuarter$LadderOfSuccessCurrentQuarterUnit$ViewPanelHeader$CommandBar$CommandExport$ctl00': 'Übersicht exportieren',
            # 'ctl00$ContentPlaceHolder1$LadderOfSuccessCurrentQuarter$LadderOfSuccessCurrentQuarterUnit$ViewPanelHeader$ConfigFilter$ProductionQuarter$ProductionQuarter' : '30.07.2016 23:59:59',
            'ctl00$ContentPlaceHolder1$LadderOfSuccessCurrentQuarter$LadderOfSuccessCurrentQuarterUnit$ViewPanelHeader$ConfigFilter$ReportingSubsidiaryCode$ReportingSubsidiaryCode': 'All'
        })
        # 'Erfolgsleiter vergangenes Quartal' is a POST request
        url.append(
            'http://www.marykayintouch.de/InTouchWeb/Reports/Report.aspx?Path=/Contest_and_Challenges/LadderOfSuccessPreviousQuarter')
        path.append('files/LadderOfSuccessPreviousQuarter.xls')
        payload.append({
            'ctl00$ContentPlaceHolder1$LadderOfSuccessPreviousQuarter$LadderOfSuccessPreviousQuarterUnit$ViewPanelHeader$CommandBar$CommandExport$ctl00': 'Übersicht exportieren',
            # 'ctl00$ContentPlaceHolder1$LadderOfSuccessPreviousQuarter$LadderOfSuccessPreviousQuarterUnit$ViewPanelHeader$ConfigFilter$QuarterStart$QuarterStart' : '30.04.2016 00:00:00',
            'ctl00$ContentPlaceHolder1$LadderOfSuccessPreviousQuarter$LadderOfSuccessPreviousQuarterUnit$ViewPanelHeader$ConfigFilter$ReportingSubsidiaryCode$ReportingSubsidiaryCode': 'All'
        })
        # 'Team-Umsatz' is a POST request
        url.append(
            'http://www.marykayintouch.de/InTouchWeb/Reports/Report.aspx?Path=/Sales_and_Recruiting/TeamAnalysisSales')
        path.append('files/TeamAnalysisSales.xls')
        payload.append({
            'ctl00$ContentPlaceHolder1$TeamAnalysisSales$TeamAnalysisSalesUnit$ViewPanelHeader$CommandBar$CommandExport$ctl00': 'Übersicht exportieren',
            'ctl00$ContentPlaceHolder1$TeamAnalysisSales$TeamAnalysisSalesUnit$ViewPanelHeader$ConfigFilter$CareerLevel$CareerLevel': 'Nicht Terminierte',
            # 'ctl00$ContentPlaceHolder1$TeamAnalysisSales$TeamAnalysisSalesUnit$ViewPanelHeader$ConfigFilter$ProductionYear$ProductionYear' : '01.07.2016 00:00:00',
            'ctl00$ContentPlaceHolder1$TeamAnalysisSales$TeamAnalysisSalesUnit$ViewPanelHeader$GridColumnPager1$ctl01$ctl00': 'Retail'
        })
        # 'Team-Provision' is a POST request
        url.append(
            'http://www.marykayintouch.de/InTouchWeb/Reports/Report.aspx?Path=/Monthly_and_Historical/RecruitersCommission')
        path.append('files/RecruitersCommission.xls')
        payload.append({
            'ctl00$ContentPlaceHolder1$RecruitersCommission$RecruitersCommissionUnit$ViewPanelHeader$CommandBar$CommandExport$ctl00': 'Übersicht exportieren',
            # 'ctl00$ContentPlaceHolder1$RecruitersCommission$RecruitersCommissionUnit$ViewPanelHeader$ConfigFilter$ProductionMonth$ProductionMonth' : '01.06.2016 00:00:00',
            'ctl00$ContentPlaceHolder1$RecruitersCommission$RecruitersCommissionUnit$ViewPanelHeader$ConfigFilter$ReportingSubsidiaryCode$ReportingSubsidiaryCode': 'All'
        })

        BackGroundInput = dict()

        with requests.session() as c:
            # get the start cookies of the session
            html = c.get(startURL)
            soup = BeautifulSoup(html.text, "lxml")

            # find all inputs to submit even the hidden ones
            for elem in soup.find('form').find_all('input', type='hidden'):
                BackGroundInput[elem['id']] = elem['value']

            # login to site with loginload as POST data
            self.progressText.emit('Login in to MaryKay Intouch')
            #print('Login in to MaryKay Intouch')

            BackGroundInput.update(loginload)
            response = c.post(loginUrl, data=BackGroundInput)
            hiddenResponse = c.get(startURL)
            BackGroundInput.clear()

            # GET 'Adressen und Karrierestufen'
            self.progressText.emit('Getting the Adresses List')
            #print('Getting the Adresses List')

            adresses = c.get(adress_url)
            self.progressText.emit(str(adresses.status_code))
            #print(str(adresses.status_code))

            if adresses.status_code == 200:
                self.progressText.emit('Access granted!')
                #print('Access granted!')

                json_format = BeautifulSoup(adresses.text, 'lxml').get_text()
                json_data = json.loads(json_format)

                for ii, elem in enumerate(json_data):
                    excelData.append(
                        ['', elem['UnitNumber'],
                         elem['SubsidiaryCode'],
                         elem['ConsultantID'],
                         elem['LastName'],
                         elem['FirstName'],
                         elem['ConsultantStatus'],
                         dparser.parse(elem['StartDate'], fuzzy=True).strftime('%d.%m.%Y'),
                         elem['DisplayBirthDate'],
                         elem['ConsultantLevelDesc'],
                         elem['DisplayLastOrderDate'],
                         elem['DisplayLastOrderRetail'],
                         elem['Address1'],
                         elem['Address2'],
                         elem['Address3'],
                         elem['Address4'],
                         elem['Address5'],
                         elem['AddressCountry'],
                         elem['FormattedPhoneMobile'],
                         elem['FormattedPhoneHome'],
                         elem['FormattedPhoneBusiness'],
                         elem['EmailAddressPersonal'],
                         elem['RecruiterConsultantNumber'],
                         elem['RecruiterLastName'],
                         elem['RecruiterFirstName'],
                         # dparser.parse(elem['StartDate'], fuzzy=True).strftime('%d.%m.%Y %H:%M:%S'),
                         # dparser.parse(elem['LastOrderDate'],fuzzy=True).strftime('%d.%m.%Y %H:%M:%S'),
                         # elem['LastOrderRetail'],
                         elem['ConsultantLevelID']])
                self.progressText.emit('Writing file to {}'.format(excelPath))
                #print('Writing file to {}'.format(excelPath))

                with open(excelPath, 'wb') as f:
                    f.write(excelData.xls)
                self.progressText.emit('Done...!')
                #print('Done...!')

            # POST Requests to urls
            for jj, element in enumerate(url):
                response = c.get(element)
                soup = BeautifulSoup(response.text, 'lxml')

                for hiddenelem in soup.find('form').find_all('input', type='hidden'):
                    BackGroundInput[hiddenelem['id']] = hiddenelem['value']

                payload[jj][soup.find('select')['name']] = \
                    soup.find('select').find_all('option', selected='selected')[0]['value']
                # print(soup.find('select').find_all('option', selected='selected')[0]['value'])
                self.progressText.emit('Getting information for {}'.format(path[jj]))
                #print('Getting information for {}'.format(path[jj]))

                BackGroundInput.update(payload[jj])
                data = c.post(element, data=BackGroundInput)
                self.progressText.emit(str(data.status_code))
                #print(str(data.status_code))

                if data.status_code == 200:
                    self.progressText.emit('Writing file to {}'.format(path[jj]))
                    #print('Writing file to {}'.format(path[jj]))

                    with open(path[jj], 'wb') as f:

                        for chunk in data:
                            f.write(chunk)
                    self.progressText.emit('Done ... !')
                    #print('Done...!')


                else:
                    self.progressText.emit('an error occured getting {}'.format(path[jj]))
                    #print('an error occured getting {}'.format(path[jj]))

                BackGroundInput.clear()
            self.progressText.emit('Done ... Closing up the InTouch Session.')
            #print('Done ... Closing up the InTouch Session.')

            c.close()


class ExampleApp(Ui_Dialog):
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)

        self.setupUi(dialog)

        self.unitClubBtn.clicked.connect(self.unitClub)
        self.inTouchBtn.clicked.connect(self.inTouch)

    def unitClub(self):

        username = self.userNametxt.text()
        password = self.passwordtxt.text()
        if not username:
            if not password:
                self.plainTextEdit.appendHtml('<font color="red">no password and username provided</font>')
                QtGui.QGuiApplication.processEvents()
                return
            else:
                self.plainTextEdit.appendPlainText('no username provided')
                QtGui.QGuiApplication.processEvents()
                return
        else:
            if not password:
                if username == 'default':
                    import credentials
                    username = credentials.unitClub['username']
                    password = credentials.unitClub['password']
                    self.get_thread = UnitClubThread(username, password)
                    self.get_thread.start()
                    self.get_thread.progressText.connect(self.updateBox)




                self.plainTextEdit.appendPlainText('no password provided')
                QtGui.QGuiApplication.processEvents()
                return
            else:
                self.get_thread = UnitClubThread(username, password)
                self.get_thread.start()

    def updateBox(self,str):
        self.plainTextEdit.appendPlainText(str)
        return

    def done(self):
        self.plainTextEdit.appendPlainText('no password provided')
        return

    def inTouch(self):

        username = self.userNametxt.text()
        password = self.passwordtxt.text()
        if not username:
            if not password:
                self.plainTextEdit.appendHtml('<font color="red">no password and username provided</font>')
                QtGui.QGuiApplication.processEvents()
                return
            else:
                self.plainTextEdit.appendPlainText('no username provided')
                QtGui.QGuiApplication.processEvents()
                return
        else:
            if not password:
                if username == 'default':
                    import credentials
                    username = credentials.inTouch['username']
                    password = credentials.inTouch['password']
                    self.get_thread = InTouchThread(username, password)
                    self.get_thread.start()
                    self.get_thread.progressText.connect(self.updateBox)



                self.plainTextEdit.appendPlainText('no password provided')
                QtGui.QGuiApplication.processEvents()
                return
            else:
                self.get_thread = InTouchThread(username, password)
                self.get_thread.start()
                self.get_thread.progressText.connect(self.updateBox)


