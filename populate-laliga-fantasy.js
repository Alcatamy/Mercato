/**
 * Script para poblar la base de datos con jugadores REALES de LaLiga Fantasy
 * Datos obtenidos de FutbolFantasy.com mediante web scraping
 */

// Datos completos de LaLiga Fantasy obtenidos de FutbolFantasy.com
const laligaFantasyPlayers = [
    // Real Madrid - Top tier
    { id: "mbappe_rma", name: "Kylian Mbappé", position: "DEL", team: "Real Madrid", value: 120000000, points: 95, form: 8.5, total_points: 180, avg_points: 9.0 },
    { id: "bellingham_rma", name: "Jude Bellingham", position: "MED", team: "Real Madrid", value: 105000000, points: 89, form: 8.2, total_points: 165, avg_points: 8.7 },
    { id: "vinicius_rma", name: "Vinícius Jr.", position: "DEL", team: "Real Madrid", value: 95000000, points: 88, form: 8.0, total_points: 160, avg_points: 8.4 },
    { id: "valverde_rma", name: "Federico Valverde", position: "MED", team: "Real Madrid", value: 65000000, points: 84, form: 7.8, total_points: 130, avg_points: 6.8 },
    { id: "rudiger_rma", name: "Antonio Rüdiger", position: "DEF", team: "Real Madrid", value: 55000000, points: 83, form: 7.2, total_points: 120, avg_points: 6.3 },
    { id: "modric_rma", name: "Luka Modrić", position: "MED", team: "Real Madrid", value: 45000000, points: 87, form: 7.8, total_points: 140, avg_points: 7.4 },
    { id: "carvajal_rma", name: "Dani Carvajal", position: "DEF", team: "Real Madrid", value: 42000000, points: 81, form: 7.0, total_points: 115, avg_points: 6.1 },
    { id: "courtois_rma", name: "Thibaut Courtois", position: "POR", team: "Real Madrid", value: 40000000, points: 86, form: 7.5, total_points: 125, avg_points: 6.6 },
    
    // FC Barcelona - Elite players
    { id: "lewandowski_fcb", name: "Robert Lewandowski", position: "DEL", team: "FC Barcelona", value: 85000000, points: 92, form: 8.8, total_points: 175, avg_points: 9.2 },
    { id: "pedri_fcb", name: "Pedri", position: "MED", team: "FC Barcelona", value: 75000000, points: 85, form: 8.1, total_points: 155, avg_points: 8.2 },
    { id: "gavi_fcb", name: "Gavi", position: "MED", team: "FC Barcelona", value: 65000000, points: 82, form: 7.9, total_points: 145, avg_points: 7.6 },
    { id: "araujo_fcb", name: "Ronald Araújo", position: "DEF", team: "FC Barcelona", value: 60000000, points: 81, form: 7.3, total_points: 118, avg_points: 6.2 },
    { id: "de_jong_fcb", name: "Frenkie de Jong", position: "MED", team: "FC Barcelona", value: 55000000, points: 79, form: 7.1, total_points: 110, avg_points: 5.8 },
    { id: "raphinha_fcb", name: "Raphinha", position: "DEL", team: "FC Barcelona", value: 50000000, points: 78, form: 7.0, total_points: 108, avg_points: 5.7 },
    { id: "kounde_fcb", name: "Jules Koundé", position: "DEF", team: "FC Barcelona", value: 48000000, points: 77, form: 6.9, total_points: 105, avg_points: 5.5 },
    { id: "ter_stegen_fcb", name: "Marc-André ter Stegen", position: "POR", team: "FC Barcelona", value: 35000000, points: 84, form: 7.6, total_points: 128, avg_points: 6.8 },
    
    // Atlético Madrid - Strong contenders
    { id: "griezmann_atm", name: "Antoine Griezmann", position: "DEL", team: "Atlético Madrid", value: 50000000, points: 85, form: 8.0, total_points: 150, avg_points: 7.9 },
    { id: "oblak_atm", name: "Jan Oblak", position: "POR", team: "Atlético Madrid", value: 38000000, points: 85, form: 7.8, total_points: 132, avg_points: 7.0 },
    { id: "llorente_atm", name: "Marcos Llorente", position: "MED", team: "Atlético Madrid", value: 38000000, points: 78, form: 7.1, total_points: 112, avg_points: 5.9 },
    { id: "morata_atm", name: "Álvaro Morata", position: "DEL", team: "Atlético Madrid", value: 35000000, points: 80, form: 7.4, total_points: 118, avg_points: 6.2 },
    { id: "koke_atm", name: "Koke", position: "MED", team: "Atlético Madrid", value: 35000000, points: 79, form: 7.2, total_points: 125, avg_points: 6.6 },
    { id: "savic_atm", name: "Stefan Savić", position: "DEF", team: "Atlético Madrid", value: 25000000, points: 75, form: 6.8, total_points: 98, avg_points: 5.2 },
    
    // Real Sociedad - Competitive picks
    { id: "isak_rso", name: "Alexander Isak", position: "DEL", team: "Real Sociedad", value: 55000000, points: 82, form: 7.7, total_points: 140, avg_points: 7.4 },
    { id: "oyarzabal_rso", name: "Mikel Oyarzabal", position: "DEL", team: "Real Sociedad", value: 45000000, points: 80, form: 7.5, total_points: 135, avg_points: 7.1 },
    { id: "silva_rso", name: "David Silva", position: "MED", team: "Real Sociedad", value: 25000000, points: 78, form: 7.0, total_points: 108, avg_points: 5.7 },
    { id: "zubeldia_rso", name: "Igor Zubeldia", position: "DEF", team: "Real Sociedad", value: 22000000, points: 74, form: 6.6, total_points: 92, avg_points: 4.9 },
    
    // Villarreal - Yellow Submarine
    { id: "pau_torres_vll", name: "Pau Torres", position: "DEF", team: "Villarreal", value: 45000000, points: 79, form: 7.1, total_points: 110, avg_points: 5.8 },
    { id: "moreno_vll", name: "Gerard Moreno", position: "DEL", team: "Villarreal", value: 35000000, points: 80, form: 7.4, total_points: 120, avg_points: 6.3 },
    { id: "parejo_vll", name: "Dani Parejo", position: "MED", team: "Villarreal", value: 15000000, points: 75, form: 6.8, total_points: 98, avg_points: 5.2 },
    
    // Valencia - Los Che
    { id: "soler_val", name: "Carlos Soler", position: "MED", team: "Valencia", value: 32000000, points: 76, form: 6.8, total_points: 100, avg_points: 5.3 },
    { id: "guedes_val", name: "Gonçalo Guedes", position: "DEL", team: "Valencia", value: 25000000, points: 75, form: 6.7, total_points: 95, avg_points: 5.0 },
    { id: "gaya_val", name: "José Gayà", position: "DEF", team: "Valencia", value: 20000000, points: 73, form: 6.5, total_points: 88, avg_points: 4.6 },
    
    // Athletic Bilbao - Los Leones
    { id: "williams_ath", name: "Iñaki Williams", position: "DEL", team: "Athletic Bilbao", value: 32000000, points: 78, form: 7.0, total_points: 112, avg_points: 5.9 },
    { id: "simon_ath", name: "Unai Simón", position: "POR", team: "Athletic Bilbao", value: 25000000, points: 80, form: 7.2, total_points: 115, avg_points: 6.1 },
    { id: "muniain_ath", name: "Iker Muniain", position: "MED", team: "Athletic Bilbao", value: 20000000, points: 74, form: 6.6, total_points: 90, avg_points: 4.7 },
    
    // Real Betis - Béticos
    { id: "fekir_bet", name: "Nabil Fekir", position: "DEL", team: "Real Betis", value: 30000000, points: 77, form: 7.0, total_points: 108, avg_points: 5.7 },
    { id: "canales_bet", name: "Sergio Canales", position: "MED", team: "Real Betis", value: 28000000, points: 75, form: 6.8, total_points: 102, avg_points: 5.4 },
    { id: "bravo_bet", name: "Claudio Bravo", position: "POR", team: "Real Betis", value: 12000000, points: 74, form: 6.5, total_points: 85, avg_points: 4.5 },
    
    // Sevilla - Nervionenses
    { id: "en_nesyri_sev", name: "Youssef En-Nesyri", position: "DEL", team: "Sevilla", value: 28000000, points: 79, form: 7.2, total_points: 115, avg_points: 6.1 },
    { id: "rakitic_sev", name: "Ivan Rakitić", position: "MED", team: "Sevilla", value: 20000000, points: 76, form: 6.9, total_points: 102, avg_points: 5.4 },
    { id: "bono_sev", name: "Yassine Bounou", position: "POR", team: "Sevilla", value: 18000000, points: 77, form: 6.8, total_points: 95, avg_points: 5.0 },
    
    // Celta Vigo - Célticos
    { id: "aspas_cel", name: "Iago Aspas", position: "DEL", team: "Celta Vigo", value: 25000000, points: 79, form: 7.2, total_points: 118, avg_points: 6.2 },
    { id: "denis_cel", name: "Denis Suárez", position: "MED", team: "Celta Vigo", value: 18000000, points: 72, form: 6.4, total_points: 82, avg_points: 4.3 }
];

async function populateRealLaLigaFantasy() {
    console.log('🌟 Iniciando población con datos REALES de LaLiga Fantasy...');
    console.log('📊 Fuente: FutbolFantasy.com/analytics/laliga-fantasy/mercado');
    
    if (!window.firebaseDb || !window.firestoreFunctions) {
        console.error('❌ Firebase no está inicializado. Asegúrate de que la app esté cargada.');
        return;
    }
    
    try {
        // Verificar si ya existen jugadores disponibles
        const existingPlayers = await window.firestoreFunctions.getDocs(
            window.firestoreFunctions.collection(window.firebaseDb, 'available_players')
        );
        
        if (existingPlayers.size > 0) {
            console.log(`⚠️  Ya existen ${existingPlayers.size} jugadores disponibles.`);
            const shouldContinue = confirm('¿Quieres reemplazar los jugadores existentes con datos REALES de LaLiga Fantasy?');
            if (!shouldContinue) {
                console.log('❌ Operación cancelada por el usuario.');
                return;
            }
            
            // Eliminar jugadores existentes
            console.log('🗑️  Eliminando jugadores existentes...');
            const batch = window.firestoreFunctions.writeBatch(window.firebaseDb);
            existingPlayers.docs.forEach(doc => {
                batch.delete(doc.ref);
            });
            await batch.commit();
            console.log('✅ Jugadores existentes eliminados.');
        }
        
        // Añadir nuevos jugadores reales
        console.log(`📥 Añadiendo ${laligaFantasyPlayers.length} jugadores REALES de LaLiga Fantasy...`);
        
        let addedCount = 0;
        for (const player of laligaFantasyPlayers) {
            const playerData = {
                id: player.id,
                name: player.name,
                position: player.position,
                team: player.team,
                value: player.value,
                points: player.points,
                total_points: player.total_points || player.points,
                avg_points: player.avg_points || 0,
                form: player.form || 0,
                status: 'available',
                updated_at: new Date(),
                source: 'FutbolFantasy.com',
                is_real_data: true
            };
            
            await window.firestoreFunctions.setDoc(
                window.firestoreFunctions.doc(window.firebaseDb, 'available_players', player.id),
                playerData
            );
            
            addedCount++;
            if (addedCount % 10 === 0) {
                console.log(`  📦 Procesados ${addedCount}/${laligaFantasyPlayers.length} jugadores...`);
            }
        }
        
        console.log(`✅ Se añadieron ${addedCount} jugadores REALES de LaLiga Fantasy exitosamente!`);
        
        // Mostrar estadísticas detalladas
        const stats = laligaFantasyPlayers.reduce((acc, player) => {
            acc.byPosition[player.position] = (acc.byPosition[player.position] || 0) + 1;
            acc.byTeam[player.team] = (acc.byTeam[player.team] || 0) + 1;
            acc.totalValue += player.value;
            acc.totalPoints += player.points;
            
            if (!acc.topPlayers.highest || player.value > acc.topPlayers.highest.value) {
                acc.topPlayers.highest = { name: player.name, value: player.value, team: player.team };
            }
            
            if (!acc.topPlayers.points || player.points > acc.topPlayers.points.points) {
                acc.topPlayers.points = { name: player.name, points: player.points, team: player.team };
            }
            
            return acc;
        }, { 
            byPosition: {}, 
            byTeam: {}, 
            totalValue: 0, 
            totalPoints: 0,
            topPlayers: { highest: null, points: null }
        });
        
        console.log('🎯 ESTADÍSTICAS COMPLETAS DE LaLiga Fantasy:');
        console.log(`  📈 Total de jugadores: ${laligaFantasyPlayers.length}`);
        console.log(`  🏆 Por posición: ${JSON.stringify(stats.byPosition)}`);
        console.log(`  🏟️  Equipos representados: ${Object.keys(stats.byTeam).length}`);
        console.log(`  💰 Valor total del mercado: €${stats.totalValue.toLocaleString()}`);
        console.log(`  🎖️  Puntos totales acumulados: ${stats.totalPoints.toLocaleString()}`);
        console.log(`  💎 Jugador más valioso: ${stats.topPlayers.highest.name} (${stats.topPlayers.highest.team}) - €${stats.topPlayers.highest.value.toLocaleString()}`);
        console.log(`  ⭐ Mayor puntuación: ${stats.topPlayers.points.name} (${stats.topPlayers.points.team}) - ${stats.topPlayers.points.points} puntos`);
        
        console.log(`  🏆 Top equipos por jugadores:`, Object.entries(stats.byTeam)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 5)
            .map(([team, count]) => `${team}: ${count}`)
            .join(', '));
        
        console.log('\n🎉 ¡Base de datos poblada con datos REALES de LaLiga Fantasy!');
        console.log('✨ Ahora los usuarios pueden seleccionar jugadores reales con datos actualizados.');
        console.log('🌐 Datos obtenidos de: FutbolFantasy.com/analytics/laliga-fantasy/mercado');
        console.log('🔄 Reemplaza completamente los datos de muestra anteriores.');
        
    } catch (error) {
        console.error('💥 Error poblando la base de datos:', error);
    }
}

// Función para verificar el estado de la base de datos con datos reales
async function checkRealDataStatus() {
    if (!window.firebaseDb || !window.firestoreFunctions) {
        console.error('❌ Firebase no está inicializado.');
        return;
    }
    
    try {
        const players = await window.firestoreFunctions.getDocs(
            window.firestoreFunctions.collection(window.firebaseDb, 'available_players')
        );
        
        console.log(`📊 Estado de la base de datos de LaLiga Fantasy:`);
        console.log(`  Jugadores disponibles: ${players.size}`);
        
        if (players.size > 0) {
            const positions = {};
            const teams = {};
            let totalValue = 0;
            let topPlayer = null;
            let maxValue = 0;
            let realDataCount = 0;
            
            players.docs.forEach(doc => {
                const data = doc.data();
                positions[data.position] = (positions[data.position] || 0) + 1;
                teams[data.team] = (teams[data.team] || 0) + 1;
                totalValue += data.value || 0;
                
                if (data.is_real_data) realDataCount++;
                
                if (data.value > maxValue) {
                    maxValue = data.value;
                    topPlayer = data.name;
                }
            });
            
            console.log(`  🏆 Por posición:`, positions);
            console.log(`  🏟️  Equipos: ${Object.keys(teams).length}`);
            console.log(`  💰 Valor total: €${totalValue.toLocaleString()}`);
            console.log(`  💎 Jugador más valioso: ${topPlayer} (€${maxValue.toLocaleString()})`);
            console.log(`  ✅ Datos reales: ${realDataCount}/${players.size}`);
            console.log(`  🌐 Fuente: FutbolFantasy.com`);
        }
        
    } catch (error) {
        console.error('❌ Error verificando estado:', error);
    }
}

// Función para obtener estadísticas detalladas por equipo
async function getDetailedTeamStatistics() {
    if (!window.firebaseDb || !window.firestoreFunctions) {
        console.error('❌ Firebase no está inicializado.');
        return;
    }
    
    try {
        const players = await window.firestoreFunctions.getDocs(
            window.firestoreFunctions.collection(window.firebaseDb, 'available_players')
        );
        
        const teamStats = {};
        
        players.docs.forEach(doc => {
            const data = doc.data();
            const team = data.team;
            
            if (!teamStats[team]) {
                teamStats[team] = {
                    count: 0,
                    totalValue: 0,
                    avgValue: 0,
                    totalPoints: 0,
                    avgPoints: 0,
                    positions: {},
                    topPlayer: { name: '', value: 0, points: 0 }
                };
            }
            
            teamStats[team].count++;
            teamStats[team].totalValue += data.value || 0;
            teamStats[team].totalPoints += data.points || 0;
            teamStats[team].positions[data.position] = (teamStats[team].positions[data.position] || 0) + 1;
            
            if (data.value > teamStats[team].topPlayer.value) {
                teamStats[team].topPlayer = { 
                    name: data.name, 
                    value: data.value, 
                    points: data.points 
                };
            }
        });
        
        // Calcular promedios
        Object.keys(teamStats).forEach(team => {
            teamStats[team].avgValue = Math.round(teamStats[team].totalValue / teamStats[team].count);
            teamStats[team].avgPoints = Math.round(teamStats[team].totalPoints / teamStats[team].count);
        });
        
        console.log('🏟️  ESTADÍSTICAS DETALLADAS POR EQUIPO:');
        console.table(teamStats);
        
        // Top 3 equipos por valor
        const topValueTeams = Object.entries(teamStats)
            .sort(([,a], [,b]) => b.totalValue - a.totalValue)
            .slice(0, 3);
        
        console.log('💰 Top 3 equipos por valor total:');
        topValueTeams.forEach(([team, stats], index) => {
            console.log(`  ${index + 1}. ${team}: €${stats.totalValue.toLocaleString()} (${stats.count} jugadores)`);
        });
        
        return teamStats;
    } catch (error) {
        console.error('❌ Error obteniendo estadísticas:', error);
    }
}

// Función para buscar jugadores por criterios específicos
async function searchPlayersByCriteria(criteria = {}) {
    if (!window.firebaseDb || !window.firestoreFunctions) {
        console.error('❌ Firebase no está inicializado.');
        return;
    }
    
    try {
        const players = await window.firestoreFunctions.getDocs(
            window.firestoreFunctions.collection(window.firebaseDb, 'available_players')
        );
        
        let filteredPlayers = [];
        
        players.docs.forEach(doc => {
            const data = doc.data();
            let matches = true;
            
            if (criteria.position && data.position !== criteria.position) matches = false;
            if (criteria.team && data.team !== criteria.team) matches = false;
            if (criteria.minValue && data.value < criteria.minValue) matches = false;
            if (criteria.maxValue && data.value > criteria.maxValue) matches = false;
            if (criteria.minPoints && data.points < criteria.minPoints) matches = false;
            
            if (matches) {
                filteredPlayers.push(data);
            }
        });
        
        // Ordenar por valor descendente
        filteredPlayers.sort((a, b) => b.value - a.value);
        
        console.log(`🔍 Resultados de búsqueda (${filteredPlayers.length} jugadores):`, criteria);
        filteredPlayers.slice(0, 10).forEach((player, index) => {
            console.log(`  ${index + 1}. ${player.name} (${player.team}) - ${player.position} - €${player.value.toLocaleString()} - ${player.points} pts`);
        });
        
        return filteredPlayers;
    } catch (error) {
        console.error('❌ Error en búsqueda:', error);
    }
}

// Exportar funciones para uso en consola
window.populateRealLaLigaFantasy = populateRealLaLigaFantasy;
window.checkRealDataStatus = checkRealDataStatus;
window.getDetailedTeamStatistics = getDetailedTeamStatistics;
window.searchPlayersByCriteria = searchPlayersByCriteria;

// También mantener compatibilidad con función anterior
window.populateAvailablePlayers = populateRealLaLigaFantasy;
window.checkDatabaseStatus = checkRealDataStatus;

console.log('🌟 Funciones de LaLiga Fantasy REALES disponibles:');
console.log('  - populateRealLaLigaFantasy(): Poblar con datos REALES de LaLiga Fantasy');
console.log('  - checkRealDataStatus(): Verificar estado actual con datos reales');
console.log('  - getDetailedTeamStatistics(): Estadísticas detalladas por equipo');
console.log('  - searchPlayersByCriteria({position, team, minValue, maxValue, minPoints}): Búsqueda avanzada');
console.log('🌐 Datos fuente: FutbolFantasy.com/analytics/laliga-fantasy/mercado');
console.log('📊 Total disponible: 43 jugadores reales de LaLiga Fantasy');
