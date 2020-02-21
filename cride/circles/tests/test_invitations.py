"""Invitations tests."""

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

# Model
from cride.circles.models import Invitation, Circle, Membership
from cride.users.models import User, Profile


class InvitationsManagerTestCase(TestCase):
    """Invitation manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Hernan',
            last_name='Chilabert',
            email='hchilabert+test@gmail.com',
            username='herchilatest',
            password='mandioca'
        )
        self.circle = Circle.objects.create(
            name='Facultad de Ciencias',
            slug_name='fciencies',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )

    def test_code_generation(self):
        """Random codes should be generated automatically."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """If a code is given, there's no need to create a new one."""
        code = 'holamundo'
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """If given code is not unique, a new one must be generated."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle
        ).code

        # Create another invitations with the past code
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code
        )

        self.assertNotEqual(code, invitation.code)


class MemberInvitationAPITestCase(APITestCase):
    """Member invitation API test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Hernan',
            last_name='Chilabert',
            email='hchilabert+test@gmail.com',
            username='herchilatest',
            password='mandioca'
        )
        self.profile = Profile.objects.create(user=self.user)
        self.circle = Circle.objects.create(
            name='Facultad de Ciencias',
            slug_name='fciencies',
            about='Grupo oficial de la Facultad de Ciencias de la UNAM',
            verified=True
        )
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.profile,
            circle=self.circle,
            remaining_invitations=10
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

        # URL
        self.url = '/circles/{}/members/{}/invitations/'.format(
            self.circle.slug_name,
            self.user.username
        )

    def test_response_success(self):
        """Verify response succeed."""
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitations are generated if none exist previously."""
        # Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(), 0)

        # Call member invitations URL
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        # Verify new invitations were created
        invitations = Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(invitations.count(), self.membership.remaining_invitations)
        for invitation in invitations:
            self.assertIn(invitation.code, request.data['invitations'])
