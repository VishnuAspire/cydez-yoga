from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
urlpatterns = [
     #templates

    path('addProgram',views.addProgram,name='add_program'),
    path('listprogram',views.listProgram,name='list_program'),
    path('editProgram<int:userid>',views.editProgram,name="editProgram"),
    path('deleteProgram',views.deleteProgram,name="deleteProgram"),
    path('addCategory',views.addCategory,name='add_category'),
    path('listCategory',views.listCategory,name='list_category'),
    path('addLevel',views.addLevel,name='add_level'),
    path('listlevel',views.listLevel,name='list_level'),
    path('editLevel<int:userid>',views.editLevel,name="editLevel"),
    path('editCategory<int:userid>',views.editCategory,name="editCategory"),
    path('deleteLevel<int:userid>',views.deleteLevel,name="deleteLevel"),
    path('deleteCategory',views.deleteCategory,name="deleteCategory"),
    path('listSlides',views.listSlides,name='list_slides'),
    path('addSlides',views.addSlides,name='add_slides'),
    path('editSlides<int:userid>',views.editSlides,name="editSlides"),
    path('deleteSlides<int:userid>',views.deleteSlides,name="deleteSlides"),
    path('searchProgram',views.searchProgram,name='searchProgram'),
    path('searchCategory',views.searchCategory,name='searchCategory'),
    path('searchLevel',views.searchLevel,name='searchLevel'),
    path('searchSlide',views.searchSlide,name='searchSlide'),

    #apiview
    path('listofprograms',views.listofprograms, name='listofprograms'),
    path('listoforder',views.listoforder, name='listoforder'),
    path('listofslides',views.listofslides, name='listofslides'),
    path('listofcategory',views.listofcategory,name='listofcategory'),
    path('retrieveprogram/<int:pid>',views.retrieveprogram, name='retrieveprogram'),
    path('retrivecategory/<int:catid>',views.retrivecategory, name='retrivecategory'),
    path('createorder/<int:userid>',views.createorder,name='createorder'),
    path('takeprogram',views.takeprogram,name='takeprogram'),
    path('programs/<int:userid>',views.programs,name='programs'),

    ### front-end ###
    path('Categories/<int:catid>',views.Categories, name='Categories'),
    path('eachProgram/<int:pid>',views.eachProgram, name='eachProgram'),
    path('listallprograms',views.listallprograms,name='listallprograms'),
]
