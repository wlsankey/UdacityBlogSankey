import os
import jinja2
import webapp2

from google.appengine.ext import db


#SETUP Jinja Environment
"""Sets Jinja2 environment for files and templates and 
also establishes file directory location.
"""
template_directory = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_directory), autoescape = True)


#Function in Handler class very useful for rendering basic templates

class Handler(webapp2.RequestHandler):
	def write (self, *a, **kw):
		self.response.write(*a, **kw)
	#Add self.response.write.out(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))
	
class MainHandler(Handler):
	def get(self):
		self.render("blog_page.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			self.write("Very good grasshooper!")
			
		else:
			error = "Please include both a title and a blog post."
			self.render("blog_page.html", error = error)
		
#class MainHandler(webapp2.RequestHandler):
#    def get(self):
#		self.response.headers['Content-Type'] = 'text/plain'
#		self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
