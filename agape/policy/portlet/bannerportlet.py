from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from agape.policy import MessageFactory as _
#from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from Acquisition import aq_inner, aq_parent


class IBannerPortlet(IPortletDataProvider):
    
    
    banner_text = schema.Text(
        title = u"Banner Text",
        required = True
    )
    
    banner_image_source = schema.TextLine(
        title = u"URL of Image",
        required = True,
    )
    

class Assignment(base.Assignment):
    implements(IBannerPortlet)
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    @property
    def title(self):
        return 'Banner Portlet'
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/bannerportlet.pt')
    
    def is_default_page(self, parent, curr_content):
        view = getMultiAdapter((parent, self.request), name='default_page')
        return view.isDefaultPage(curr_content)
    
    def filter_portlet(self):
        portlet_key = self.__portlet_metadata__['key']
        context = self.context
        
        
        if portlet_key == '/'.join(self.context.getPhysicalPath()):
            return True
        else:
            parent_folder = aq_parent(aq_inner(self.context))
            parent_path = '/'.join(parent_folder.getPhysicalPath())
            
            
            if self.is_default_page(parent_folder, self.context):
                path1 = aq_parent(aq_inner(self.context)).getPhysicalPath()
                if (len(path1)) in [4,5]:
                    return True
            
        return False
    
    def banner_txt(self):
        return self.data.banner_text
    
    def banner_img(self):
        return self.data.banner_image_source
    

class AddForm(base.AddForm):
    form_fields = form.Fields(IBannerPortlet)
    form_fields['banner_text'].custom_widget = WYSIWYGWidget
    label = u"Add Banner Portlet"
    
    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.fields(IBannerPortlet)
    form_fields['banner_text'].custom_widget = WYSIWYGWidget
    label = u"Edit Banner Portlet"
    
    