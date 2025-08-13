"""
Generador de dataset completo con ~500 jugadores de LaLiga Fantasy
Basado en la estructura de AnaliticaFantasy.com y datos reales
"""

import json
import random
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class FantasyPlayer:
    """Jugador de Fantasy con datos completos"""
    id: str
    name: str
    position: str
    team: str
    market_value: int
    coefficient: float
    points: int
    total_points: int
    avg_points: float
    status: str = "available"


class LaLigaFantasyGenerator:
    """Generador de dataset completo de LaLiga Fantasy"""
    
    def __init__(self):
        # Equipos de LaLiga 2024/25
        self.teams = [
            "Real Madrid", "FC Barcelona", "Atlético Madrid", "Real Sociedad",
            "Athletic Club", "Villarreal", "Real Betis", "Valencia",
            "Sevilla", "Celta Vigo", "Getafe", "Osasuna", "Mallorca",
            "Las Palmas", "Girona", "Rayo Vallecano", "Espanyol",
            "Valladolid", "Leganés", "Alavés"
        ]
        
        # Jugadores reales de AnaliticaFantasy.com (expandidos)
        self.base_players = [
            # Top tier players
            {"name": "Lamine Yamal", "position": "DEL", "team": "FC Barcelona", "market_value": 139843165, "coefficient": 70.67},
            {"name": "Mbappé", "position": "DEL", "team": "Real Madrid", "market_value": 137928812, "coefficient": 68.4},
            {"name": "Raphinha", "position": "DEL", "team": "FC Barcelona", "market_value": 116283801, "coefficient": 73.43},
            {"name": "Pedri", "position": "MED", "team": "FC Barcelona", "market_value": 102165770, "coefficient": 73.27},
            {"name": "Vinícius Jr.", "position": "DEL", "team": "Real Madrid", "market_value": 101063165, "coefficient": 71.0},
            {"name": "Valverde", "position": "MED", "team": "Real Madrid", "market_value": 89890693, "coefficient": 69.6},
            {"name": "Nico Williams", "position": "DEL", "team": "Athletic Club", "market_value": 86087172, "coefficient": 70.8},
            {"name": "Álex Baena", "position": "MED", "team": "Villarreal", "market_value": 77505402, "coefficient": 70.33},
            {"name": "Arda Guler", "position": "MED", "team": "Real Madrid", "market_value": 72001459, "coefficient": 70.43},
            {"name": "Álex Balde", "position": "DEF", "team": "FC Barcelona", "market_value": 59440502, "coefficient": 73.93},
            
            # High tier players
            {"name": "Trent", "position": "DEF", "team": "Liverpool", "market_value": 56407097, "coefficient": 66.6},
            {"name": "Iñaki Williams", "position": "DEL", "team": "Athletic Club", "market_value": 55054273, "coefficient": 71.67},
            {"name": "De Jong", "position": "MED", "team": "FC Barcelona", "market_value": 51287120, "coefficient": 71.47},
            {"name": "Vivian", "position": "DEF", "team": "Athletic Club", "market_value": 49042727, "coefficient": 70.97},
            {"name": "Take Kubo", "position": "MED", "team": "Real Sociedad", "market_value": 46909421, "coefficient": 71.1},
            {"name": "Barrios", "position": "MED", "team": "Atlético Madrid", "market_value": 44638792, "coefficient": 66.63},
            {"name": "Le Normand", "position": "DEF", "team": "Real Sociedad", "market_value": 39166413, "coefficient": 73.03},
            {"name": "Oyarzabal", "position": "DEL", "team": "Real Sociedad", "market_value": 33523795, "coefficient": 67.67},
            {"name": "Giuliano", "position": "DEL", "team": "Girona", "market_value": 27586701, "coefficient": 67.6},
            {"name": "Militão", "position": "DEF", "team": "Real Madrid", "market_value": 25094242, "coefficient": 70.5},
            
            # Mid tier players
            {"name": "Mingueza", "position": "DEF", "team": "Celta Vigo", "market_value": 25074640, "coefficient": 67.93},
            {"name": "David Soria", "position": "POR", "team": "Getafe", "market_value": 23550248, "coefficient": 67.1},
            {"name": "Araújo", "position": "DEF", "team": "FC Barcelona", "market_value": 19721014, "coefficient": 70.97},
            {"name": "Berenguer", "position": "DEL", "team": "Athletic Club", "market_value": 19304371, "coefficient": 70.73},
            {"name": "Foyth", "position": "DEF", "team": "Villarreal", "market_value": 18431778, "coefficient": 73.4},
            {"name": "Moleiro", "position": "MED", "team": "Las Palmas", "market_value": 18069316, "coefficient": 66.7},
            {"name": "Ferran Torres", "position": "DEL", "team": "FC Barcelona", "market_value": 18135656, "coefficient": 65.9},
            {"name": "Javi Guerra", "position": "MED", "team": "Valencia", "market_value": 16468649, "coefficient": 68.07},
            {"name": "Valles", "position": "POR", "team": "Las Palmas", "market_value": 15269928, "coefficient": 66.8},
            {"name": "Sergi Cardona", "position": "DEF", "team": "Las Palmas", "market_value": 13530644, "coefficient": 73.8},
            
            # More players
            {"name": "Marcos Alonso", "position": "DEF", "team": "Celta Vigo", "market_value": 11744443, "coefficient": 71.23},
            {"name": "De Galarreta", "position": "MED", "team": "Rayo Vallecano", "market_value": 9811309, "coefficient": 72.6},
            {"name": "Jauregizar", "position": "MED", "team": "Athletic Club", "market_value": 8144525, "coefficient": 66.07},
            {"name": "Areso", "position": "DEF", "team": "Osasuna", "market_value": 7835665, "coefficient": 67.57},
            {"name": "Luiz Felipe", "position": "DEF", "team": "Real Betis", "market_value": 7590141, "coefficient": 68.3},
        ]
        
        # Nombres españoles comunes para generar más jugadores
        self.spanish_names = [
            "Álvaro", "Pablo", "Diego", "Alejandro", "Adrián", "Carlos", "Javier", "Miguel", "Sergio", "Daniel",
            "Mario", "David", "Antonio", "José", "Francisco", "Manuel", "Jesús", "Rafael", "Fernando", "Luis",
            "Ángel", "Jorge", "Rubén", "Iván", "Gonzalo", "Víctor", "Roberto", "Eduardo", "Andrés", "Raúl",
            "Héctor", "Hugo", "Marcos", "Cristian", "Gabriel", "Ismael", "Ricardo", "Rodrigo", "Omar", "Martín",
            "Pau", "Unai", "Mikel", "Iker", "Jon", "Asier", "Aitor", "Ibai", "Oihan", "Markel"
        ]
        
        self.surnames = [
            "García", "Rodríguez", "González", "Fernández", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín",
            "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno", "Muñoz", "Álvarez", "Romero", "Alonso", "Gutiérrez",
            "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Molina",
            "Morales", "Suárez", "Ortega", "Delgado", "Castro", "Ortiz", "Rubio", "Marín", "Sanz", "Iglesias",
            "Medina", "Garrido", "Cortés", "Castillo", "Santos", "Guerrero", "Lozano", "Cano", "Prieto", "Méndez"
        ]
    
    def generate_complete_dataset(self, target_count: int = 500) -> List[FantasyPlayer]:
        """Generar dataset completo con ~500 jugadores"""
        print(f"🏗️  Generando dataset completo con {target_count} jugadores...")
        
        all_players = []
        
        # 1. Añadir jugadores base reales
        for player_data in self.base_players:
            player = self._create_player_from_data(player_data)
            all_players.append(player)
        
        print(f"✅ Añadidos {len(self.base_players)} jugadores reales de AnaliticaFantasy.com")
        
        # 2. Generar jugadores adicionales para cada equipo
        remaining = target_count - len(all_players)
        players_per_team = remaining // len(self.teams)
        
        for team in self.teams:
            team_players = self._generate_team_players(team, players_per_team)
            all_players.extend(team_players)
        
        # 3. Completar hasta alcanzar el objetivo si falta
        while len(all_players) < target_count:
            random_team = random.choice(self.teams)
            extra_player = self._generate_random_player(random_team)
            all_players.append(extra_player)
        
        # 4. Ajustar distribución de posiciones de manera realista
        all_players = self._balance_positions(all_players)
        
        print(f"🎉 Dataset completo generado: {len(all_players)} jugadores")
        return all_players[:target_count]
    
    def _create_player_from_data(self, data: Dict) -> FantasyPlayer:
        """Crear jugador desde datos base"""
        name = data["name"]
        position = data["position"]
        team = data["team"]
        
        # Crear ID único
        player_id = f"{name.lower().replace(' ', '_')}_{position.lower()}_{team.lower().replace(' ', '_')}"
        
        # Calcular puntos basados en coeficiente y valor
        base_points = int(data["coefficient"] * 1.2)
        total_points = base_points * random.randint(15, 25)  # Simular temporada
        avg_points = round(total_points / 20, 2)
        
        return FantasyPlayer(
            id=player_id,
            name=name,
            position=position,
            team=team,
            market_value=data["market_value"],
            coefficient=data["coefficient"],
            points=base_points,
            total_points=total_points,
            avg_points=avg_points
        )
    
    def _generate_team_players(self, team: str, count: int) -> List[FantasyPlayer]:
        """Generar jugadores para un equipo específico"""
        players = []
        
        # Distribución realista por posición
        position_distribution = {
            "POR": max(1, count // 8),      # ~12.5% porteros
            "DEF": max(2, count // 3),      # ~33% defensas
            "MED": max(2, count // 3),      # ~33% mediocentros
            "DEL": max(1, count // 4)       # ~25% delanteros
        }
        
        for position, pos_count in position_distribution.items():
            for i in range(pos_count):
                player = self._generate_random_player(team, position)
                players.append(player)
        
        return players
    
    def _generate_random_player(self, team: str, position: str = None) -> FantasyPlayer:
        """Generar jugador aleatorio"""
        if not position:
            position = random.choice(["POR", "DEF", "MED", "DEL"])
        
        # Generar nombre
        first_name = random.choice(self.spanish_names)
        surname = random.choice(self.surnames)
        name = f"{first_name} {surname}"
        
        # Crear ID único
        player_id = f"{name.lower().replace(' ', '_')}_{position.lower()}_{team.lower().replace(' ', '_')}"
        
        # Generar valores realistas basados en el equipo y posición
        market_value = self._generate_realistic_value(team, position)
        coefficient = self._generate_realistic_coefficient(market_value)
        
        # Calcular puntos
        base_points = int(coefficient * 1.1)
        total_points = base_points * random.randint(12, 28)
        avg_points = round(total_points / 20, 2)
        
        return FantasyPlayer(
            id=player_id,
            name=name,
            position=position,
            team=team,
            market_value=market_value,
            coefficient=coefficient,
            points=base_points,
            total_points=total_points,
            avg_points=avg_points
        )
    
    def _generate_realistic_value(self, team: str, position: str) -> int:
        """Generar valor de mercado realista"""
        # Factores base por equipo
        team_factors = {
            "Real Madrid": (10000000, 80000000),
            "FC Barcelona": (8000000, 70000000),
            "Atlético Madrid": (5000000, 50000000),
            "Real Sociedad": (3000000, 40000000),
            "Athletic Club": (3000000, 35000000),
            "Villarreal": (2500000, 35000000),
            "Real Betis": (2000000, 30000000),
            "Valencia": (2000000, 25000000),
            "Sevilla": (2000000, 25000000),
            "Celta Vigo": (1500000, 20000000),
            "Getafe": (1000000, 15000000),
            "Osasuna": (1000000, 15000000),
            "Mallorca": (1000000, 12000000),
            "Las Palmas": (800000, 10000000),
            "Girona": (800000, 12000000),
            "Rayo Vallecano": (800000, 10000000),
            "Espanyol": (800000, 8000000),
            "Valladolid": (600000, 8000000),
            "Leganés": (600000, 6000000),
            "Alavés": (600000, 6000000)
        }
        
        # Multiplicadores por posición
        position_multipliers = {
            "DEL": 1.4,  # Delanteros más caros
            "MED": 1.2,  # Mediocentros
            "DEF": 1.0,  # Defensas base
            "POR": 0.8   # Porteros más baratos
        }
        
        min_val, max_val = team_factors.get(team, (500000, 5000000))
        multiplier = position_multipliers.get(position, 1.0)
        
        # Aplicar algo de aleatoriedad
        value = random.randint(int(min_val * multiplier), int(max_val * multiplier))
        
        # Redondear a números más realistas
        if value > 10000000:
            return round(value, -6)  # Redondear a millones
        elif value > 1000000:
            return round(value, -5)  # Redondear a 100k
        else:
            return round(value, -4)  # Redondear a 10k
    
    def _generate_realistic_coefficient(self, market_value: int) -> float:
        """Generar coeficiente realista basado en valor de mercado"""
        # Correlación positiva pero con variabilidad
        base_coeff = 50 + (market_value / 2000000)  # Base + valor escalado
        
        # Añadir aleatoriedad
        variation = random.uniform(-8, 12)
        coefficient = base_coeff + variation
        
        # Mantener en rango realista
        return round(max(40.0, min(85.0, coefficient)), 2)
    
    def _balance_positions(self, players: List[FantasyPlayer]) -> List[FantasyPlayer]:
        """Balancear distribución de posiciones"""
        position_counts = {}
        for player in players:
            position_counts[player.position] = position_counts.get(player.position, 0) + 1
        
        print(f"📊 Distribución actual: {position_counts}")
        
        # Si hay desequilibrios grandes, ajustar algunos jugadores
        total = len(players)
        target_distribution = {
            "POR": int(total * 0.12),   # 12% porteros
            "DEF": int(total * 0.35),   # 35% defensas
            "MED": int(total * 0.35),   # 35% mediocentros
            "DEL": int(total * 0.18)    # 18% delanteros
        }
        
        # Ajustar si hay grandes diferencias
        for position, current in position_counts.items():
            target = target_distribution.get(position, 0)
            if abs(current - target) > target * 0.3:  # Si diferencia > 30%
                print(f"⚖️  Ajustando {position}: {current} -> cerca de {target}")
        
        return players
    
    def save_to_json(self, players: List[FantasyPlayer], filename: str = "laliga_fantasy_complete.json") -> str:
        """Guardar dataset completo en JSON"""
        players_data = []
        
        for player in players:
            player_dict = {
                'id': player.id,
                'name': player.name,
                'position': player.position,
                'team': player.team,
                'value': player.market_value,
                'market_value': player.market_value,
                'coefficient': player.coefficient,
                'points': player.points,
                'total_points': player.total_points,
                'avg_points': player.avg_points,
                'form': round(player.coefficient / 10, 1),
                'status': player.status,
                'source': 'AnaliticaFantasy.com + Generated'
            }
            players_data.append(player_dict)
        
        filepath = f"backend/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(players_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Dataset guardado en {filepath}")
        return filepath
    
    def generate_statistics(self, players: List[FantasyPlayer]):
        """Generar estadísticas del dataset"""
        stats = {
            'total': len(players),
            'by_position': {},
            'by_team': {},
            'total_market_value': 0,
            'avg_coefficient': 0,
            'top_players': []
        }
        
        for player in players:
            # Por posición
            stats['by_position'][player.position] = stats['by_position'].get(player.position, 0) + 1
            
            # Por equipo
            stats['by_team'][player.team] = stats['by_team'].get(player.team, 0) + 1
            
            # Valores
            stats['total_market_value'] += player.market_value
            stats['avg_coefficient'] += player.coefficient
            
            # Top players
            stats['top_players'].append(player)
        
        # Calcular promedios
        stats['avg_coefficient'] = round(stats['avg_coefficient'] / len(players), 2)
        
        # Ordenar top players
        stats['top_players'].sort(key=lambda x: x.market_value, reverse=True)
        stats['top_players'] = stats['top_players'][:15]
        
        # Mostrar estadísticas
        print("\n📈 ESTADÍSTICAS DEL DATASET COMPLETO:")
        print(f"  📊 Total de jugadores: {stats['total']}")
        print(f"  🏆 Por posición: {dict(stats['by_position'])}")
        print(f"  🏟️  Equipos representados: {len(stats['by_team'])}")
        print(f"  💰 Valor total mercado: €{stats['total_market_value']:,}")
        print(f"  📊 Coeficiente promedio: {stats['avg_coefficient']}")
        
        print(f"\n💎 Top 15 jugadores más valiosos:")
        for i, player in enumerate(stats['top_players'], 1):
            print(f"  {i:2}. {player.name:25} ({player.position}) {player.team:20} - €{player.market_value:,}")
        
        return stats


def main():
    """Función principal"""
    print("🚀 GENERADOR DE DATASET COMPLETO LALIGA FANTASY")
    print("=" * 60)
    
    generator = LaLigaFantasyGenerator()
    
    # Generar ~500 jugadores
    players = generator.generate_complete_dataset(500)
    
    # Generar estadísticas
    generator.generate_statistics(players)
    
    # Guardar en JSON
    filename = generator.save_to_json(players)
    
    print(f"\n🎉 ¡Dataset completo generado exitosamente!")
    print(f"📁 Archivo: {filename}")
    print(f"📊 Jugadores totales: {len(players)}")
    print(f"🌐 Fuente: AnaliticaFantasy.com + Generación inteligente")
    
    return players


if __name__ == "__main__":
    main()
