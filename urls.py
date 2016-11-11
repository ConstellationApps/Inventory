from django.conf.urls import url

from . import views

urlpatterns = [
# =============================================================================
# View Routes
# =============================================================================

    url(r'^view/list$', views.view_list),

# =============================================================================
# Management Routes
# =============================================================================

    url(r'^manage/create-board$', views.manage_create_board),

# =============================================================================
# API Routes for the v1 API
# =============================================================================

    # The API routes are divided into functional groups based on what
    # they control.  In general each group will contain the standard
    # CRUD calls, but may also contain additional calls for specific
    # objects.

# -----------------------------------------------------------------------------
# API Routes related to Board Operations
# -----------------------------------------------------------------------------

    url(r'^api/v1/board/list$', views.api_v1_board_list),
    url(r'^api/v1/board/create$', views.api_v1_board_create),
    url(r'^api/v1/board/([\d]*)/deactivate$', views.api_v1_board_deactivate),
    url(r'^api/v1/board/([\d]*)/activate$', views.api_v1_board_activate),
    url(r'^api/v1/board/([\d]*)/active-cards$',
        views.api_v1_board_active_cards),
    url(r'^api/v1/board/([\d]*)/archived-cards$',
        views.api_v1_board_archived_cards),

# -----------------------------------------------------------------------------
# API Routes related to Card Operations
# -----------------------------------------------------------------------------

    url(r'^api/v1/card/create$', views.api_v1_card_create),
    url(r'^api/v1/card/([\d]*)/archive$', views.api_v1_card_archive),
    url(r'^api/v1/card/([\d]*)/unarchive$', views.api_v1_card_unarchive),

# -----------------------------------------------------------------------------
# API Routes related to Stage Operations
# -----------------------------------------------------------------------------

    url(r'^api/v1/stage/create$', views.api_v1_stage_create),
    url(r'^api/v1/stage/([\d]*)/archive$', views.api_v1_stage_archive),
    url(r'^api/v1/stage/([\d]*)/unarchive$', views.api_v1_stage_unarchive),

]
