/**
 * Script para poblar la base de datos con jugadores desde el frontend
 * Se ejecuta directamente en la consola del navegador
 */

// Datos de muestra de jugadores de LaLiga
const samplePlayers = [
    { id: "bellingham", name: "Jude Bellingham", position: "MED", team: "Real Madrid", value: 105000000, points: 89 },
    { id: "lewandowski", name: "Robert Lewandowski", position: "DEL", team: "FC Barcelona", value: 85000000, points: 92 },
    { id: "vinicius", name: "Vinícius Jr.", position: "DEL", team: "Real Madrid", value: 95000000, points: 88 },
    { id: "pedri", name: "Pedri", position: "MED", team: "FC Barcelona", value: 75000000, points: 85 },
    { id: "benzema", name: "Karim Benzema", position: "DEL", team: "Real Madrid", value: 80000000, points: 90 },
    { id: "gavi", name: "Gavi", position: "MED", team: "FC Barcelona", value: 65000000, points: 82 },
    { id: "modric", name: "Luka Modrić", position: "MED", team: "Real Madrid", value: 45000000, points: 87 },
    { id: "ter-stegen", name: "Marc-André ter Stegen", position: "POR", team: "FC Barcelona", value: 35000000, points: 84 },
    { id: "courtois", name: "Thibaut Courtois", position: "POR", team: "Real Madrid", value: 40000000, points: 86 },
    { id: "rudiger", name: "Antonio Rüdiger", position: "DEF", team: "Real Madrid", value: 55000000, points: 83 },
    { id: "araujo", name: "Ronald Araújo", position: "DEF", team: "FC Barcelona", value: 60000000, points: 81 },
    { id: "koke", name: "Koke", position: "MED", team: "Atlético Madrid", value: 35000000, points: 79 },
    { id: "griezmann", name: "Antoine Griezmann", position: "DEL", team: "Atlético Madrid", value: 50000000, points: 85 },
    { id: "oyarzabal", name: "Mikel Oyarzabal", position: "DEL", team: "Real Sociedad", value: 45000000, points: 80 },
    { id: "isak", name: "Alexander Isak", position: "DEL", team: "Real Sociedad", value: 55000000, points: 82 },
    { id: "oblak", name: "Jan Oblak", position: "POR", team: "Atlético Madrid", value: 38000000, points: 85 },
    { id: "carvajal", name: "Dani Carvajal", position: "DEF", team: "Real Madrid", value: 42000000, points: 81 },
    { id: "alba", name: "Jordi Alba", position: "DEF", team: "FC Barcelona", value: 28000000, points: 78 },
    { id: "carrasco", name: "Yannick Carrasco", position: "MED", team: "Atlético Madrid", value: 40000000, points: 77 },
    { id: "soler", name: "Carlos Soler", position: "MED", team: "Valencia", value: 32000000, points: 76 },
    { id: "aspas", name: "Iago Aspas", position: "DEL", team: "Celta Vigo", value: 25000000, points: 79 },
    { id: "canales", name: "Sergio Canales", position: "MED", team: "Real Betis", value: 28000000, points: 75 },
    { id: "moreno", name: "Gerard Moreno", position: "DEL", team: "Villarreal", value: 35000000, points: 80 },
    { id: "pau-torres", name: "Pau Torres", position: "DEF", team: "Villarreal", value: 45000000, points: 79 },
    { id: "marcos-llorente", name: "Marcos Llorente", position: "MED", team: "Atlético Madrid", value: 38000000, points: 78 }
];

async function populateAvailablePlayers() {
    console.log('🚀 Iniciando población de jugadores disponibles...');
    
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
            const shouldContinue = confirm('¿Quieres reemplazar los jugadores existentes?');
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
        
        // Añadir nuevos jugadores
        console.log(`📥 Añadiendo ${samplePlayers.length} jugadores...`);
        
        let addedCount = 0;
        for (const player of samplePlayers) {
            const playerData = {
                id: player.id,
                name: player.name,
                position: player.position,
                team: player.team,
                value: player.value,
                points: player.points,
                status: 'available',
                updated_at: new Date()
            };
            
            await window.firestoreFunctions.setDoc(
                window.firestoreFunctions.doc(window.firebaseDb, 'available_players', player.id),
                playerData
            );
            
            addedCount++;
            if (addedCount % 5 === 0) {
                console.log(`  📦 Procesados ${addedCount}/${samplePlayers.length} jugadores...`);
            }
        }
        
        console.log(`✅ Se añadieron ${addedCount} jugadores exitosamente!`);
        
        // Mostrar estadísticas
        const stats = samplePlayers.reduce((acc, player) => {
            acc.byPosition[player.position] = (acc.byPosition[player.position] || 0) + 1;
            acc.byTeam[player.team] = (acc.byTeam[player.team] || 0) + 1;
            return acc;
        }, { byPosition: {}, byTeam: {} });
        
        console.log('📈 Estadísticas:');
        console.log('  Por posición:', stats.byPosition);
        console.log('  Por equipo:', stats.byTeam);
        
        console.log('🎉 ¡Base de datos poblada exitosamente!');
        console.log('💡 Ahora los usuarios pueden buscar y añadir jugadores desde la interfaz.');
        
    } catch (error) {
        console.error('💥 Error poblando la base de datos:', error);
    }
}

// Función para verificar el estado de la base de datos
async function checkDatabaseStatus() {
    if (!window.firebaseDb || !window.firestoreFunctions) {
        console.error('❌ Firebase no está inicializado.');
        return;
    }
    
    try {
        const players = await window.firestoreFunctions.getDocs(
            window.firestoreFunctions.collection(window.firebaseDb, 'available_players')
        );
        
        console.log(`📊 Estado de la base de datos:`);
        console.log(`  Jugadores disponibles: ${players.size}`);
        
        if (players.size > 0) {
            const positions = {};
            players.docs.forEach(doc => {
                const data = doc.data();
                positions[data.position] = (positions[data.position] || 0) + 1;
            });
            console.log(`  Por posición:`, positions);
        }
        
    } catch (error) {
        console.error('❌ Error verificando estado:', error);
    }
}

// Exportar funciones para uso en consola
window.populateAvailablePlayers = populateAvailablePlayers;
window.checkDatabaseStatus = checkDatabaseStatus;

console.log('🔧 Funciones de población disponibles:');
console.log('  - populateAvailablePlayers(): Poblar con jugadores de muestra');
console.log('  - checkDatabaseStatus(): Verificar estado actual de la base de datos');
