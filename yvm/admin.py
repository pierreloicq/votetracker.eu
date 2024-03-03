from django.contrib import admin, messages
from .models import Position
from django.forms import Textarea
from django.contrib.admin.views.main import ChangeList
from django.utils.safestring import mark_safe

#configure the general layout
# https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#customizing-the-adminsite-class
class MyAdminSite(admin.AdminSite):
    site_header = "VoteTracker.eu/comment my stances"
    site_title = "VoteTracker.eu/comment my stances"
    index_title = "gg"
    enable_nav_sidebar = False


class MyChangeList(ChangeList):
    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        if self.is_popup:
            title = "Select %s" % self.opts.verbose_name
        elif self.model_admin.has_change_permission(request):
            title = "Click on the text description to add your comment/explanation. Please write the comments in the language of your voters."
        else:
            title = "Select %s to view" % self.opts.verbose_name
        self.title = title


# configure the things that are shown for modification by the MEPs
class PositionAdmin(admin.ModelAdmin):
    readonly_fields = ["vote_date", "text_id", "text_part", "summary_url", "procedure_url", "short_desc", "your_stance", "mep"]
    fields =          ["vote_date", "text_id", "text_part", "summary_url", "procedure_url", "short_desc", "your_stance", "mep", "comment"] # you need to put the readonly_fields here too
    list_display  =   ["short_desc", "text_id", "text_part", "your_stance", "your_comment"] # displayed on the admin change list page

    # Remove the message shown on the change list after a comment is saved
    def message_user(self, request, message, level=messages.SUCCESS, extra_tags='', fail_silently=False):
        message = ""
        super().message_user(request, message, level, extra_tags, fail_silently)

    # Set the custom ChangeList class
    def get_changelist(self, request, **kwargs):
        return MyChangeList

    # fetch short_desc in the Vote model    
    def short_desc(self, obj):
        return mark_safe(obj.vote.short_desc)
    
    def vote_date(self, obj):
        return obj.vote.vote_date
    
    def text_id(self, obj):
        return obj.vote.text_id
    
    def summary_url(self, obj):
        return obj.vote.summary_url
    
    def procedure_url(self, obj):
        return obj.vote.procedure_url
    
    def text_part(self, obj):
        title = obj.vote.title
        if ' Am ' in title:
            idx = title.find(' Am ')
            return title[idx:idx+8].rstrip()
        else:
            return "full text"
        

    # Filter positions based on the currently logged-in Mep
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_authenticated and request.user.mep:
            return queryset.filter(mep=request.user.mep)
        else:
            # If not logged in as a Mep, show all positions
            return queryset

    # get a textarea for the comment instead of a small one line box
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'comment':
            kwargs['widget'] = Textarea(attrs={'rows': 5, 'cols': 40})
        return super().formfield_for_dbfield(db_field, **kwargs)

    # display nice stance
    def your_stance(self, obj):
        stance_mapping = {
            'for': 'For',
            'ag': 'Against',
            'abs': 'Abstention',
            'NA': 'No vote'
        }
        original_stance = obj.stance
        your_stance = stance_mapping.get(original_stance, original_stance)
        return your_stance
    
    def your_comment(self, obj):
        your_comment = obj.comment
        return your_comment


# if you don't subclass AdminSite
# admin.site.register(Position, PositionAdmin)

admin_site = MyAdminSite(name="myadmin")
admin_site.register(Position, PositionAdmin)