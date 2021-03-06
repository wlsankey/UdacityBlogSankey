import os
import jinja2
import webapp2
import re

from google.appengine.ext import db


#SETUP Jinja Environment
"""Sets Jinja2 environment for files and templates and 
also establishes file directory location.
"""
template_directory = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_directory), autoescape = True)



class BlogPost(db.Model):
	title = db.StringProperty(required = True)
	blog_content = db.TextProperty(required = True)
	post_time = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)
	
	
class Handler(webapp2.RequestHandler):
	def write (self, *a, **kw):
		self.response.write(*a, **kw)
	#Add self.response.write.out(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
	
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class OpeningPageHandler(Handler):
	def render_front(self, subject = "", content = ""):
		db_cursor = db.GqlQuery("SELECT * FROM BlogPost ORDER BY post_time DESC limit 10")
		self.render("home_page.html", blog_post=db_cursor)
	
	def get(self):
		self.render_front()
		
	
class BlogInputHandler(Handler):
	def render_front(self, subject = "", content = "", error = ""):
		db_cursor = db.GqlQuery("SELECT * FROM BlogPost ORDER BY post_time DESC")
		self.render("blog_page.html", subject=subject, content=content, error=error, blog_post=db_cursor)
		
	
	def get(self):
		self.render_front()

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")#.replace('\n', '\<br>')

		if subject and content:
			instance = BlogPost(title=subject, blog_content=content)
			instance.put()
			post_key = str(instance.key().id())
			self.redirect("/blog/%s" %post_key)
			
			
		else:
			error = "Please include both a title and a blog post."
			self.render_front(subject, content, error)
			
class PostPageHandler(Handler):
	def get(self, post_id):
		post_id = int(post_id)
		post = BlogPost.get_by_id(post_id)
		if post:
			self.render("permalink.html", post=post)
		else:
			self.write("This page does not exist.")


app = webapp2.WSGIApplication([
    ('/', BlogInputHandler),
	('/home', OpeningPageHandler),
	('/blog', OpeningPageHandler),
	('/blog/([0-9]+)', PostPageHandler),
	], debug=True)
