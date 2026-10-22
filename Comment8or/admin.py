from django.contrib.admin import AdminSite
class Comment8orAdminSite(AdminSite):
    site_title = 'c8admin'
    site_header = 'c8admin'
    index_title = 'c8admin'
    logout_template= 'comment8or/logged_out.html'
comment8or_admin_site = Comment8orAdminSite(name="comment8or_admin")
