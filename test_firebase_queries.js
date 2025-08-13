// Test script para verificar las consultas de Firebase
// Ejecutar en la consola del navegador cuando la app esté cargada

async function testFirebaseQueries() {
    console.log('🧪 Iniciando pruebas de consultas Firebase...');
    
    try {
        // Test 1: Consulta principal de jugadores
        console.log('\n📋 Test 1: Consulta de jugadores con orderBy...');
        const playersRef = firestoreFunctions.collection(window.firebaseDb, 'players');
        
        try {
            const q1 = firestoreFunctions.query(
                playersRef,
                firestoreFunctions.where('source', '==', 'FutbolFantasy.com'),
                firestoreFunctions.orderBy('value', 'desc'),
                firestoreFunctions.limit(10)
            );
            
            const snapshot1 = await firestoreFunctions.getDocs(q1);
            console.log('✅ Consulta con índice: OK -', snapshot1.size, 'jugadores');
        } catch (error) {
            console.log('⚠️ Consulta con índice falló:', error.message);
            
            // Probar consulta alternativa
            const q2 = firestoreFunctions.query(
                playersRef,
                firestoreFunctions.where('source', '==', 'FutbolFantasy.com'),
                firestoreFunctions.limit(10)
            );
            
            const snapshot2 = await firestoreFunctions.getDocs(q2);
            console.log('✅ Consulta alternativa: OK -', snapshot2.size, 'jugadores');
        }
        
        // Test 2: Consulta de verificación de duplicados
        console.log('\n🔍 Test 2: Consulta de verificación de duplicados...');
        
        if (window.currentManagerId) {
            try {
                const q3 = firestoreFunctions.query(
                    playersRef,
                    firestoreFunctions.where('managerId', '==', window.currentManagerId),
                    firestoreFunctions.where('name', '==', 'Test Player'),
                    firestoreFunctions.where('team', '==', 'Test Team')
                );
                
                const snapshot3 = await firestoreFunctions.getDocs(q3);
                console.log('✅ Consulta de duplicados con índice: OK');
            } catch (error) {
                console.log('⚠️ Consulta de duplicados falló:', error.message);
                
                // Probar consulta alternativa
                const q4 = firestoreFunctions.query(
                    playersRef,
                    firestoreFunctions.where('managerId', '==', window.currentManagerId)
                );
                
                const snapshot4 = await firestoreFunctions.getDocs(q4);
                console.log('✅ Consulta alternativa de duplicados: OK -', snapshot4.size, 'jugadores');
            }
        } else {
            console.log('ℹ️ No hay manager logueado - saltando test de duplicados');
        }
        
        console.log('\n🎉 Todas las pruebas completadas exitosamente!');
        console.log('📖 Si ves warnings sobre índices, revisa FIREBASE_INDEX_SETUP.md');
        
    } catch (error) {
        console.error('❌ Error en las pruebas:', error);
    }
}

// Ejecutar automáticamente cuando se carga el script
if (typeof window !== 'undefined' && window.firebaseDb) {
    testFirebaseQueries();
} else {
    console.log('⏳ Esperando que Firebase se inicialice...');
    setTimeout(() => {
        if (window.firebaseDb) {
            testFirebaseQueries();
        } else {
            console.log('❌ Firebase no se ha inicializado');
        }
    }, 2000);
}
