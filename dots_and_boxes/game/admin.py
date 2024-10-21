from django.contrib import admin
from .models import Game
import json

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'mode', 'player1', 'player2', 'current_player', 'winner')
    list_filter = ('mode', 'winner')
    search_fields = ('player1', 'player2')
    
    fieldsets = (
        (None, {
            'fields': ('mode', 'player1', 'player2')
        }),
        ('Game State', {
            'fields': ('current_player', 'winner'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new game
            obj.current_player = obj.player1
            obj.board = json.dumps([
                ["D", "E", "D", "E", "D", "E", "D", "E", "D"],
                ["E", " ", "E", " ", "E", " ", "E", " ", "E"],
                ["D", "E", "D", "E", "D", "E", "D", "E", "D"],
                ["E", " ", "E", " ", "E", " ", "E", " ", "E"],
                ["D", "E", "D", "E", "D", "E", "D", "E", "D"],
                ["E", " ", "E", " ", "E", " ", "E", " ", "E"],
                ["D", "E", "D", "E", "D", "E", "D", "E", "D"],
                ["E", " ", "E", " ", "E", " ", "E", " ", "E"],
                ["D", "E", "D", "E", "D", "E", "D", "E", "D"],
            ])
        super().save_model(request, obj, form, change)

admin.site.register(Game, GameAdmin)