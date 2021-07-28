from django.urls import path
from .views import (Register, Login, View_Profile, User_Profile, View_Group,
                    Join_Group, Select_Group_Content, Select_Note, Select_Video, Select_Site,
                    List_All_Groups, List_Subject_Groups,Add_Description, List_All_Group_Members, Write_Comment, Create_Group)

app_name = "Profile"

urlpatterns = [
    path('register/', Register, name="Register"),
    path('login/', Login, name="Login"),
    path('group/', List_All_Groups, name="List All Groups"),
    path('group/subject/<subject_slug>/', List_Subject_Groups, name="List Subject Groups"),
    path('profile/', User_Profile, name="Profile"),
    path('profile/view/<profile_slug>/', View_Profile, name="View Profile"),
    path('profile/add/description/', Add_Description, name="Add Description"),
    path('group/create/', Create_Group, name="Create Group"),
    path('group/<group_id>', View_Group, name="View Group"),
    path('group/members/<group_id>', List_All_Group_Members, name="List All Group Members"),
    path('group/comment/<group_id>', Write_Comment, name="Write Comment"),
    path('group/join/<group_id>', Join_Group, name="Join Group"),
    path('group/select/<content_slug>/<group_id>/', Select_Group_Content, name="Select Content"),
    path('group/select/note/<group_id>/<note_id>', Select_Note, name="Select Note"),
    path('group/select/video/<group_id>/<video_id>', Select_Video, name="Select Video"),
    path('group/select/site/<group_id>/<site_id>', Select_Site, name="Select Site"),
    ]
