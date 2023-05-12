# from django import template
# from forarmenians_app.models import LangTopMenuNav, LangProfileMenuNav, LangLogin, LangRegister
#
# register = template.Library()
#
#
# @register.simple_tag()
# def get_nav():
#     return LangTopMenuNav.objects.get(id=1)
#
#
# @register.simple_tag()
# def get_profile():
#     return LangProfileMenuNav.objects.get(id=1)
# 1
#
# @register.simple_tag()
# def get_log_in():
#     return LangLogin.objects.get(id=1)
#
#
# @register.simple_tag()
# def get_register():
#     return LangRegister.objects.get(id=1)
#
