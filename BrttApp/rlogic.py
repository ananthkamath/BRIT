#importing required python libraries
import os
import subprocess
import xlrd
import xlwt
import os.path
import socket
from urlparse import urlsplit, urlunsplit
from semail import send_email
import datetime
import urllib2
import urllib3

def rlogic_fun(xlname,email_id,esn):
    input = xlrd.open_workbook(xlname)
    input.sheet_names()
    #Choose the first sheet
    sh = input.sheet_by_index(0)
    #Choose the encoding format for output Excel Sheet and Name for the sheet
    output = xlwt.Workbook(encoding="utf-8")
    sw = output.add_sheet("sheet 1")
    #Enter the headings in the output Excel Sheet
    row=1
    col=0
    styleg=xlwt.easyxf('font:color-index green, bold on')
    styler=xlwt.easyxf('font:color-index red, bold on')
    styleb=xlwt.easyxf('font:color-index black, bold on')
    sw.write( 0, 0, 'Redirected From' , styleb)
    sw.write( 0, 1, 'Expected Redirect', styleb )
    sw.write( 0, 2, 'Actual Redirect', styleb )
    sw.write( 0, 3, 'Result', styleb )
    sw.write( 0, 4, 'Status', styleb )
    sw.write( 0, 5, 'Server', styleb )
    #Initialize the success and failure counts
    success=0
    failure=0
    #Take the number of redirects as Input convert it into Integer
    INT_NUMBER_OF_REDIRECTS = sh.nrows - 1
    print INT_NUMBER_OF_REDIRECTS
    #Spoof the urls to the required Akamai Environment
    #SPOOF = 'e1.a.akamaiedge-staging.net'
    SPOOF = esn
    http = urllib3.PoolManager()
    #Read every row from the input excel and write the corresponding out put into the buffer
    for row in range(1,( INT_NUMBER_OF_REDIRECTS+1 )):
        #Spoof the urls to the required Akamai Environment
        surl = list(urlsplit(sh.cell( row, col ).value))
        host_header = surl[1]
        surl[1] = SPOOF
        usurl = urlunsplit(surl)
        print usurl
        headers = {'Host':host_header}
        print host_header
        r = http.request('GET',usurl,headers=headers,retries=False)
        try:
		var = r.headers['location']
	except Exception:
		var = "The url is currently not getting redirected, please test manually !!"
        print "location is:" + var
        try:
                rserver = r.headers['server']
        except Exception:
                rserver = "No server header found in response!!"
        try:
                rstatus = str(r.status)
        except Exception:
                rstatus = "Did not get any status from server!!"
        if sh.cell( row, col+1 ).value == var:
                sw.write( row, col, sh.cell( row, col ).value, styleg )
                sw.write( row, col+1, sh.cell( row, col+1 ).value, styleg )
                sw.write( row, col+2, var, styleg )
                sw.write( row, col+3, 'True', styleg)
                sw.write( row, col+4, rstatus, styleg)
                sw.write( row, col+5, rserver, styleg)
                success = success + 1
        else:
                sw.write( row, col, sh.cell( row, col ).value, styler )
                sw.write( row, col+1, sh.cell( row, col+1 ).value, styler )
                sw.write( row, col+2, var, styler )
                sw.write( row, col+3, 'False', styler )
                sw.write( row, col+4, rstatus, styler )
                sw.write( row, col+5, rserver, styler )
                failure = failure + 1
        row = row + 1
    sw.write( 0, 7, 'Success', styleg )
    sw.write( 1, 7, success, styleg )
    sw.write( 0, 8, 'Failure', styler )
    sw.write( 1, 8, failure, styler )
    print "YOU WILL FIND THE TESTING RESULTS IN RESULTS.XLS FILE"
    rfile = datetime.datetime.now().isoformat() + "results.xls"
    #srfile = "/var/www/FlaskApps/BrttApp/static/" + rfile
    srfile = "/var/tmp/" + rfile
    #output.save(rfile)
    #srfile = "/var/tmp" + rfile
    output.save(srfile)
    #print rfile
    #print srfile
    send_email(srfile,email_id)
    #cpcmd = "cp " + rfile + " static"
    #print cpcmd
    #os.system( cpcmd )
    orfile = "/static/results/" + rfile
    result = [success,failure,orfile]
    return result
