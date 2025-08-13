/**
 * Dataset completo de 500 jugadores de LaLiga Fantasy
 * Generado desde AnaliticaFantasy.com + Generación inteligente
 */

// Importar el dataset JSON generado
import fs from 'fs';
import path from 'path';

// Leer el archivo JSON generado
const datasetPath = path.join(process.cwd(), 'backend', 'laliga_fantasy_complete.json');

function generateJavaScriptDataset() {
    try {
        // Leer el archivo JSON
        if (!fs.existsSync(datasetPath)) {
            console.log('❌ Archivo de dataset no encontrado:', datasetPath);
            console.log('📝 Ejecuta primero generate_complete_dataset.py');
            return;
        }
        
        const rawData = fs.readFileSync(datasetPath, 'utf8');
        const dataset = JSON.parse(rawData);
        
        console.log(`📊 Dataset cargado: ${dataset.players.length} jugadores`);
        
        // Generar código JavaScript
        const jsContent = `/**
 * Dataset completo de LaLiga Fantasy
 * Fuente: AnaliticaFantasy.com + Generación inteligente
 * Total: ${dataset.players.length} jugadores
 * Valor total: €${dataset.total_market_value.toLocaleString()}
 * Fecha generación: ${new Date().toISOString()}
 */

export const laliga500Players = ${JSON.stringify(dataset.players, null, 2)};

export const datasetInfo = {
    total_players: ${dataset.players.length},
    total_market_value: ${dataset.total_market_value},
    generated_at: "${new Date().toISOString()}",
    source: "AnaliticaFantasy.com + Generated",
    version: "complete_500"
};

export default {
    players: laliga500Players,
    info: datasetInfo
};`;
        
        // Escribir archivo JavaScript
        const outputPath = path.join(process.cwd(), 'frontend', 'populate-laliga-500.js');
        fs.writeFileSync(outputPath, jsContent, 'utf8');
        
        console.log(`✅ Dataset JavaScript generado: ${outputPath}`);
        console.log(`📊 ${dataset.players.length} jugadores exportados`);
        
        // Generar estadísticas
        const stats = dataset.players.reduce((acc, player) => {
            acc.byPosition[player.position] = (acc.byPosition[player.position] || 0) + 1;
            acc.byTeam[player.team] = (acc.byTeam[player.team] || 0) + 1;
            return acc;
        }, { byPosition: {}, byTeam: {} });
        
        console.log('📈 Estadísticas:');
        console.log('  Por posición:', stats.byPosition);
        console.log('  Equipos representados:', Object.keys(stats.byTeam).length);
        
    } catch (error) {
        console.error('❌ Error generando dataset JavaScript:', error);
    }
}

// Ejecutar si es llamado directamente
if (import.meta.url === `file://${process.argv[1]}`) {
    generateJavaScriptDataset();
}

export { generateJavaScriptDataset };
