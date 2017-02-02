from django.contrib.auth.models import User  # #BTlt9#
from home.models import HomePage

# create an admin user
User.objects.create_superuser('admin', 'admin@example.com', 'pass')

# A default home page was created by the 0002_create_homepage migration
home_page = HomePage.objects.get(slug='home')

# let's create another page to link to
other_page = home_page.add_child(instance=HomePage(title="Test page", slug="test", medium=u'<p>Just a page to link to</p>'))
other_page.save()

# set the medium-enabled rich text field to some data, with a link to other_page
home_page.medium = u"""<p>A list :</p>
<span><ul><li>A<br/></li><li>B</li></ul></span>
<p>and a\xa0<a fragment="fragment" id="%s" linktype="page">link to a page</a>.</p>
<p>Some text with formatting : <b>bold</b>, <i>italic</i>, <u>underline</u>. Mixed <b><i><u>formatting</u></i></b> here.</p>
<p><span><code>This would be some code</code></span></p>
""" % other_page.id
home_page.save()
