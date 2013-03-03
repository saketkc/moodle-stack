from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib, re, getpass, os
login_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/login/index.php","2011":"http://moodle.iitb.ac.in/moodle2011/login/index.php"}
resource_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/mod/resource/index.php?id=","2011":"http://moodle.iitb.ac.in/moodle2009/mod/resource/index.php?id="}


resource_view_url = {"2009":"http://moodle.iitb.ac.in/moodle2009/mod/resource/","2011":"http://moodle.iitb.ac.in/moodle2009/mod/resource/"}

course_url={"2009":"http://moodle.iitb.ac.in/moodle2009/course/view.php?id=","2011":"http://moodle.iitb.ac.in/moodle2011/course/view.php?id="}

base_url = {"2009":"http://moodle.iitb.ac.in/moodle2009","2011":"http://moodle.iitb.ac.in/moodle2011"}

def moodle_updates(username,password):
	
	proxy_support=urllib2.ProxyHandler({})
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), proxy_support)
	login_data = urllib.urlencode({'username':username, 'password': password })
 	for year in login_url:
		print year
		opener.open(login_url[year], login_data)
		returnvalue=""
		url=opener.open(base_url[year])
		url=url.read()
		courses=re.compile('<a title="Click to enter this course" href="(.*)')
		list=courses.findall(str(url))

		for i in range(len(list)):
			course_code= list[i].split("\">")[0].split("=")[1]
			course_name= list[i].split("</a>")[0].split("\">")[1]
			c_url=course_url[year]+course_code
			r_url=resource_url[year]+course_code
		#print course_url
			if r_url:
				url_dump=opener.open(r_url)
				html=url_dump.read()
				soup=BeautifulSoup(html)
				table = soup.find('table',{"class":"generaltable boxaligncenter"})
#				print table,i
				if table:
					rows = table.findAll('tr')			
					for row in rows:
						tds = row.findAll('td')
						for td in tds:
							try:
								new_link = td.a['href']
								new_url = resource_view_url[year] + new_link							
								url_dump = opener.open(new_url)
							
								html = url_dump.read()
								generated_url = url_dump.geturl()
							
								#print generated_url
								if generated_url!=new_url:
									folderlocation = "/var/www/flask_app/"+str(year)+"/"+str(course_code)+"/"
									print folderlocation
									if not  os.path.exists(folderlocation):
										os.makedirs(folderlocation)
									filelocation = folderlocation + "/" + genrated_url.split('/')[-1]
		
									pdf = open(filelocation ,"wb")
									pdf.write(html)
									pdf.close()
								else:
									new_soup = BeautifulSoup(html)
							except:
								prit=1
			
			

	


moodle_updates('saket.kumar', 'whatsinaname.')
