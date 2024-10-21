import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.files.storage import default_storage
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .serializers import GameStateSerializer, MoveSerializer
from .models import Game
import logging
import subprocess
import threading
import sys

logger = logging.getLogger(__name__)

def game_view(request, game_id):
    game = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        row = int(request.POST.get('row'))
        col = int(request.POST.get('col'))
        if game.make_move(row, col):
            game.print_game_state()
            print("Move added")
            return JsonResponse({
                'success': True,
                'board': game.get_board(),
                'current_player': game.current_player,
                'winner': game.winner,
                'player1_moves': game.get_player1_moves(),
                'player2_moves': game.get_player2_moves(),
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid move'})
    
    # GET request
    context = {
        'game': game,
        'board': game.get_board(),
        'player1_moves': game.get_player1_moves(),
        'player2_moves': game.get_player2_moves(),
    }
    return render(request, 'game/game_board.html', context)

def game_list(request):
    games = Game.objects.all()
    return render(request, 'game/game_list.html', {'games': games})

@require_POST
def restart_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.initialize_board()
    game.clear_moves()
    game.current_player = game.player1
    game.winner = None
    game.save()

    return JsonResponse({
        'success': True,
        'board': game.get_board(),
        'current_player': game.current_player,
        'player1_moves': game.get_player1_moves(),
        'player2_moves': game.get_player2_moves(),
    }) 

def game_entry(request):
    return render(request, 'game/game_entry.html')

def create_game(request):
    if request.method == 'POST':
        game_mode = request.POST.get('game_mode')
        player1 = request.POST.get('player1', 'Agent 1')
        player2 = request.POST.get('player2', 'Agent 2')
        use_implemented_agent = request.POST.get('use_implemented_agent') == 'on'
        
        game = Game.objects.create(
            mode=game_mode,
            player1=player1,
            player2=player2,
            player1_is_agent=game_mode == 'AVA',
            player2_is_agent=game_mode in ['PVA', 'AVA']
        )
        
        server_url = request.build_absolute_uri('/').rstrip('/')
        port = request.META.get('SERVER_PORT', '8000')

        if game_mode == 'PVA' and not use_implemented_agent:
            agent_file = request.FILES.get('pva_agent_file')
            if agent_file:
                file_name = f"agent_{game.id}_2{os.path.splitext(agent_file.name)[1]}"
                file_path = os.path.join(settings.MEDIA_ROOT, 'agent_files', file_name)
                default_storage.save(file_path, agent_file)
                game.agent2_file = file_path
                game.save()
                
                # Start the agent in a separate thread
                threading.Thread(target=run_agent, args=(file_path, game.id, player2, server_url, port)).start()
        elif game_mode == 'AVA':
            agent1_file = request.FILES.get('agent1_file')
            agent2_file = request.FILES.get('agent2_file')
            if agent1_file:
                file_name = f"agent_{game.id}_1{os.path.splitext(agent1_file.name)[1]}"
                file_path = os.path.join(settings.MEDIA_ROOT, 'agent_files', file_name)
                default_storage.save(file_path, agent1_file)
                game.agent1_file = file_path
                
                # Start agent 1 in a separate thread
                threading.Thread(target=run_agent, args=(file_path, game.id, player1, server_url, port)).start()
            if agent2_file:
                file_name = f"agent_{game.id}_2{os.path.splitext(agent2_file.name)[1]}"
                file_path = os.path.join(settings.MEDIA_ROOT, 'agent_files', file_name)
                default_storage.save(file_path, agent2_file)
                game.agent2_file = file_path
                
                # Start agent 2 in a separate thread
                threading.Thread(target=run_agent, args=(file_path, game.id, player2, server_url, port)).start()
            game.save()
        
        return redirect('game_view', game_id=game.id)
    
    return redirect('game_entry')

def run_agent(file_path, game_id, player_name, server_url, port):
    subprocess.Popen([sys.executable, 'agent_wrapper.py', file_path, str(game_id), player_name, server_url, port])

class GameStateView(APIView):
    def get(self, request, game_id):
        try:
            game = Game.objects.get(pk=game_id)
            serializer = GameStateSerializer(game)
            return Response(serializer.data)
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

class MakeMoveView(APIView):
    def post(self, request, game_id):
        try:
            game = Game.objects.get(pk=game_id)
            player_name = request.data.get('name')
            
            if player_name not in [game.player1, game.player2]:
                return Response({"error": "Invalid player"}, status=status.HTTP_401_UNAUTHORIZED)
            
            if game.current_player != player_name:
                return Response({"error": "It's not your turn"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = MoveSerializer(data=request.data)
            if serializer.is_valid():
                row = serializer.validated_data['row']
                col = serializer.validated_data['col']
                if game.make_move(row, col):
                    return Response(GameStateSerializer(game).data)
                else:
                    return Response({"error": "Invalid move"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)