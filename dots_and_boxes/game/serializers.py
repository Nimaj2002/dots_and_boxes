from rest_framework import serializers
from .models import Game
import json

class GameStateSerializer(serializers.ModelSerializer):
    board = serializers.SerializerMethodField()
    player1_name = serializers.CharField(source='player1')
    player2_name = serializers.CharField(source='player2')

    class Meta:
        model = Game
        fields = ['board', 'player1_score', 'player2_score', 'current_player', 
                  'player1_moves', 'player2_moves', 'player1_name', 'player2_name']

    def get_board(self, obj):
        return json.loads(obj.board)

class MoveSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    row = serializers.IntegerField(min_value=0, max_value=8)
    col = serializers.IntegerField(min_value=0, max_value=8)
    