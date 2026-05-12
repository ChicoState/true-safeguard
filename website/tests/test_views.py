from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def setUp(self):
        # Create a test user for login verification
        self.username = "testuser"
        self.password = "ComplexPass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login')
        self.register_url = reverse('register')

    def test_registration_creates_user(self):
        """Verify that submitting the register form creates a new user in the DB."""
        new_username = "newly_registered"
        response = self.client.post(self.register_url, {
            'username': new_username,
            'password1': 'secret_password',
            'password2': 'secret_password'
        })
        # Check if user exists in the database
        self.assertTrue(User.objects.filter(username=new_username).exists())
        # Check if it redirects (usually to login page)
        self.assertEqual(response.status_code, 302)

    def test_login_successful(self):
        """Verify that a user can login and is redirected."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        }, follow=True)
        
        # Check if the user is now authenticated in the session
        self.assertTrue(response.context['user'].is_authenticated)
        # Verify the success page (replace 'home' with your post-login URL name)
        self.assertRedirects(response, reverse('home'))

    def test_login_failure_invalid_credentials(self):
        """Ensure invalid login attempts do not log the user in."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'wrongpassword'
        })
        # User should still be unauthenticated
        self.assertFalse(response.context['user'].is_authenticated)
        # Should stay on the same page (200 OK) rather than redirecting (302)
        self.assertEqual(response.status_code, 200)

    def test_registration_password_mismatch(self):
        """Verify that unequal passwords prevent account creation."""
        response = self.client.post(self.register_url, {
            'username': 'mismatch_user',
            'password1': 'pass1',
            'password2': 'pass2'
        })
        self.assertFalse(User.objects.filter(username='mismatch_user').exists())

class ResourceContentTests(TestCase):
    def test_offline_activities_rendering(self):
        """Verify that the offline activities loop is working."""
        # Create a mock list for the context
        test_activities = [{'title': 'Test Chess', 'desc': 'Test Desc'}]
        response = self.client.get(reverse('resources'), {'offline_activities': test_activities})
        
        self.assertEqual(response.status_code, 200)
        # Check if our specific wide-box text exists
        self.assertContains(response, "Beyond the Screen")
        self.assertContains(response, "Chico Library")

    def test_external_links_present(self):
        """Verify key community links are in the HTML."""
        response = self.client.get(reverse('resources'))
        self.assertContains(response, "https://www.chicorec.gov")
        self.assertContains(response, "https://www.buttecounty.net/148/Library")


class BlacklistPageTests(TestCase):
    def test_blacklist_page_loads(self):
        "Verify page loads successfully."
        response = self.client.get(reverse('blacklist'))
        self.assertEqual(response.status_code, 200)

    def test_blacklist_template_used(self):
        "Verify that the correct template is used for the blacklist page."
        response = self.client.get(reverse('blacklist'))
        self.assertTemplateUsed(response, 'website/blacklist.html')

    def test_blacklist_css_loaded(self):
        "Verify that blacklist CSS file is referenced in the page."
        response = self.client.get(reverse('blacklist'))
        self.assertContains(response, 'blacklist.css', html=False)


