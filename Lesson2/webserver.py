from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# use webserverHandler to respond to different status codes
class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # get method for edit page
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myResuaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myResuaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>"
                    output += myResuaurantQuery.name
                    output += "</h1>"
                    output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type ='text' placeholder='%s'>" % myResuaurantQuery.name
                    output += "<input type ='submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)

            # get method for resturants page
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

        	# get method for creating a new restaurant page
        	if self.path.endswith("/restaurants/new"):
        		self.send_response(200)
        		self.send_header('Content-type', 'text/html')
        		self.end_headers()
        		output = ""
        		output += "<html><body>"
        		output += "<h1>Make a New Restaurant</h1>"
        		output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'><input name ='newRestaurantName' type='text' placeholder='Give me a new restaurant!'><input type = 'submit' value='Create'></form>"
        		output += "</body></html>"
        		self.wfile.write(output)
        		print output
        		return

        	


        	# if self.path.endswith("/hello"):
         #        self.send_response(200)
         #        self.send_header('Content-type', 'text/html')
         #        self.end_headers()
         #        output = ""
         #        output += "<html><body>"
         #        output += "<h1>Hello!</h1>"
         #        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
         #        output += "</body></html>"
         #        self.wfile.write(output)
         #        print output
         #        return

         #    if self.path.endswith("/hola"):
         #        self.send_response(200)
         #        self.send_header('Content-type', 'text/html')
         #        self.end_headers()
         #        output = ""
         #        output += "<html><body>"
         #        output += "<h1>&#161 Hola !</h1>"
         #        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
         #        output += "</body></html>"
         #        self.wfile.write(output)
         #        print output
         #        return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantIDPath = self.path.split('/')[2]

                myResuaurantQuery = session.query(Restaurant).filter_by(restaurantIDPath).one()
                if myResuaurantQuery:
                    myResuaurantQuery.name = messagecontent[0]
                    session.add(myResuaurantQuery)
                    session.commit()

                    # redirect to resturants page
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            # post method for creating new restaurants 

        	if self.path.endswith('/restaurants/new'):
        		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        		if ctype == 'multipart/form-data':
        			fields = cgi.parse_multipart(self.rfile, pdict)
        		messagecontent = fields.get('newRestaurantName')

        		# Create new Restaurant class
        		newRestaurant = Restaurant(name=messagecontent[0])
        		session.add(newRestaurant)
        		session.commit()

        		self.send_response(301)
        		self.send_header('Content-type', 'text/html')
        		self.send_header('Location', '/restaurants')
        		self.end_headers()


            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # ctype, pdict = cgi.parse_header(
            #     self.headers.getheader('content-type'))
            # if ctype == 'multipart/form-data':
            #     fields = cgi.parse_multipart(self.rfile, pdict)
            #     messagecontent = fields.get('message')
            # output = ""
            # output += "<html><body>"
            # output += " <h2> Okay, how about this: </h2>"
            # output += "<h1> %s </h1>" % messagecontent[0]
            # output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            # output += "</body></html>"
            # self.wfile.write(output)
            # print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()