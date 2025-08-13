// Aplicación principal - Mercado La Liga El Rancho
// Funciones Firebase se cargarán dinámicamente desde CDN

let firebaseLoaded = false;
let firestoreFunctions = {};

// Variables globales
let currentManagerId = null;
let managers = [];
let allPlayers = [];
let marketItems = [];
let auctionItems = [];
let tradeItems = [];

// Rutas de las colecciones en Firestore
const COLLECTIONS = {
    managers: 'managers',
    players: 'players',
    market: 'market',
    auctions: 'auctions',
    trades: 'trades'
};

// Claves de acceso para managers
const managerKeys = {
    'alcatamy-esports-by-rolex': 'ALCA-2025',
    'vigar-fc': 'VIGA-2025',
    'baena10': 'BA10-2025',
    'dubai-city-fc': 'DUBA-2025',
    'visite-la-manga-fc': 'MANGA-2025',
    'morenazos-fc': 'MORE-2025'
};

const managerNames = [
    "Alcatamy eSports by Rolex", 
    "Vigar FC", 
    "Baena10", 
    "Dubai cITY FC", 
    "Visite La Manga FC", 
    "Morenazos FC"
];

const positions = ["POR", "DEF", "MED", "DEL"];

// Cargar funciones de Firestore dinámicamente
async function loadFirestoreFunctions() {
    if (firebaseLoaded) return;
    
    try {
        const { 
            collection, 
            onSnapshot, 
            addDoc, 
            updateDoc, 
            deleteDoc, 
            writeBatch, 
            query, 
            where, 
            getDocs, 
            doc, 
            getDoc, 
            setDoc,
            limit,
            orderBy
        } = await import("https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js");
        
        const { signInAnonymously } = await import("https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js");
        
        firestoreFunctions = {
            collection, onSnapshot, addDoc, updateDoc, deleteDoc, 
            writeBatch, query, where, getDocs, doc, getDoc, setDoc,
            limit, orderBy, signInAnonymously
        };
        
        firebaseLoaded = true;
        console.log('✅ Funciones de Firestore cargadas');
    } catch (error) {
        console.error('❌ Error cargando Firebase:', error);
        throw error;
    }
}

// Inicialización de la aplicación
async function initializeApp() {
    document.getElementById('loading-spinner').classList.remove('hidden');
    
    try {
        // Esperar a que Firebase esté disponible
        let retries = 0;
        while (!window.firebaseAuth && retries < 50) {
            await new Promise(resolve => setTimeout(resolve, 100));
            retries++;
        }
        
        if (!window.firebaseAuth) {
            throw new Error('Firebase no se cargó correctamente');
        }
        
        // Cargar funciones de Firestore
        await loadFirestoreFunctions();
        
        // Autenticación anónima
        await firestoreFunctions.signInAnonymously(window.firebaseAuth);
        console.log('✅ Autenticado en Firebase');
        
        // Configurar datos iniciales
        await setupInitialData();
        
        // Escuchar cambios en tiempo real
        listenToAllChanges();
        
        // Configurar event listeners
        setupEventListeners();
        
        console.log('🎉 Aplicación inicializada correctamente');
        
    } catch (error) {
        console.error("Error en la inicialización:", error);
        showMessageModal(
            'Error de Conexión', 
            `No se pudo conectar con la base de datos. Por favor, refresca la página. Error: ${error.message}`, 
            'fa-exclamation-triangle text-red-500'
        );
    } finally {
        document.getElementById('loading-spinner').classList.add('hidden');
    }
}

// Configurar datos iniciales en Firebase
async function setupInitialData() {
    const managersRef = firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.managers);
    const managersSnapshot = await firestoreFunctions.getDocs(managersRef);
    
    if (managersSnapshot.empty) {
        console.log("Creando managers iniciales...");
        const batch = firestoreFunctions.writeBatch(window.firebaseDb);
        
        managerNames.forEach(name => {
            const id = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
            batch.set(firestoreFunctions.doc(window.firebaseDb, COLLECTIONS.managers, id), { 
                name: name,
                createdAt: new Date()
            });
        });
        
        await batch.commit();
        console.log("✅ Managers iniciales creados");
    }
}

// Escuchar cambios en tiempo real
function listenToAllChanges() {
    // Managers
    firestoreFunctions.onSnapshot(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.managers), snapshot => {
        managers = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        populateManagerSelect();
        if (currentManagerId) renderAllTabs();
    });

    // Players
    firestoreFunctions.onSnapshot(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.players), snapshot => {
        allPlayers = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        if (currentManagerId) renderAllTabs();
    });

    // Market
    firestoreFunctions.onSnapshot(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.market), snapshot => {
        marketItems = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        if (currentManagerId) {
            renderMarketTab();
            renderSquadTab();
        }
    });

    // Auctions
    firestoreFunctions.onSnapshot(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.auctions), snapshot => {
        auctionItems = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        if (currentManagerId) {
            renderAuctionsTab();
            renderSquadTab();
        }
    });

    // Trades
    firestoreFunctions.onSnapshot(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.trades), snapshot => {
        tradeItems = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        if (currentManagerId) {
            renderTradesTab();
            renderSquadTab();
        }
    });
}

// Configurar event listeners
function setupEventListeners() {
    document.getElementById('manager-select').addEventListener('change', (e) => {
        const selectedManagerId = e.target.value;
        if (selectedManagerId) {
            openKeyPromptModal(selectedManagerId);
        } else {
            currentManagerId = null;
            document.getElementById('main-content').classList.add('hidden');
        }
    });
}

// Poblar selector de managers
function populateManagerSelect() {
    const select = document.getElementById('manager-select');
    const currentSelection = select.value;
    
    select.innerHTML = '<option value="">-- Elige tu manager --</option>';
    
    managers.sort((a, b) => a.name.localeCompare(b.name)).forEach(manager => {
        const option = document.createElement('option');
        option.value = manager.id;
        option.textContent = manager.name;
        select.appendChild(option);
    });
    
    select.value = currentSelection;
}

// Funciones de navegación por tabs
window.showTab = (tabName) => {
    document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('tab-active'));
    
    document.getElementById(`tab-content-${tabName}`).classList.remove('hidden');
    document.getElementById(`tab-${tabName}`).classList.add('tab-active');
    
    renderAllTabs();
};

function renderAllTabs() {
    if (!currentManagerId) return;
    
    renderSquadTab();
    renderStandingsTab();
    renderMarketTab();
    renderAuctionsTab();
    renderTradesTab();
}

// Obtener estado de un jugador
function getPlayerStatus(playerId) {
    if (marketItems.some(item => item.playerId === playerId)) {
        return { status: 'market', text: 'EN VENTA', class: 'bg-blue-500' };
    }
    if (auctionItems.some(item => item.playerId === playerId)) {
        return { status: 'auction', text: 'SUBASTA', class: 'bg-red-500' };
    }
    if (tradeItems.some(trade => 
        (trade.proposerPlayers.includes(playerId) || trade.receiverPlayers.includes(playerId)) 
        && trade.status === 'pending'
    )) {
        return { status: 'trade', text: 'EN INTERCAMBIO', class: 'bg-purple-500' };
    }
    return null;
}

// Renderizar tab de plantilla
function renderSquadTab() {
    const container = document.getElementById('tab-content-squad');
    const myPlayers = allPlayers.filter(p => p.ownerId === currentManagerId);
    
    container.innerHTML = `
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
            <div class="p-4 border-b grid grid-cols-1 md:grid-cols-2 gap-4">
                <button onclick="openTradeModal()" class="w-full bg-purple-600 text-white px-4 py-3 rounded-lg font-semibold hover:bg-purple-700 transition shadow-md flex items-center justify-center text-lg">
                    <i class="fas fa-exchange-alt mr-3"></i>Proponer Intercambio
                </button>
                <button onclick="openEditSquadModal()" class="w-full bg-green-600 text-white px-4 py-3 rounded-lg font-semibold hover:bg-green-700 transition shadow-md flex items-center justify-center text-lg">
                    <i class="fas fa-edit mr-3"></i>Editar Plantilla
                </button>
            </div>
            <ul class="divide-y divide-gray-200">
                ${myPlayers.length === 0 ? 
                    `<li class="p-8 text-center text-gray-500">Tu plantilla está vacía. Añade jugadores desde "Editar Plantilla".</li>` : 
                    myPlayers.map(player => {
                        const status = getPlayerStatus(player.id);
                        return `
                        <li class="p-4 flex items-center justify-between hover:bg-gray-50 transition">
                            <div class="flex items-center">
                                <p class="font-semibold text-lg text-gray-800">${player.name}</p>
                                ${status ? `<span class="ml-3 px-2 py-1 text-xs font-semibold text-white ${status.class} rounded-full">${status.text}</span>` : ''}
                            </div>
                            <div class="flex items-center space-x-2">
                                <p class="text-sm text-gray-500 hidden md:block">${player.position} - ${formatCurrency(player.value)}</p>
                                <button ${status ? 'disabled' : ''} onclick="openSellModal('${player.id}')" class="bg-blue-500 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-blue-600 transition shadow disabled:opacity-50 disabled:cursor-not-allowed" title="Vender">
                                    <i class="fas fa-dollar-sign"></i>
                                </button>
                                <button ${status ? 'disabled' : ''} onclick="openAuctionModal('${player.id}')" class="bg-red-500 text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-red-600 transition shadow disabled:opacity-50 disabled:cursor-not-allowed" title="Subastar">
                                    <i class="fas fa-gavel"></i>
                                </button>
                            </div>
                        </li>
                    `}).join('')
                }
            </ul>
        </div>
    `;
}

// Renderizar tab de mercado
async function renderMarketTab() {
    const container = document.getElementById('tab-content-market');
    
    if (marketItems.length === 0) {
        container.innerHTML = `<div class="text-center p-8 bg-white rounded-xl shadow-md"><p class="text-gray-500">El mercado está tranquilo... de momento.</p></div>`;
        return;
    }

    let html = '<div class="space-y-4">';
    
    for (const item of marketItems) {
        const offersSnapshot = await firestoreFunctions.getDocs(firestoreFunctions.collection(window.firebaseDb, `${COLLECTIONS.market}/${item.id}/offers`));
        const offers = offersSnapshot.docs.map(doc => ({id: doc.id, ...doc.data()}));

        html += `
            <div class="bg-white rounded-xl shadow-md p-4 animate-pulse-once">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="font-bold text-xl text-gray-800">${item.playerName}</p>
                        <p class="text-sm text-gray-500">Vendido por: ${item.sellerName}</p>
                        <p class="text-lg font-semibold text-green-600 mt-1">Precio: ${formatCurrency(item.price)}</p>
                    </div>
                    ${item.sellerId !== currentManagerId ? `
                    <button onclick="openOfferModal('${item.id}')" class="bg-green-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-600 transition shadow-md">Hacer Oferta</button>
                    ` : `
                    <button onclick="cancelSale('${item.id}')" class="bg-gray-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-600 transition shadow-md">Retirar</button>
                    `}
                </div>
                ${item.sellerId === currentManagerId ? `
                <div class="mt-4 border-t pt-4">
                    <h4 class="font-semibold mb-2">Ofertas recibidas:</h4>
                    ${offers.length > 0 ? `
                        <ul class="space-y-2">
                            ${offers.map(offer => `
                                <li class="p-2 bg-gray-100 rounded-lg flex justify-between items-center">
                                    <div>
                                        <p><span class="font-medium">${offer.buyerName}</span> ofrece <span class="font-semibold text-green-700">${formatCurrency(offer.amount)}</span></p>
                                    </div>
                                    <button onclick="acceptOffer('${item.id}', '${offer.id}')" class="bg-blue-500 text-white px-3 py-1 text-sm rounded-md hover:bg-blue-600">Aceptar</button>
                                </li>
                            `).join('')}
                        </ul>
                    ` : `<p class="text-sm text-gray-500">Aún no hay ofertas.</p>`}
                </div>
                ` : ''}
            </div>
        `;
    }
    
    html += '</div>';
    container.innerHTML = html;
}

// Modal de edición de plantilla
window.openEditSquadModal = async () => {
    const content = `
        <div class="p-6" style="max-height: 90vh; overflow-y: auto;">
            <h3 class="text-2xl font-bold mb-4 text-center">Editar Plantilla</h3>
            
            <!-- Solo búsqueda de jugadores reales de FutbolFantasy -->
            <div class="bg-blue-50 p-4 rounded-lg mb-4">
                <div class="flex items-center mb-2">
                    <i class="fas fa-star text-yellow-500 mr-2"></i>
                    <h4 class="font-semibold text-blue-800">Buscar Jugadores de FutbolFantasy.com</h4>
                </div>
                <p class="text-sm text-blue-700">Solo puedes añadir jugadores reales de LaLiga Fantasy</p>
                
                <!-- Filtros de búsqueda -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
                    <div>
                        <input type="text" id="player-search" placeholder="Buscar por nombre..." class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500" oninput="searchRealPlayers()">
                    </div>
                    <div>
                        <select id="team-filter" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500" onchange="searchRealPlayers()">
                            <option value="">Todos los equipos</option>
                        </select>
                    </div>
                    <div>
                        <select id="value-filter" class="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500" onchange="searchRealPlayers()">
                            <option value="">Cualquier valor</option>
                            <option value="0-10000000">Hasta 10M €</option>
                            <option value="10000000-50000000">10M - 50M €</option>
                            <option value="50000000-100000000">50M - 100M €</option>
                            <option value="100000000-999999999">Más de 100M €</option>
                        </select>
                    </div>
                </div>
                
                <!-- Loading y resultados -->
                <div id="players-loading" class="text-center py-4 hidden">
                    <i class="fas fa-spinner fa-spin text-blue-500"></i>
                    <p class="text-gray-600 mt-2">Buscando jugadores...</p>
                </div>
                
                <div id="players-results" class="max-h-64 overflow-y-auto border rounded-lg bg-white mt-4">
                    <div class="p-4 text-center text-gray-500">
                        <i class="fas fa-search fa-2x mb-2"></i>
                        <p>Busca jugadores por nombre o filtra por equipo/valor</p>
                        <p class="text-sm mt-1">Se mostrarán los primeros 50 resultados</p>
                    </div>
                </div>
            </div>
            
            <!-- Plantilla actual -->
            <div id="edit-squad-list-container" class="mt-6">
                <h4 class="font-semibold mb-2">Plantilla Actual</h4>
                <div class="max-h-48 overflow-y-auto border rounded-lg bg-white"></div>
            </div>
            
            <div class="mt-6 flex justify-end">
                <button onclick="closeModal()" class="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-bold">Cerrar</button>
            </div>
        </div>
    `;

    openModal(content);
    renderEditSquadList();
    
    // Cargar equipos para el filtro y jugadores iniciales
    setTimeout(() => {
        loadTeamsForFilter();
        searchRealPlayers();
    }, 500);
};

// Añadir jugador a plantilla
window.addPlayerToSquad = async () => {
    const nameInput = document.getElementById('new-player-name');
    const valueInput = document.getElementById('new-player-value');
    const positionSelect = document.getElementById('new-player-position');

    const name = nameInput.value.trim();
    const value = Number(valueInput.value);
    const position = positionSelect.value;

    if (!name || !value || value <= 0) {
        showMessageModal('Datos incompletos', 'Por favor, introduce un nombre y un valor válido para el jugador.', 'fa-exclamation-circle text-yellow-500');
        return;
    }
    
    const manager = managers.find(m => m.id === currentManagerId);
    try {
        await firestoreFunctions.addDoc(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.players), {
            name,
            position,
            value,
            ownerId: manager.id,
            ownerName: manager.name
        });
        nameInput.value = '';
        valueInput.value = '';
        nameInput.focus();
        // The onSnapshot listener will automatically re-render the list
    } catch (e) {
        console.error("Error al añadir jugador:", e);
        showMessageModal('Error', 'No se pudo añadir el jugador.', 'fa-times-circle text-red-500');
    }
};

// Funciones para la búsqueda de jugadores de la API
let searchTimeout;
let cachedPlayers = [];

// Variables para la búsqueda
let cachedRealPlayers = [];
let teamsCache = [];

// Cargar equipos para el filtro
window.loadTeamsForFilter = async () => {
    try {
        if (teamsCache.length === 0) {
            const playersSnapshot = await firestoreFunctions.getDocs(
                firestoreFunctions.query(
                    firestoreFunctions.collection(window.firebaseDb, 'players'),
                    firestoreFunctions.where('source', '==', 'FutbolFantasy.com')
                )
            );
            
            const teams = new Set();
            playersSnapshot.forEach(doc => {
                const player = doc.data();
                if (player.team && player.team !== 'N/A') {
                    teams.add(player.team);
                }
            });
            
            teamsCache = Array.from(teams).sort();
        }
        
        const teamFilter = document.getElementById('team-filter');
        if (teamFilter) {
            teamFilter.innerHTML = '<option value="">Todos los equipos</option>' +
                teamsCache.map(team => `<option value="${team}">${team}</option>`).join('');
        }
        
    } catch (error) {
        console.error('Error cargando equipos:', error);
    }
};

// Buscar jugadores reales de FutbolFantasy
window.searchRealPlayers = () => {
    // Limpiar timeout anterior
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    // Debounce la búsqueda
    searchTimeout = setTimeout(async () => {
        const searchInput = document.getElementById('player-search');
        const teamFilter = document.getElementById('team-filter');
        const valueFilter = document.getElementById('value-filter');
        const resultsContainer = document.getElementById('players-results');
        const loadingContainer = document.getElementById('players-loading');
        
        const searchQuery = searchInput?.value?.trim().toLowerCase() || '';
        const selectedTeam = teamFilter?.value || '';
        const selectedValueRange = valueFilter?.value || '';
        
        // Mostrar loading
        loadingContainer.classList.remove('hidden');
        
        try {
            let players = [];
            
            // Obtener jugadores de FutbolFantasy.com desde Firebase
            const playersRef = firestoreFunctions.collection(window.firebaseDb, 'players');
            
            let q;
            if (searchQuery && searchQuery.length >= 3) {
                // Búsqueda optimizada por nombre cuando hay query específico
                q = firestoreFunctions.query(
                    playersRef,
                    firestoreFunctions.where('source', '==', 'FutbolFantasy.com'),
                    firestoreFunctions.where('name_lowercase', '>=', searchQuery),
                    firestoreFunctions.where('name_lowercase', '<=', searchQuery + '\uf8ff'),
                    firestoreFunctions.limit(50)
                );
            } else {
                // Consulta general
                q = firestoreFunctions.query(
                    playersRef,
                    firestoreFunctions.where('source', '==', 'FutbolFantasy.com'),
                    firestoreFunctions.limit(100)
                );
            }
            
            const playersSnapshot = await firestoreFunctions.getDocs(q);
            
            playersSnapshot.forEach(doc => {
                const player = doc.data();
                player.id = doc.id;
                players.push(player);
            });
            
            // Aplicar filtros
            let filteredPlayers = players;
            
            // Filtro por nombre - mejorado para búsqueda eficiente
            if (searchQuery) {
                // Si el campo name_lowercase existe, usarlo para búsqueda más eficiente
                filteredPlayers = filteredPlayers.filter(player => {
                    const nameSearch = (player.name_lowercase || player.name.toLowerCase()).includes(searchQuery);
                    const teamSearch = (player.team_lowercase || player.team.toLowerCase()).includes(searchQuery);
                    return nameSearch || teamSearch;
                });
            }
            
            // Filtro por equipo
            if (selectedTeam) {
                filteredPlayers = filteredPlayers.filter(player => player.team === selectedTeam);
            }
            
            // Filtro por valor
            if (selectedValueRange) {
                const [min, max] = selectedValueRange.split('-').map(Number);
                filteredPlayers = filteredPlayers.filter(player => {
                    const value = player.value || 0;
                    return value >= min && value <= max;
                });
            }
            
            // Ordenar por valor (de mayor a menor)
            filteredPlayers.sort((a, b) => (b.value || 0) - (a.value || 0));
            
            // Limitar a 50 resultados
            filteredPlayers = filteredPlayers.slice(0, 50);
            
            renderRealPlayersResults(filteredPlayers);
            
        } catch (error) {
            console.error('Error buscando jugadores:', error);
            resultsContainer.innerHTML = `
                <div class="p-4 text-center text-red-500">
                    <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                    <p>Error al buscar jugadores</p>
                    <p class="text-sm">${error.message}</p>
                </div>
            `;
        } finally {
            loadingContainer.classList.add('hidden');
        }
    }, 300);
};

// Renderizar resultados de jugadores reales
function renderRealPlayersResults(players) {
    const container = document.getElementById('players-results');
    
    if (!players || players.length === 0) {
        container.innerHTML = `
            <div class="p-4 text-center text-gray-500">
                <i class="fas fa-search fa-2x mb-2"></i>
                <p>No se encontraron jugadores</p>
                <p class="text-sm">Prueba con otros filtros de búsqueda</p>
            </div>
        `;
        return;
    }
    
    const playersHTML = players.map(player => `
        <div class="p-3 border-b hover:bg-gray-50 transition-colors">
            <div class="flex justify-between items-center">
                <div class="flex-1">
                    <div class="flex items-center mb-1">
                        <h5 class="font-semibold text-gray-800">${player.name}</h5>
                        <span class="ml-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">${player.team}</span>
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                        <i class="fas fa-euro-sign mr-1"></i>
                        <span class="font-medium">${formatCurrency(player.value || 0)}</span>
                        <span class="ml-3 text-xs text-gray-500">
                            <i class="fas fa-globe mr-1"></i>FutbolFantasy.com
                        </span>
                    </div>
                </div>
                <button 
                    onclick="addRealPlayerToSquad('${player.id}', '${player.name}', '${player.team}', ${player.value || 0})"
                    class="bg-green-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-600 transition shadow">
                    <i class="fas fa-plus mr-1"></i>Añadir
                </button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = playersHTML;
}

// Añadir jugador real a la plantilla
window.addRealPlayerToSquad = async (playerId, name, team, value) => {
    try {
        // Verificar si el jugador ya está en la plantilla del manager actual
        const squadSnapshot = await firestoreFunctions.getDocs(
            firestoreFunctions.query(
                firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.players),
                firestoreFunctions.where('managerId', '==', currentManagerId),
                firestoreFunctions.where('name', '==', name),
                firestoreFunctions.where('team', '==', team)
            )
        );
        
        if (!squadSnapshot.empty) {
            showMessageModal('¡Jugador ya en plantilla!', `${name} ya está en tu plantilla.`, 'fa-exclamation-triangle text-yellow-500');
            return;
        }
        
        // Añadir jugador a la plantilla
        await firestoreFunctions.addDoc(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.players), {
            name: name,
            team: team,
            value: value,
            managerId: currentManagerId,
            status: 'squad',
            source: 'FutbolFantasy.com',
            originalId: playerId,
            dateAdded: new Date()
        });
        
        showMessageModal('¡Jugador Añadido!', `${name} ha sido añadido a tu plantilla.`, 'fa-check-circle text-green-500');
        
        // Actualizar vista de plantilla
        renderEditSquadList();
        
        // Opcional: cerrar modal después de añadir
        // closeModal();
        
    } catch (error) {
        console.error('Error añadiendo jugador:', error);
        showMessageModal('Error', 'No se pudo añadir el jugador. Inténtalo de nuevo.', 'fa-times-circle text-red-500');
    }
};

async function getPlayersFromAPI(search = '', position = '') {
    // Por ahora simularemos con datos locales
    // En el futuro aquí harías fetch a tu API backend
    
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
        { id: "isak", name: "Alexander Isak", position: "DEL", team: "Real Sociedad", value: 55000000, points: 82 }
    ];
    
    // Cachear todos los jugadores
    if (cachedPlayers.length === 0) {
        cachedPlayers = samplePlayers;
    }
    
    let filtered = samplePlayers;
    
    // Filtrar por búsqueda de texto
    if (search) {
        filtered = filtered.filter(player => 
            player.name.toLowerCase().includes(search.toLowerCase())
        );
    }
    
    // Filtrar por posición
    if (position) {
        filtered = filtered.filter(player => player.position === position);
    }
    
    // Ordenar por valor (más caros primero)
    filtered.sort((a, b) => b.value - a.value);
    
    return filtered.slice(0, 20); // Limitar a 20 resultados
}

function renderPlayersResults(players) {
    const container = document.getElementById('players-results');
    
    if (players.length === 0) {
        container.innerHTML = `
            <div class="p-4 text-center text-gray-500">
                <i class="fas fa-search fa-2x mb-2"></i>
                <p>No se encontraron jugadores</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    players.forEach(player => {
        // Verificar si el jugador ya está en alguna plantilla
        const isOwned = allPlayers.some(p => p.name === player.name);
        
        html += `
            <div class="p-3 border-b last:border-b-0 hover:bg-gray-50 transition ${isOwned ? 'opacity-50' : ''}">
                <div class="flex justify-between items-center">
                    <div class="flex-1">
                        <div class="flex items-center mb-1">
                            <span class="font-medium text-gray-800">${player.name}</span>
                            <span class="ml-2 px-2 py-0.5 text-xs rounded-full ${getPositionBadgeClass(player.position)}">${player.position}</span>
                            ${isOwned ? '<span class="ml-2 px-2 py-0.5 text-xs bg-red-100 text-red-700 rounded-full">EN PLANTILLA</span>' : ''}
                        </div>
                        <div class="text-sm text-gray-600">
                            ${player.team} • ${formatCurrency(player.value)} • ${player.points} pts
                        </div>
                    </div>
                    <button 
                        onclick="addAPIPlayerToSquad('${player.id}', '${player.name}', '${player.position}', '${player.team}', ${player.value})"
                        class="ml-3 px-3 py-1 text-sm rounded-lg transition ${isOwned ? 'bg-gray-300 cursor-not-allowed' : 'bg-green-500 hover:bg-green-600 text-white'}"
                        ${isOwned ? 'disabled' : ''}
                    >
                        ${isOwned ? 'Ya en plantilla' : 'Añadir'}
                    </button>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function getPositionBadgeClass(position) {
    const classes = {
        'POR': 'bg-yellow-100 text-yellow-800',
        'DEF': 'bg-blue-100 text-blue-800', 
        'MED': 'bg-green-100 text-green-800',
        'DEL': 'bg-red-100 text-red-800'
    };
    return classes[position] || 'bg-gray-100 text-gray-800';
}

window.addAPIPlayerToSquad = async (playerId, name, position, team, value) => {
    const manager = managers.find(m => m.id === currentManagerId);
    
    try {
        await firestoreFunctions.addDoc(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.players), {
            apiId: playerId,
            name,
            position,
            team,
            value,
            ownerId: manager.id,
            ownerName: manager.name,
            addedAt: new Date()
        });
        
        showMessageModal('¡Jugador Añadido!', `${name} ha sido añadido a tu plantilla.`, 'fa-check-circle text-green-500');
        
        // Actualizar vista de plantilla
        renderEditSquadList();
        
    } catch (e) {
        console.error("Error al añadir jugador:", e);
        showMessageModal('Error', 'No se pudo añadir el jugador.', 'fa-times-circle text-red-500');
    }
};

window.addCustomPlayerToSquad = async () => {
    const nameInput = document.getElementById('new-player-name');
    const valueInput = document.getElementById('new-player-value');
    const positionSelect = document.getElementById('new-player-position');
    const teamInput = document.getElementById('new-player-team');

    const name = nameInput.value.trim();
    const value = Number(valueInput.value);
    const position = positionSelect.value;
    const team = teamInput.value.trim() || 'Personalizado';

    if (!name || !value || value <= 0) {
        showMessageModal('Datos incompletos', 'Por favor, introduce un nombre y un valor válido para el jugador.', 'fa-exclamation-circle text-yellow-500');
        return;
    }
    
    const manager = managers.find(m => m.id === currentManagerId);
    try {
        await firestoreFunctions.addDoc(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.players), {
            name,
            position,
            team,
            value,
            ownerId: manager.id,
            ownerName: manager.name,
            isCustom: true,
            addedAt: new Date()
        });
        
        // Limpiar formulario
        nameInput.value = '';
        valueInput.value = '';
        teamInput.value = '';
        nameInput.focus();
        
        showMessageModal('¡Jugador Creado!', `${name} ha sido añadido a tu plantilla.`, 'fa-check-circle text-green-500');
        
    } catch (e) {
        console.error("Error al añadir jugador personalizado:", e);
        showMessageModal('Error', 'No se pudo añadir el jugador.', 'fa-times-circle text-red-500');
    }
};

// Renderizar tabs vacíos por ahora
function renderAuctionsTab() {
    const container = document.getElementById('tab-content-auctions');
    container.innerHTML = `<div class="text-center p-8 bg-white rounded-xl shadow-md"><p class="text-gray-500">No hay subastas activas.</p></div>`;
}

function renderTradesTab() {
    const container = document.getElementById('tab-content-trades');
    container.innerHTML = `<div class="text-center p-8 bg-white rounded-xl shadow-md"><p class="text-gray-500">No hay intercambios pendientes.</p></div>`;
}

// Renderizar lista de edición de plantilla
async function renderEditSquadList() {
    const container = document.querySelector('#edit-squad-list-container .overflow-y-auto');
    const myPlayers = allPlayers.filter(p => p.ownerId === currentManagerId);
    
    if (myPlayers.length === 0) {
        container.innerHTML = '<p class="text-gray-500 p-4 text-center">No hay jugadores en tu plantilla.</p>';
        return;
    }

    let html = '';
    for (const player of myPlayers) {
        html += `
            <div class="flex justify-between items-center p-3 border-b last:border-b-0">
                <div>
                    <span class="font-medium">${player.name}</span>
                    <span class="text-sm text-gray-500 ml-2">${player.position}</span>
                    <span class="text-sm text-gray-500 ml-2">${formatCurrency(player.value)}</span>
                </div>
                <button onclick="removePlayerFromSquad('${player.id}')" class="text-red-500 hover:text-red-700 px-2 py-1">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

// Eliminar jugador de plantilla
window.removePlayerFromSquad = async (playerId) => {
    if (!confirm('¿Estás seguro de que quieres eliminar este jugador de tu plantilla?')) {
        return;
    }
    
    try {
        await firestoreFunctions.deleteDoc(firestoreFunctions.doc(window.firebaseDb, COLLECTIONS.players, playerId));
        // The onSnapshot listener will automatically re-render the list
    } catch (e) {
        console.error("Error al eliminar jugador:", e);
        showMessageModal('Error', 'No se pudo eliminar el jugador.', 'fa-times-circle text-red-500');
    }
};

// Funciones del mercado
window.openSellModal = (playerId) => {
    const player = allPlayers.find(p => p.id === playerId);
    if (!player) return;

    const content = `
        <div class="p-6">
            <h3 class="text-xl font-semibold mb-4">Vender Jugador</h3>
            <p class="mb-4">Vas a poner en venta a <span class="font-bold">${player.name}</span></p>
            <input type="number" id="sell-price" class="w-full p-2 border rounded-lg mb-4" placeholder="Precio de venta (€)" min="1000000">
            <div class="flex justify-end space-x-3">
                <button onclick="closeModal()" class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">Cancelar</button>
                <button onclick="sellPlayer('${playerId}')" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">Poner a la Venta</button>
            </div>
        </div>
    `;
    openModal(content);
    document.getElementById('sell-price').focus();
};

window.sellPlayer = async (playerId) => {
    const player = allPlayers.find(p => p.id === playerId);
    const price = Number(document.getElementById('sell-price').value);
    
    if (!price || price <= 0) {
        showMessageModal('Error', 'Introduce un precio válido.', 'fa-exclamation-circle text-yellow-500');
        return;
    }

    try {
        await firestoreFunctions.addDoc(firestoreFunctions.collection(window.firebaseDb, COLLECTIONS.market), {
            playerId: player.id,
            playerName: player.name,
            position: player.position,
            sellerId: player.ownerId,
            sellerName: player.ownerName,
            price: price,
            createdAt: new Date()
        });

        closeModal();
        showMessageModal('¡Éxito!', `${player.name} ha sido puesto a la venta por ${formatCurrency(price)}.`, 'fa-check-circle text-green-500');
    } catch (e) {
        console.error("Error al poner jugador a la venta:", e);
        showMessageModal('Error', 'No se pudo poner el jugador a la venta.', 'fa-times-circle text-red-500');
    }
};

window.openOfferModal = (marketItemId) => {
    const item = marketItems.find(m => m.id === marketItemId);
    if (!item) return;

    const content = `
        <div class="p-6">
            <h3 class="text-xl font-semibold mb-4">Hacer Oferta</h3>
            <p class="mb-4">Oferta para <span class="font-bold">${item.playerName}</span></p>
            <p class="text-sm text-gray-600 mb-4">Precio actual: ${formatCurrency(item.price)}</p>
            <input type="number" id="offer-amount" class="w-full p-2 border rounded-lg mb-4" placeholder="Tu oferta (€)" min="1000000">
            <div class="flex justify-end space-x-3">
                <button onclick="closeModal()" class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">Cancelar</button>
                <button onclick="makeOffer('${marketItemId}')" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Hacer Oferta</button>
            </div>
        </div>
    `;
    openModal(content);
    document.getElementById('offer-amount').focus();
};

window.makeOffer = async (marketItemId) => {
    const amount = Number(document.getElementById('offer-amount').value);
    const manager = managers.find(m => m.id === currentManagerId);
    
    if (!amount || amount <= 0) {
        showMessageModal('Error', 'Introduce una cantidad válida.', 'fa-exclamation-circle text-yellow-500');
        return;
    }

    try {
        await firestoreFunctions.addDoc(firestoreFunctions.collection(window.firebaseDb, `${COLLECTIONS.market}/${marketItemId}/offers`), {
            buyerId: manager.id,
            buyerName: manager.name,
            amount: amount,
            createdAt: new Date()
        });

        closeModal();
        showMessageModal('¡Oferta Enviada!', `Tu oferta de ${formatCurrency(amount)} ha sido enviada.`, 'fa-check-circle text-green-500');
    } catch (e) {
        console.error("Error al hacer oferta:", e);
        showMessageModal('Error', 'No se pudo enviar la oferta.', 'fa-times-circle text-red-500');
    }
};

window.acceptOffer = async (marketItemId, offerId) => {
    if (!confirm('¿Estás seguro de que quieres aceptar esta oferta?')) {
        return;
    }

    try {
        // Get offer details
        const offerDoc = await firestoreFunctions.getDoc(firestoreFunctions.doc(window.firebaseDb, `${COLLECTIONS.market}/${marketItemId}/offers`, offerId));
        const offer = offerDoc.data();
        
        // Get market item details
        const marketDoc = await firestoreFunctions.getDoc(firestoreFunctions.doc(window.firebaseDb, COLLECTIONS.market, marketItemId));
        const marketItem = marketDoc.data();
        
        // Update player ownership
        await firestoreFunctions.updateDoc(firestoreFunctions.doc(window.firebaseDb, COLLECTIONS.players, marketItem.playerId), {
            ownerId: offer.buyerId,
            ownerName: offer.buyerName
        });

        // Remove from market
        await firestoreFunctions.deleteDoc(firestoreFunctions.doc(window.firebaseDb, COLLECTIONS.market, marketItemId));
        
        showMessageModal('¡Venta Completada!', `${marketItem.playerName} ha sido vendido a ${offer.buyerName} por ${formatCurrency(offer.amount)}.`, 'fa-check-circle text-green-500');
    } catch (e) {
        console.error("Error al aceptar oferta:", e);
        showMessageModal('Error', 'No se pudo completar la venta.', 'fa-times-circle text-red-500');
    }
};

window.cancelSale = async (marketItemId) => {
    if (!confirm('¿Estás seguro de que quieres retirar este jugador del mercado?')) {
        return;
    }

    try {
        await firestoreFunctions.deleteDoc(firestoreFunctions.doc(window.firebaseDb, COLLECTIONS.market, marketItemId));
        showMessageModal('Venta Cancelada', 'El jugador ha sido retirado del mercado.', 'fa-info-circle text-blue-500');
    } catch (e) {
        console.error("Error al cancelar venta:", e);
        showMessageModal('Error', 'No se pudo retirar el jugador del mercado.', 'fa-times-circle text-red-500');
    }
};

// Funciones de utilidad
function formatCurrency(value) {
    return new Intl.NumberFormat('es-ES', { 
        style: 'currency', 
        currency: 'EUR', 
        minimumFractionDigits: 0 
    }).format(value);
}

function formatTimeLeft(ms) {
    if (ms <= 0) return "Finalizado";
    const totalSeconds = Math.floor(ms / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    return `${hours}h ${minutes}m restantes`;
}

// Funciones de modales
function openModal(content) {
    document.getElementById('modal-content').innerHTML = content;
    document.getElementById('modal-container').classList.remove('hidden');
}

window.closeModal = () => {
    document.getElementById('modal-container').classList.add('hidden');
    document.getElementById('modal-content').innerHTML = '';
};

function showMessageModal(title, message, iconClass = 'fa-info-circle text-blue-500', customButton = null) {
    const buttonHtml = customButton ? customButton : 
        `<button onclick="closeModal()" class="mt-6 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 w-full">Entendido</button>`;
    
    const content = `
        <div class="p-6 text-center">
            <i class="fas ${iconClass} fa-3x mb-4"></i>
            <h3 class="text-xl font-semibold mb-2">${title}</h3>
            <p class="text-gray-600">${message}</p>
            <div class="mt-6">
                ${buttonHtml}
            </div>
        </div>
    `;
    openModal(content);
}

// Modal de verificación de clave
window.openKeyPromptModal = (managerId) => {
    const manager = managers.find(m => m.id === managerId);
    const content = `
        <div class="p-6">
            <h3 class="text-xl font-semibold mb-4">Identificación de Manager</h3>
            <p class="mb-4 text-gray-600">Introduce la clave para <span class="font-bold">${manager.name}</span>.</p>
            <input type="password" id="manager-key-input" class="w-full p-2 border rounded-lg" placeholder="Clave secreta">
            <div class="mt-6 flex justify-end space-x-3">
                <button onclick="cancelLogin()" class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">Cancelar</button>
                <button onclick="verifyManagerKey('${managerId}')" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Entrar</button>
            </div>
        </div>
    `;
    openModal(content);
    document.getElementById('manager-key-input').focus();
};

window.cancelLogin = () => {
    document.getElementById('manager-select').value = '';
    closeModal();
};

window.verifyManagerKey = (managerId) => {
    const correctKey = managerKeys[managerId];
    const inputKey = document.getElementById('manager-key-input').value;
    
    if (inputKey === correctKey) {
        currentManagerId = managerId;
        document.getElementById('main-content').classList.remove('hidden');
        closeModal();
        showTab('squad');
    } else {
        showMessageModal(
            'Clave Incorrecta', 
            'La clave introducida no es correcta. Inténtalo de nuevo.', 
            'fa-times-circle text-red-500'
        );
        document.getElementById('manager-select').value = '';
    }
};

// =============================================================================
// SISTEMA DE CLASIFICACIONES Y JORNADAS
// =============================================================================

// Renderizar la pestaña de clasificaciones
function renderStandingsTab() {
    const container = document.getElementById('tab-content-standings');
    
    container.innerHTML = `
        <div class="bg-white rounded-xl shadow-md p-6">
            <div class="flex justify-between items-center mb-6">
                <h2 class="text-2xl font-bold text-gray-800">
                    <i class="fas fa-trophy text-yellow-500 mr-2"></i>
                    Clasificación por Jornadas
                </h2>
                <button onclick="openManageJornadaModal()" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition font-medium">
                    <i class="fas fa-plus mr-2"></i>Gestionar Jornada
                </button>
            </div>

            <!-- Selector de Jornada -->
            <div class="mb-6">
                <div class="flex items-center space-x-4">
                    <label for="jornada-selector" class="font-medium text-gray-700">Ver Jornada:</label>
                    <select id="jornada-selector" onchange="loadJornadaData()" class="px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                        <option value="">Seleccionar jornada...</option>
                    </select>
                    <div class="flex-1"></div>
                    <div class="text-sm text-gray-600">
                        <i class="fas fa-calendar mr-1"></i>
                        Temporada 2025/2026
                    </div>
                </div>
            </div>

            <!-- Clasificación de la Jornada -->
            <div id="jornada-standings" class="mb-8">
                <div class="text-center py-8 text-gray-500">
                    <i class="fas fa-list-ol fa-3x mb-4 opacity-50"></i>
                    <p>Selecciona una jornada para ver la clasificación</p>
                </div>
            </div>

            <!-- Sistema de Penalizaciones -->
            <div class="bg-red-50 border border-red-200 rounded-lg p-6">
                <h3 class="text-lg font-bold text-red-800 mb-4">
                    <i class="fas fa-euro-sign mr-2"></i>
                    Sistema de Penalizaciones
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div class="bg-red-100 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                            <span class="font-medium text-red-800">Último Puesto</span>
                            <span class="bg-red-600 text-white px-3 py-1 rounded-full font-bold">3€</span>
                        </div>
                        <p class="text-sm text-red-700 mt-1">Por jornada</p>
                    </div>
                    <div class="bg-orange-100 rounded-lg p-4">
                        <div class="flex items-center justify-between">
                            <span class="font-medium text-orange-800">Penúltimo Puesto</span>
                            <span class="bg-orange-600 text-white px-3 py-1 rounded-full font-bold">2€</span>
                        </div>
                        <p class="text-sm text-orange-700 mt-1">Por jornada</p>
                    </div>
                </div>
                
                <!-- Control de Pagos -->
                <div id="payment-control" class="mt-4">
                    <!-- Se llenará dinámicamente -->
                </div>
            </div>

            <!-- Resumen de la Temporada -->
            <div class="mt-8 bg-gray-50 rounded-lg p-6">
                <h3 class="text-lg font-bold text-gray-800 mb-4">
                    <i class="fas fa-chart-line mr-2"></i>
                    Resumen de la Temporada
                </h3>
                <div id="season-summary" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <!-- Se llenará dinámicamente -->
                </div>
            </div>
        </div>
    `;

    // Cargar jornadas disponibles
    loadAvailableJornadas();
}

// Cargar jornadas disponibles en el selector
async function loadAvailableJornadas() {
    try {
        const jornadasSnapshot = await firestoreFunctions.getDocs(
            firestoreFunctions.collection(window.firebaseDb, 'jornadas')
        );
        
        const selector = document.getElementById('jornada-selector');
        selector.innerHTML = '<option value="">Seleccionar jornada...</option>';
        
        const jornadas = [];
        jornadasSnapshot.forEach(doc => {
            const data = doc.data();
            jornadas.push({ id: doc.id, ...data });
        });
        
        // Ordenar por número de jornada
        jornadas.sort((a, b) => a.numero - b.numero);
        
        jornadas.forEach(jornada => {
            const option = document.createElement('option');
            option.value = jornada.id;
            option.textContent = `Jornada ${jornada.numero}${jornada.completada ? ' ✓' : ' (En curso)'}`;
            selector.appendChild(option);
        });

        // Si hay jornadas, cargar la más reciente
        if (jornadas.length > 0) {
            const latestJornada = jornadas[jornadas.length - 1];
            selector.value = latestJornada.id;
            loadJornadaData();
        }
        
    } catch (error) {
        console.error('Error cargando jornadas:', error);
    }
}

// Cargar datos de una jornada específica
window.loadJornadaData = async () => {
    const jornadaId = document.getElementById('jornada-selector').value;
    if (!jornadaId) return;

    try {
        // Obtener datos de la jornada
        const jornadaDoc = await firestoreFunctions.getDoc(
            firestoreFunctions.doc(window.firebaseDb, 'jornadas', jornadaId)
        );
        
        if (!jornadaDoc.exists()) return;
        
        const jornadaData = jornadaDoc.data();
        
        // Renderizar clasificación
        renderJornadaStandings(jornadaData);
        
        // Renderizar control de pagos
        renderPaymentControl(jornadaId, jornadaData);
        
    } catch (error) {
        console.error('Error cargando datos de jornada:', error);
    }
};

// Renderizar clasificación de la jornada
function renderJornadaStandings(jornadaData) {
    const container = document.getElementById('jornada-standings');
    
    if (!jornadaData.clasificacion || jornadaData.clasificacion.length === 0) {
        container.innerHTML = `
            <div class="text-center py-8 text-gray-500">
                <i class="fas fa-hourglass-half fa-2x mb-4 opacity-50"></i>
                <p>No hay datos de clasificación para esta jornada</p>
            </div>
        `;
        return;
    }

    const standings = jornadaData.clasificacion.sort((a, b) => a.posicion - b.posicion);
    
    const standingsHTML = standings.map((team, index) => {
        const isLast = index === standings.length - 1;
        const isPenultimate = index === standings.length - 2;
        
        let positionClass = '';
        let penaltyBadge = '';
        
        if (isLast) {
            positionClass = 'bg-red-100 border-red-300';
            penaltyBadge = '<span class="bg-red-600 text-white px-2 py-1 rounded-full text-xs font-bold ml-2">-3€</span>';
        } else if (isPenultimate) {
            positionClass = 'bg-orange-100 border-orange-300';
            penaltyBadge = '<span class="bg-orange-600 text-white px-2 py-1 rounded-full text-xs font-bold ml-2">-2€</span>';
        } else if (index === 0) {
            positionClass = 'bg-yellow-100 border-yellow-300';
        } else if (index < 3) {
            positionClass = 'bg-green-100 border-green-300';
        }

        return `
            <div class="flex items-center p-4 border rounded-lg ${positionClass}">
                <div class="flex items-center flex-1">
                    <span class="text-2xl font-bold text-gray-700 w-8">${team.posicion}</span>
                    <div class="ml-4">
                        <h4 class="font-semibold text-gray-800">${team.manager}</h4>
                        <p class="text-sm text-gray-600">${team.puntos} puntos</p>
                    </div>
                </div>
                <div class="text-right">
                    <span class="text-lg font-bold text-gray-800">${team.puntos}</span>
                    ${penaltyBadge}
                </div>
            </div>
        `;
    }).join('');

    container.innerHTML = `
        <div class="space-y-3">
            <h3 class="text-lg font-bold text-gray-800 mb-4">
                Clasificación - Jornada ${jornadaData.numero}
            </h3>
            ${standingsHTML}
        </div>
    `;
}

// Renderizar control de pagos
function renderPaymentControl(jornadaId, jornadaData) {
    const container = document.getElementById('payment-control');
    
    if (!jornadaData.clasificacion || jornadaData.clasificacion.length === 0) {
        container.innerHTML = '';
        return;
    }

    const standings = jornadaData.clasificacion.sort((a, b) => a.posicion - b.posicion);
    const lastTeam = standings[standings.length - 1];
    const penultimateTeam = standings[standings.length - 2];
    
    const paymentData = jornadaData.pagos || {};

    container.innerHTML = `
        <h4 class="font-semibold text-gray-800 mb-3">Control de Pagos - Jornada ${jornadaData.numero}</h4>
        <div class="space-y-3">
            <!-- Último puesto -->
            <div class="flex items-center justify-between p-3 bg-red-50 rounded-lg border">
                <div>
                    <span class="font-medium text-red-800">${lastTeam.manager}</span>
                    <span class="text-sm text-red-600 ml-2">(Último - 3€)</span>
                </div>
                <div class="flex items-center space-x-3">
                    <label class="flex items-center">
                        <input type="checkbox" 
                               ${paymentData[lastTeam.manager]?.pagado ? 'checked' : ''} 
                               onchange="updatePaymentStatus('${jornadaId}', '${lastTeam.manager}', 3, this.checked)"
                               class="mr-2">
                        <span class="text-sm">Pagado</span>
                    </label>
                    <input type="number" 
                           value="${paymentData[lastTeam.manager]?.cantidad || 3}" 
                           onchange="updatePaymentAmount('${jornadaId}', '${lastTeam.manager}', this.value)"
                           class="w-16 px-2 py-1 border rounded text-center text-sm"
                           step="0.5" min="0">
                    <span class="text-sm">€</span>
                </div>
            </div>
            
            <!-- Penúltimo puesto -->
            <div class="flex items-center justify-between p-3 bg-orange-50 rounded-lg border">
                <div>
                    <span class="font-medium text-orange-800">${penultimateTeam.manager}</span>
                    <span class="text-sm text-orange-600 ml-2">(Penúltimo - 2€)</span>
                </div>
                <div class="flex items-center space-x-3">
                    <label class="flex items-center">
                        <input type="checkbox" 
                               ${paymentData[penultimateTeam.manager]?.pagado ? 'checked' : ''} 
                               onchange="updatePaymentStatus('${jornadaId}', '${penultimateTeam.manager}', 2, this.checked)"
                               class="mr-2">
                        <span class="text-sm">Pagado</span>
                    </label>
                    <input type="number" 
                           value="${paymentData[penultimateTeam.manager]?.cantidad || 2}" 
                           onchange="updatePaymentAmount('${jornadaId}', '${penultimateTeam.manager}', this.value)"
                           class="w-16 px-2 py-1 border rounded text-center text-sm"
                           step="0.5" min="0">
                    <span class="text-sm">€</span>
                </div>
            </div>
        </div>
        
        <div class="mt-4 p-3 bg-blue-50 rounded-lg">
            <div class="flex justify-between items-center">
                <span class="font-medium text-blue-800">Total recaudado:</span>
                <span class="font-bold text-blue-800">${calculateTotalCollected(paymentData)}€</span>
            </div>
        </div>
    `;
}

// Actualizar estado de pago
window.updatePaymentStatus = async (jornadaId, manager, defaultAmount, paid) => {
    try {
        const jornadaRef = firestoreFunctions.doc(window.firebaseDb, 'jornadas', jornadaId);
        
        await firestoreFunctions.updateDoc(jornadaRef, {
            [`pagos.${manager}.pagado`]: paid,
            [`pagos.${manager}.cantidad`]: defaultAmount,
            [`pagos.${manager}.fechaPago`]: paid ? new Date() : null
        });
        
        console.log(`Pago ${paid ? 'marcado' : 'desmarcado'} para ${manager}`);
        
    } catch (error) {
        console.error('Error actualizando estado de pago:', error);
    }
};

// Actualizar cantidad de pago
window.updatePaymentAmount = async (jornadaId, manager, amount) => {
    try {
        const jornadaRef = firestoreFunctions.doc(window.firebaseDb, 'jornadas', jornadaId);
        
        await firestoreFunctions.updateDoc(jornadaRef, {
            [`pagos.${manager}.cantidad`]: parseFloat(amount)
        });
        
        // Actualizar el total mostrado
        loadJornadaData();
        
    } catch (error) {
        console.error('Error actualizando cantidad de pago:', error);
    }
};

// Calcular total recaudado
function calculateTotalCollected(paymentData) {
    let total = 0;
    Object.values(paymentData).forEach(payment => {
        if (payment.pagado) {
            total += payment.cantidad || 0;
        }
    });
    return total.toFixed(2);
}

// Modal para gestionar jornadas
window.openManageJornadaModal = () => {
    const content = `
        <div class="p-6">
            <h3 class="text-xl font-semibold mb-4">
                <i class="fas fa-calendar-plus mr-2"></i>
                Gestionar Jornada
            </h3>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        Número de Jornada
                    </label>
                    <input type="number" id="jornada-numero" min="1" max="38" 
                           class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500">
                </div>
                
                <div class="space-y-3" id="managers-positions">
                    <label class="block text-sm font-medium text-gray-700">
                        Clasificación de Managers
                    </label>
                    <!-- Se llenará dinámicamente con los managers -->
                </div>
            </div>
            
            <div class="mt-6 flex justify-end space-x-3">
                <button onclick="closeModal()" class="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300">
                    Cancelar
                </button>
                <button onclick="saveJornadaData()" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Guardar Jornada
                </button>
            </div>
        </div>
    `;
    
    openModal(content);
    loadManagersForJornada();
};

// Cargar managers para la jornada
async function loadManagersForJornada() {
    const container = document.getElementById('managers-positions');
    
    const managersHTML = managers.map((manager, index) => `
        <div class="flex items-center space-x-3 p-3 border rounded-lg">
            <span class="w-8 text-center font-medium">${index + 1}°</span>
            <span class="flex-1 font-medium">${manager.name}</span>
            <input type="number" 
                   id="points-${manager.id}" 
                   placeholder="Puntos" 
                   class="w-20 px-2 py-1 border rounded text-center"
                   step="0.1">
        </div>
    `).join('');
    
    container.innerHTML = managersHTML;
}

// Guardar datos de jornada
window.saveJornadaData = async () => {
    const jornadaNumero = document.getElementById('jornada-numero').value;
    
    if (!jornadaNumero || jornadaNumero < 1 || jornadaNumero > 38) {
        showMessageModal('Error', 'Por favor introduce un número de jornada válido (1-38).', 'fa-exclamation-triangle text-yellow-500');
        return;
    }
    
    // Recopilar datos de clasificación
    const clasificacion = [];
    let hasValidData = false;
    
    managers.forEach((manager, index) => {
        const pointsInput = document.getElementById(`points-${manager.id}`);
        const points = parseFloat(pointsInput.value) || 0;
        
        if (points > 0) hasValidData = true;
        
        clasificacion.push({
            manager: manager.name,
            managerId: manager.id,
            puntos: points,
            posicion: index + 1 // Se reordenará después
        });
    });
    
    if (!hasValidData) {
        showMessageModal('Error', 'Por favor introduce al menos algunos puntos para los managers.', 'fa-exclamation-triangle text-yellow-500');
        return;
    }
    
    // Ordenar por puntos (mayor a menor)
    clasificacion.sort((a, b) => b.puntos - a.puntos);
    
    // Asignar posiciones correctas
    clasificacion.forEach((team, index) => {
        team.posicion = index + 1;
    });
    
    try {
        // Guardar en Firebase
        await firestoreFunctions.setDoc(
            firestoreFunctions.doc(window.firebaseDb, 'jornadas', `jornada-${jornadaNumero}`),
            {
                numero: parseInt(jornadaNumero),
                clasificacion: clasificacion,
                fechaCreacion: new Date(),
                completada: true,
                pagos: {} // Se inicializa vacío
            }
        );
        
        showMessageModal('¡Éxito!', `Jornada ${jornadaNumero} guardada correctamente.`, 'fa-check-circle text-green-500');
        closeModal();
        
        // Recargar datos
        loadAvailableJornadas();
        
    } catch (error) {
        console.error('Error guardando jornada:', error);
        showMessageModal('Error', 'No se pudo guardar la jornada. Inténtalo de nuevo.', 'fa-times-circle text-red-500');
    }
};

// Placeholder para funciones que implementaremos
window.openTradeModal = () => {
    showMessageModal('Próximamente', 'Los intercambios estarán disponibles pronto.', 'fa-clock text-yellow-500');
};

window.openAuctionModal = () => {
    showMessageModal('Próximamente', 'Las subastas estarán disponibles pronto.', 'fa-clock text-yellow-500');
};

// Inicializar la aplicación cuando la página esté lista
document.addEventListener('DOMContentLoaded', initializeApp);
