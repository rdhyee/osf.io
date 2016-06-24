from nose.tools import *  # flake8: noqa
from datetime import datetime

from framework.guid.model import Guid

from api.base.settings.defaults import API_BASE
from api_tests import utils as test_utils
from tests.base import ApiTestCase
from tests.factories import ProjectFactory, AuthUserFactory, CommentFactory, NodeWikiFactory


class CommentReportsMixin(object):

    def setUp(self):
        super(CommentReportsMixin, self).setUp()
        self.user = AuthUserFactory()
        self.contributor = AuthUserFactory()
        self.non_contributor = AuthUserFactory()
        self.payload = {
            'data': {
                'type': 'comment_reports',
                'attributes': {
                    'category': 'spam',
                    'message': 'delicious spam'
                }
            }
        }

    def _set_up_private_project_comment_reports(self):
        raise NotImplementedError

    def _set_up_public_project_comment_reports(self, comment_level='public'):
        raise NotImplementedError

    def test_private_node_logged_out_user_cannot_view_reports(self):
        self._set_up_private_project_comment_reports()
        res = self.app.get(self.private_url, expect_errors=True)
        assert_equal(res.status_code, 401)

    def test_private_node_logged_in_non_contributor_cannot_view_reports(self):
        self._set_up_private_project_comment_reports()
        res = self.app.get(self.private_url, auth=self.non_contributor.auth, expect_errors=True)
        assert_equal(res.status_code, 403)

    def test_private_node_only_reporting_user_can_view_reports(self):
        self._set_up_private_project_comment_reports()
        res = self.app.get(self.private_url, auth=self.user.auth)
        assert_equal(res.status_code, 200)
        report_json = res.json['data']
        report_ids = [report['id'] for report in report_json]
        assert_equal(len(report_json), 1)
        assert_in(self.user._id, report_ids)

    def test_private_node_reported_user_does_not_see_report(self):
        self._set_up_private_project_comment_reports()
        res = self.app.get(self.private_url, auth=self.contributor.auth)
        assert_equal(res.status_code, 200)
        report_json = res.json['data']
        report_ids = [report['id'] for report in report_json]
        assert_equal(len(report_json), 0)
        assert_not_in(self.contributor._id, report_ids)

    def test_public_node_only_reporting_contributor_can_view_report(self):
        self._set_up_public_project_comment_reports()
        res = self.app.get(self.public_url, auth=self.user.auth)
        assert_equal(res.status_code, 200)
        report_json = res.json['data']
        report_ids = [report['id'] for report in report_json]
        assert_equal(len(report_json), 1)
        assert_in(self.user._id, report_ids)

    def test_public_node_reported_user_does_not_see_report(self):
        self._set_up_public_project_comment_reports()
        res = self.app.get(self.public_url, auth=self.contributor.auth)
        assert_equal(res.status_code, 200)
        report_json = res.json['data']
        report_ids = [report['id'] for report in report_json]
        assert_equal(len(report_json), 0)
        assert_not_in(self.contributor._id, report_ids)

    def test_public_node_non_contributor_does_not_see_other_user_reports(self):
        self._set_up_public_project_comment_reports()
        res = self.app.get(self.public_url, auth=self.non_contributor.auth, expect_errors=True)
        assert_equal(res.status_code, 200)
        report_json = res.json['data']
        report_ids = [report['id'] for report in report_json]
        assert_equal(len(report_json), 0)
        assert_not_in(self.non_contributor._id, report_ids)

    def test_public_node_non_contributor_reporter_can_view_own_report(self):
        self._set_up_public_project_comment_reports()
        self.public_comment.reports[self.non_contributor._id] = {
            'category': 'spam',
            'text': 'This is spam',
            'date': datetime.utcnow(),
            'retracted': False,
        }
        self.public_comment.save()
        res = self.app.get(self.public_url, auth=self.non_contributor.auth)
        assert_equal(res.status_code, 200)
        report_json = res.json['data']
        report_ids = [report['id'] for report in report_json]
        assert_equal(len(report_json), 1)
        assert_in(self.non_contributor._id, report_ids)

    def test_public_node_logged_out_user_cannot_view_reports(self):
        self._set_up_public_project_comment_reports()
        res = self.app.get(self.public_url, expect_errors=True)
        assert_equal(res.status_code, 401)

    def test_public_node_private_comment_level_non_contributor_cannot_see_reports(self):
        self._set_up_public_project_comment_reports(comment_level='private')
        res = self.app.get(self.public_url, auth=self.non_contributor.auth, expect_errors=True)
        assert_equal(res.status_code, 403)
        assert_equal(res.json['errors'][0]['detail'], 'You do not have permission to perform this action.')

    def test_report_comment_invalid_type(self):
        self._set_up_private_project_comment_reports()
        payload = {
            'data': {
                'type': 'Not a valid type.',
                'attributes': {
                    'category': 'spam',
                    'message': 'delicious spam'
                }
            }
        }
        res = self.app.post_json_api(self.private_url, payload, auth=self.user.auth, expect_errors=True)
        assert_equal(res.status_code, 409)

    def test_report_comment_no_type(self):
        self._set_up_private_project_comment_reports()
        payload = {
            'data': {
                'type': '',
                'attributes': {
                    'category': 'spam',
                    'message': 'delicious spam'
                }
            }
        }
        res = self.app.post_json_api(self.private_url, payload, auth=self.user.auth, expect_errors=True)
        assert_equal(res.status_code, 400)
        assert_equal(res.json['errors'][0]['detail'], 'This field may not be blank.')
        assert_equal(res.json['errors'][0]['source']['pointer'], '/data/type')

    def test_report_comment_invalid_spam_category(self):
        self._set_up_private_project_comment_reports()
        category = 'Not a valid category'
        payload = {
            'data': {
                'type': 'comment_reports',
                'attributes': {
                    'category': category,
                    'message': 'delicious spam'
                }
            }
        }
        res = self.app.post_json_api(self.private_url, payload, auth=self.user.auth, expect_errors=True)
        assert_equal(res.status_code, 400)
        assert_equal(res.json['errors'][0]['detail'], '\"' + category + '\"' + ' is not a valid choice.')

    def test_report_comment_allow_blank_message(self):
        self._set_up_private_project_comment_reports()
        comment = CommentFactory(node=self.private_project, user=self.contributor, target=self.comment.target)
        url = '/{}comments/{}/reports/'.format(API_BASE, comment._id)
        payload = {
            'data': {
                'type': 'comment_reports',
                'attributes': {
                    'category': 'spam',
                    'message': ''
                }
            }
        }
        res = self.app.post_json_api(url, payload, auth=self.user.auth)
        assert_equal(res.status_code, 201)
        assert_equal(res.json['data']['id'], self.user._id)
        assert_equal(res.json['data']['attributes']['message'], payload['data']['attributes']['message'])

    def test_private_node_logged_out_user_cannot_report_comment(self):
        self._set_up_private_project_comment_reports()
        res = self.app.post_json_api(self.private_url, self.payload, expect_errors=True)
        assert_equal(res.status_code, 401)

    def test_private_node_logged_in_non_contributor_cannot_report_comment(self):
        self._set_up_private_project_comment_reports()
        res = self.app.post_json_api(self.private_url, self.payload, auth=self.non_contributor.auth, expect_errors=True)
        assert_equal(res.status_code, 403)

    def test_private_node_logged_in_contributor_can_report_comment(self):
        self._set_up_private_project_comment_reports()
        comment = CommentFactory(node=self.private_project, user=self.contributor, target=self.comment.target)
        url = '/{}comments/{}/reports/'.format(API_BASE, comment._id)
        res = self.app.post_json_api(url, self.payload, auth=self.user.auth)
        assert_equal(res.status_code, 201)
        assert_equal(res.json['data']['id'], self.user._id)

    def test_user_cannot_report_own_comment(self):
        self._set_up_private_project_comment_reports()
        res = self.app.post_json_api(self.private_url, self.payload, auth=self.contributor.auth, expect_errors=True)
        assert_equal(res.status_code, 400)
        assert_equal(res.json['errors'][0]['detail'], 'You cannot report your own comment.')

    def test_user_cannot_report_comment_twice(self):
        self._set_up_private_project_comment_reports()
        # User cannot report the comment again
        res = self.app.post_json_api(self.private_url, self.payload, auth=self.user.auth, expect_errors=True)
        assert_equal(res.status_code, 400)
        assert_equal(res.json['errors'][0]['detail'], 'Comment already reported.')

    def test_public_node_logged_out_user_cannot_report_comment(self):
        self._set_up_public_project_comment_reports()
        res = self.app.post_json_api(self.public_url, self.payload, expect_errors=True)
        assert_equal(res.status_code, 401)

    def test_public_node_contributor_can_report_comment(self):
        self._set_up_public_project_comment_reports()
        comment = CommentFactory(node=self.public_project, user=self.contributor, target=self.public_comment.target)
        url = '/{}comments/{}/reports/'.format(API_BASE, comment._id)

        res = self.app.post_json_api(url, self.payload, auth=self.user.auth)
        assert_equal(res.status_code, 201)
        assert_equal(res.json['data']['id'], self.user._id)

    def test_public_node_non_contributor_can_report_comment(self):
        """ Test that when a public project allows any osf user to
            comment (comment_level == 'public), non-contributors
            can also report comments.
        """
        self._set_up_public_project_comment_reports()
        res = self.app.post_json_api(self.public_url, self.payload, auth=self.non_contributor.auth)
        assert_equal(res.status_code, 201)
        assert_equal(res.json['data']['id'], self.non_contributor._id)

    def test_public_node_private_comment_level_non_contributor_cannot_report_comment(self):
        self._set_up_public_project_comment_reports(comment_level='private')
        res = self.app.get(self.public_url, auth=self.non_contributor.auth, expect_errors=True)
        assert_equal(res.status_code, 403)
        assert_equal(res.json['errors'][0]['detail'], 'You do not have permission to perform this action.')


class TestCommentReportsView(CommentReportsMixin, ApiTestCase):

    def _set_up_private_project_comment_reports(self):
        self.private_project = ProjectFactory.create(is_public=False, creator=self.user)
        self.private_project.add_contributor(contributor=self.contributor, save=True)
        self.comment = CommentFactory.build(node=self.private_project, user=self.contributor)
        self.comment.reports = self.comment.reports or {}
        self.comment.reports[self.user._id] = {
            'category': 'spam',
            'text': 'This is spam',
            'date': datetime.utcnow(),
            'retracted': False,
        }
        self.comment.save()
        self.private_url = '/{}comments/{}/reports/'.format(API_BASE, self.comment._id)

    def _set_up_public_project_comment_reports(self, comment_level='public'):
        self.public_project = ProjectFactory.create(is_public=True, creator=self.user, comment_level=comment_level)
        self.public_project.add_contributor(contributor=self.contributor, save=True)
        self.public_comment = CommentFactory.build(node=self.public_project, user=self.contributor)
        self.public_comment.reports = self.public_comment.reports or {}
        self.public_comment.reports[self.user._id] = {
            'category': 'spam',
            'text': 'This is spam',
            'date': datetime.utcnow(),
            'retracted': False,
        }
        self.public_comment.save()
        self.public_url = '/{}comments/{}/reports/'.format(API_BASE, self.public_comment._id)


class TestFileCommentReportsView(CommentReportsMixin, ApiTestCase):

    def _set_up_private_project_comment_reports(self):
        self.private_project = ProjectFactory.create(is_public=False, creator=self.user)
        self.private_project.add_contributor(contributor=self.contributor, save=True)
        self.file = test_utils.create_test_file(self.private_project, self.user)
        self.comment = CommentFactory.build(node=self.private_project, target=self.file.get_guid(), user=self.contributor)
        self.comment.reports = self.comment.reports or {}
        self.comment.reports[self.user._id] = {
            'category': 'spam',
            'text': 'This is spam',
            'date': datetime.utcnow(),
            'retracted': False,
        }
        self.comment.save()
        self.private_url = '/{}comments/{}/reports/'.format(API_BASE, self.comment._id)

    def _set_up_public_project_comment_reports(self, comment_level='public'):
        self.public_project = ProjectFactory.create(is_public=True, creator=self.user, comment_level=comment_level)
        self.public_project.add_contributor(contributor=self.contributor, save=True)
        self.public_file = test_utils.create_test_file(self.public_project, self.user)
        self.public_comment = CommentFactory.build(node=self.public_project, target=self.public_file.get_guid(), user=self.contributor)
        self.public_comment.reports = self.public_comment.reports or {}
        self.public_comment.reports[self.user._id] = {
            'category': 'spam',
            'text': 'This is spam',
            'date': datetime.utcnow(),
            'retracted': False,
        }
        self.public_comment.save()
        self.public_url = '/{}comments/{}/reports/'.format(API_BASE, self.public_comment._id)


class TestWikiCommentReportsView(CommentReportsMixin, ApiTestCase):

    def _set_up_private_project_comment_reports(self):
        self.private_project = ProjectFactory.create(is_public=False, creator=self.user)
        self.private_project.add_contributor(contributor=self.contributor, save=True)
        self.wiki = NodeWikiFactory(node=self.private_project, user=self.user)
        self.comment = CommentFactory.build(node=self.private_project, target=Guid.load(self.wiki._id), user=self.contributor)
        self.comment.reports = self.comment.reports or {}
        self.comment.reports[self.user._id] = {
            'category': 'spam',
            'text': 'This is spam',
            'date': datetime.utcnow(),
            'retracted': False,
        }
        self.comment.save()
        self.private_url = '/{}comments/{}/reports/'.format(API_BASE, self.comment._id)

    def _set_up_public_project_comment_reports(self, comment_level='public'):
        self.public_project = ProjectFactory.create(is_public=True, creator=self.user, comment_level=comment_level)
        self.public_project.add_contributor(contributor=self.contributor, save=True)
        self.public_wiki = NodeWikiFactory(node=self.public_project, user=self.user)
        self.public_comment = CommentFactory.build(node=self.public_project, target=Guid.load(self.public_wiki._id), user=self.contributor)
        self.public_comment.reports = self.public_comment.reports or {}
        self.public_comment.reports[self.user._id] = {
            'category': 'spam',
            'text': 'This is spam',
            'date': datetime.utcnow(),
            'retracted': False,
        }
        self.public_comment.save()
        self.public_url = '/{}comments/{}/reports/'.format(API_BASE, self.public_comment._id)
