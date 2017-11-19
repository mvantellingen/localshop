import pytest

from localshop.apps.accounts import forms
from tests.factories import TeamFactory, TeamMemberFactory, UserFactory


class TestAccessKeyForm:

    @pytest.mark.django_db
    def test_save(self):
        user = UserFactory()
        data = {
            'comment': 'something',
        }
        form = forms.AccessKeyForm(data=data, user=user)
        assert form.is_valid()

        form.save()
        assert user.access_keys.count() == 1

        key = user.access_keys.first()
        assert key.comment == 'something'


class TestTeamMemberAddForm:
    @pytest.mark.django_db
    def test_save(self):
        user = UserFactory()
        team = TeamFactory()

        data = {
            'user': user.pk,
            'role': 'owner',
        }
        form = forms.TeamMemberAddForm(data=data, team=team)
        assert form.is_valid()

        form.save()
        assert team.users.count() == 1

        member = team.members.first()
        assert member.user == user
        assert member.role == 'owner'

    @pytest.mark.django_db
    def test_duplicate(self):
        user = UserFactory()
        team = TeamFactory()
        TeamMemberFactory(user=user, team=team, role='owner')

        data = {
            'user': user.pk,
            'role': 'owner',
        }
        form = forms.TeamMemberAddForm(data=data, team=team)
        assert not form.is_valid()


class TestTeamMemberRemoveForm:
    @pytest.mark.django_db
    def test_save(self):
        user = UserFactory()
        team = TeamFactory()
        member = TeamMemberFactory(user=user, team=team, role='owner')

        data = {
            'member_obj': member.pk
        }
        form = forms.TeamMemberRemoveForm(data=data, team=team)
        assert form.is_valid()

        cleaned_data = form.clean()
        assert cleaned_data == {'member_obj': member}

    @pytest.mark.django_db
    def test_invalid_team(self):
        user = UserFactory()
        team = TeamFactory()
        member = TeamMemberFactory(user=user, role='owner')

        data = {
            'member_obj': member.pk
        }
        form = forms.TeamMemberRemoveForm(data=data, team=team)
        assert not form.is_valid()
