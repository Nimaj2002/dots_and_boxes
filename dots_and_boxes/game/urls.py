# game/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import GameStateView, MakeMoveView

urlpatterns = [
    path('', views.game_entry, name='game_entry'),
    path('create/', views.create_game, name='create_game'),
    path('game/<int:game_id>/', views.game_view, name='game_view'),
    path('games/', views.game_list, name='game_list'),
    path('game/<int:game_id>/restart/', views.restart_game, name='restart_game'),
    path('api/game/<int:game_id>/state/', GameStateView.as_view(), name='game_state'),
    path('api/game/<int:game_id>/move/', MakeMoveView.as_view(), name='make_move'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)