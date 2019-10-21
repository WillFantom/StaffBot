import logging
import random
import os
import json
import time
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from flask import Flask, Response, request

# Grabber
class StaffbotGrabber():

    __STAFF_URL = "https://www.lancaster.ac.uk/scc/about-us/people/"

    def __init__(self, logger):
        ''' create a staffbot grabber '''
        self.logger = logger
        self.logger.info("Creating staffbot grabber | ")
        self.__staff_list = []
        self.__build_list()
        self.logger.info("Created staffbot grabber | ok")
        
    def __build_list(self, rebuild=False):
        ''' build the initial staff list '''
        self.logger.info("Building Staff List")
        webpage = None
        try:
            webpage = self.__get_webpage()
        except:
            if rebuild == True:
                return 1
            else:
                time.sleep(10)
                self.__build_list()
        soup = BeautifulSoup(webpage, 'html.parser')
        academic_html = soup.findAll('div', attrs={'data-categories':'academic'})
        professional_html = soup.findAll('div', attrs={'data-categories':'professional'})
        research_html = soup.findAll('div', attrs={'data-categories':'research'})
        staff_html = academic_html + professional_html + research_html
        staff_list_tmp = []
        for member in staff_html:
                member_img = member.find('img')
                staff_list_tmp.append(
                    { 
                        "name": member_img['alt'],
                        "img_url": member_img['data-src']
                    }
                )
        self.__staff_list = staff_list_tmp
        self.logger.info("Staff list length | {}".format(len(self.__staff_list)))
        return 0

    def __get_webpage(self):
        ''' get the staff webpage '''
        url = self.__STAFF_URL
        content = urlopen(url).read()
        return str(content)

    def get(self, name=None):
        ''' get a staff member '''
        if len(self.__staff_list) == 0:
            return None
        if not name == None:
            for member in self.__staff_list:
                if member.get("name") == name:
                    return member
            return None
        return random.choice(self.__staff_list)

    def rebuild_list(self):
        ''' rebuild the staff list '''
        return self.__build_list(rebuild=True)

# Setup
secret_key = os.environ['SECRET_KEY']
debug_mode = int(os.environ['DEBUG'])
if debug_mode > 0:
    log_lvl = logging.DEBUG
else:
    log_lvl = logging.ERROR
logging.basicConfig(stream=sys.stdout, level=log_lvl)
grabber_logger = logging.getLogger('StaffBot-Grabber')
staffbot_grabber = StaffbotGrabber(grabber_logger)

# API
logger = logging.getLogger('StaffBot-API')
API_VERSION = os.environ['API_VERSION']
app = Flask(__name__)

@app.route('/v'+str(API_VERSION)+'/get_member')
def get_member():
    ''' get a staff member '''
    logger.info("Request for staff member info")
    name = request.args.get('name', None)
    if not name == None:
        logger.info("Request searching for staff member " + name)
    staff_member = staffbot_grabber.get(name=name)
    if staff_member == None:
        return Response(json.dumps({'Error': 'Staff member not found'}), 
                        status=404, 
                        mimetype='application/json')
    return Response(json.dumps(staff_member), 
                        status=200, 
                        mimetype='application/json')

@app.route('/v'+str(API_VERSION)+'/rebuild')
def rebuild_list():
    ''' rebuild the list of staff members '''
    logger.info("Request to rebuild stafflist")
    key = request.args.get('key', None)
    if not key == secret_key:
        return Response(json.dumps({'Error': 'Invalid key'}), 
                        status=403,
                        mimetype='application/json')
    return_code = staffbot_grabber.rebuild_list()
    if return_code == 0:
        return Response(json.dumps({'Success': 'Stafflist rebuilt'}), 
                        status=200, 
                        mimetype='application/json')
    return Response(json.dumps({'Error': 'Failed to rebuild list'}), 
                    status=500, 
                    mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)