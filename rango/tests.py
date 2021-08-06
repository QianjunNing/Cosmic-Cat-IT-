import os
import rango.models
from django.test import TestCase
from django.urls import reverse
from populate_rango import populate
from django.contrib.auth.models import User
from django.forms import fields as django_fields

from rango import forms
from rango.models import Page, Category, UserComment
# from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, CommentForm



FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"

class SearchCategoryPageTests(TestCase):
    """
    A series of tests to ensure that the search category page/view has been updated to work with templates.
    """
    def setUp(self):
        self.response = self.client.get(reverse('rango:search_category'))
    
    def test_search_category_template(self):
        """
        Checks whether the search category view uses a template
        """
        self.assertTemplateUsed(self.response, 'rango/search_category.html', f"{FAILURE_HEADER}Your search_category() view does not use the expected template.{FAILURE_FOOTER}")
    
   
    def test_search_category_starts_with_doctype(self):
        """
        Is the <!DOCTYPE html> declaration on the first line of the search_category.html template?
        """
        self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your search_category.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
    
   
class SearchPageTests(TestCase):
    """
    A series of tests to ensure that the search page/view has been updated to work with templates.
    """
    def setUp(self):
        self.response = self.client.get(reverse('rango:search'))
    
    def test_search_template(self):
        """
        Checks whether the search view uses a template
        """
        self.assertTemplateUsed(self.response, 'rango/search.html', f"{FAILURE_HEADER}Your search() view does not use the expected template.{FAILURE_FOOTER}")
    
   
    def test_search_starts_with_doctype(self):
        """
        Is the <!DOCTYPE html> declaration on the first line of the search.html template?
        """
        self.assertTrue(self.response.content.decode().startswith('<!DOCTYPE html>'), f"{FAILURE_HEADER}Your search.html template does not start with <!DOCTYPE html> -- this is requirement of the HTML specification.{FAILURE_FOOTER}")
 

class StaticCssTests(TestCase):
    """
    A series of tests to check whether css files has been setup and used correctly.
   
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        
    
    def test_does_static_directory_exist(self):
        """
        Tests whether the static directory exists in the correct location -- and the css subdirectory.
        
        """
        does_static_dir_exist = os.path.isdir(self.static_dir)
        does_css_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'css'))
        does_js_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'js'))
        
        self.assertTrue(does_static_dir_exist, f"{FAILURE_HEADER}The static directory was not found in the expected location. Check  and try again.{FAILURE_FOOTER}")
        self.assertTrue(does_css_static_dir_exist, f"{FAILURE_HEADER}The css subdirectory was not found in your static directory.{FAILURE_FOOTER}")
        self.assertTrue(does_js_static_dir_exist, f"{FAILURE_HEADER}The js subdirectory was not found in your static directory.{FAILURE_FOOTER}")



def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user    

class UsercommentModelTests(TestCase):
    """
    Tests to check whether the Usercomment model has been created according to the specification.
    """
   
    
    def test_Usercomment_class(self):
        """
        Does the Usercomment class exist in rango.models?
        """
        self.assertTrue('UserComment' in dir(rango.models))
    def test_link(self):
        populate()
        content = self.client.get(reverse('rango:show_category',kwargs={'category_name_slug': 'python'})).content.decode()

        self.assertTrue( '<form id="comment_form">'not in content, f"{FAILURE_HEADER}The comment was present on category page when a user is not logged in. This shouldn't be the case! Please check.{FAILURE_FOOTER}")
        
        
    
     