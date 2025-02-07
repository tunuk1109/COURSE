from django.contrib import admin
from .models import *
import nested_admin
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


@admin.register(Teacher, Category)
class AllAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class OptionInline(nested_admin.NestedStackedInline, TranslationInlineModelAdmin):
    model = Option
    extra = 1

class QuestionsInline(nested_admin.NestedStackedInline, TranslationInlineModelAdmin):
    model = Questions
    extra = 1
    inlines = [OptionInline]


@admin.register(Exam)
class ExamAdmin(TranslationAdmin, nested_admin.NestedModelAdmin):
    inlines = [QuestionsInline]


    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class NetworkInline(admin.StackedInline):
    model = Network
    extra = 1

class UserNetworkAdmin(admin.ModelAdmin):
    inlines = [NetworkInline]


class LessonInline(admin.StackedInline, TranslationInlineModelAdmin):
    model = Lesson
    extra = 1

class AssignmentInline(admin.StackedInline, TranslationInlineModelAdmin):
    model = Assignment
    extra = 1


@admin.register(Course)
class CourseAllAdmin(TranslationAdmin):
    inlines = [LessonInline, AssignmentInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }



admin.site.register(UserProfile, UserNetworkAdmin)
admin.site.register(Student)
admin.site.register(Certificate)
admin.site.register(CourseReview)
admin.site.register(TeacherRating)
admin.site.register(History)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)






