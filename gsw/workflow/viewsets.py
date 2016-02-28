from viewsets import ModelViewSet
from workflow.views import * 
class GSWModelViewSet(ModelViewSet):
    PLACEHOLDER_PATTERN = r'(?P<pk>[0-9]+)/'
    LANGUAGE_PATTERN = r'(?P<language>[a-z-]+)/'
    views = {
        'list_view': {
            'view': GSWListView,
            'pattern': r'',
            'name': 'list',
        },
        'new_view': {
            'view': GSWNewView,
            'pattern': r'new/',
            'name': 'new',
        },
        'detail_view': {
            'view': GSWDetailView,
            'pattern': PLACEHOLDER_PATTERN,
            'name': 'details',
        },
        'edit_view': {
            'view': GSWEditView,
            'pattern': PLACEHOLDER_PATTERN + r'edit/'+ LANGUAGE_PATTERN,
            'name': 'edit',
        },
        'review_view': {
            'view': GSWReviewView,
            'pattern': PLACEHOLDER_PATTERN + r'review/',
            'name': 'review',
        },
        'publish_view': {
            'view': GSWPublishView,
            'pattern': PLACEHOLDER_PATTERN + r'publish/',
            'name': 'publish',
        },
        'reviewed_view': {
            'view': GSWReviewedView,
            'pattern': r'reviewed/',
            'name': 'reviewed',
        },
        'published_view': {
            'view': GSWPublishedView,
            'pattern': r'published/',
            'name': 'published',
        },
        'not_reviewed_view': {
            'view': GSWNotReviewedView,
            'pattern': r'not_reviewed/',
            'name': 'not-reviewed',
        },
    }
