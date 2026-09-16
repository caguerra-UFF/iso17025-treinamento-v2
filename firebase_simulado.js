// -*- coding: utf-8 -*-
/**
 * firebase_simulado.js
 * Módulo de integração Firebase (Auth + Firestore) para o Simulado ISO/IEC 17025:2017.
 * Conectado ao projeto oficial 'duapp-ea6a8' (Eletronuclear / LMA).
 * 
 * Funcionalidades:
 * 1. Login e Logout via Google Auth (Firebase Auth).
 * 2. Auto-cadastro e perfil do participante (Matrícula, Setor, Função, Perfil) em 'iso17025_usuarios'.
 * 3. Envio e registro de provas em 'iso17025_submissoes' com status de habilitação (nota >= 70%).
 * 4. Painel do Gestor: listagem de alunos, filtros e exportação de relatórios (CSV/Excel).
 * 5. Fallback local / Modo Demonstração transparente quando offline ou sem conexão.
 */

const FIREBASE_CONFIG = {
    apiKey: "AIzaSyBt77mpmpK308DBw4SsQ4uf20fM2wycD-o",
    authDomain: "duapp-ea6a8.firebaseapp.com",
    projectId: "duapp-ea6a8",
    storageBucket: "duapp-ea6a8.firebasestorage.app",
    messagingSenderId: "899938665434",
    appId: "1:899938665434:web:65e6c61d81ffe37ae7b6e3"
};

// Lista de e-mails autorizados para acesso ao Painel do Gestor / Instrutor
const INSTRUCTOR_WHITELIST = [
    "caguerra.uff@gmail.com",
    "caguerra@eletronuclear.gov.br",
    "instrutor.iso17025@gmail.com",
    "qualidade.lma@eletronuclear.gov.br",
    "admin@lma.com"
];

class FirebaseSimuladoService {
    constructor() {
        this.app = null;
        this.auth = null;
        this.db = null;
        this.currentUser = null;
        this.currentProfile = null;
        this.isInitialized = false;
        this.authListeners = [];
    }

    /**
     * Inicializa o Firebase Web SDK (compat v9/v10 via CDN)
     */
    init() {
        try {
            if (window.firebase && !firebase.apps.length) {
                this.app = firebase.initializeApp(FIREBASE_CONFIG);
                this.auth = firebase.auth();
                this.db = firebase.firestore();
                this.isInitialized = true;

                // Monitorar estado de autenticação
                this.auth.onAuthStateChanged(async (user) => {
                    this.currentUser = user;
                    if (user) {
                        this.currentProfile = await this.obterOuCriarPerfil(user);
                    } else {
                        this.currentProfile = null;
                    }
                    this._notifyListeners();
                });
                console.log("[FirebaseSimulado] Conectado com sucesso ao projeto:", FIREBASE_CONFIG.projectId);
            } else if (window.firebase && firebase.apps.length) {
                this.app = firebase.app();
                this.auth = firebase.auth();
                this.db = firebase.firestore();
                this.isInitialized = true;
            } else {
                console.warn("[FirebaseSimulado] SDK Firebase não detectado. Ativando modo local resiliente.");
            }
        } catch (e) {
            console.error("[FirebaseSimulado] Erro ao inicializar Firebase:", e);
        }
    }

    onAuthChange(callback) {
        this.authListeners.push(callback);
        // Disparar imediatamente com o estado atual se já disponível
        if (this.isInitialized && this.currentUser !== undefined) {
            callback(this.currentUser, this.currentProfile);
        }
    }

    _notifyListeners() {
        for (const cb of this.authListeners) {
            try {
                cb(this.currentUser, this.currentProfile);
            } catch (err) {
                console.error("[FirebaseSimulado] Erro em listener de autenticação:", err);
            }
        }
    }

    /**
     * Login em 1 clique com Conta Google
     */
    async loginGoogle() {
        if (!this.auth) {
            return this._loginMockDemo();
        }
        try {
            const provider = new firebase.auth.GoogleAuthProvider();
            provider.setCustomParameters({ prompt: 'select_account' });
            const result = await this.auth.signInWithPopup(provider);
            this.currentUser = result.user;
            this.currentProfile = await this.obterOuCriarPerfil(result.user);
            this._notifyListeners();
            return { success: true, user: result.user, profile: this.currentProfile };
        } catch (error) {
            console.error("[FirebaseSimulado] Erro no login Google:", error);
            // Se o popup for bloqueado ou offline, perguntar se deseja usar modo teste
            if (error.code === 'auth/popup-blocked' || error.code === 'auth/network-request-failed') {
                alert("Aviso: O popup de login foi bloqueado pelo navegador ou não há conexão. Verifique as permissões de popups.");
            }
            throw error;
        }
    }

    /**
     * Logout
     */
    async logout() {
        if (this.auth) {
            await this.auth.signOut();
        }
        this.currentUser = null;
        this.currentProfile = null;
        localStorage.removeItem('iso17025_demo_user');
        this._notifyListeners();
    }

    /**
     * Busca ou cria o documento de perfil em 'iso17025_usuarios'
     */
    async obterOuCriarPerfil(user) {
        if (!this.db || !user) return null;
        try {
            const docRef = this.db.collection('iso17025_usuarios').doc(user.uid);
            const docSnap = await docRef.get();

            if (docSnap.exists) {
                return docSnap.data();
            } else {
                // Perfil inicial pendente de complementação
                const novoPerfil = {
                    uid: user.uid,
                    email: user.email || '',
                    nome: user.displayName || 'Participante',
                    foto: user.photoURL || '',
                    matricula: '',
                    setor: '',
                    funcao: '',
                    perfilMetrologico: 'geral',
                    isHabilitado: false,
                    melhorNota: 0,
                    totalTentativas: 0,
                    dataCriacao: new Date().toISOString(),
                    ultimaAtividade: new Date().toISOString()
                };
                await docRef.set(novoPerfil);
                return novoPerfil;
            }
        } catch (e) {
            console.warn("[FirebaseSimulado] Erro ao ler perfil do Firestore, usando dados locais:", e);
            return {
                uid: user.uid,
                email: user.email || '',
                nome: user.displayName || 'Participante',
                foto: user.photoURL || '',
                matricula: '',
                setor: '',
                funcao: '',
                isHabilitado: false,
                melhorNota: 0,
                totalTentativas: 0
            };
        }
    }

    /**
     * Salva ou atualiza os dados do cadastro simples
     */
    async salvarCadastro(dados) {
        if (!this.currentUser) throw new Error("Usuário não autenticado");

        const uid = this.currentUser.uid;
        const perfilAtualizado = {
            ...this.currentProfile,
            nome: dados.nome || this.currentUser.displayName || 'Participante',
            matricula: dados.matricula ? dados.matricula.trim() : '',
            setor: dados.setor ? dados.setor.trim() : '',
            funcao: dados.funcao ? dados.funcao.trim() : '',
            perfilMetrologico: dados.perfilMetrologico || 'geral',
            cadastroCompleto: true,
            ultimaAtividade: new Date().toISOString()
        };

        if (this.db) {
            try {
                await this.db.collection('iso17025_usuarios').doc(uid).set(perfilAtualizado, { merge: true });
            } catch (e) {
                console.error("[FirebaseSimulado] Erro ao salvar cadastro no Firestore:", e);
            }
        }

        this.currentProfile = perfilAtualizado;
        this._notifyListeners();
        return perfilAtualizado;
    }

    /**
     * Registra o resultado da avaliação e atualiza status de habilitação
     */
    async enviarSubmissaoProva(payload) {
        if (!this.currentUser) {
            console.warn("[FirebaseSimulado] Prova finalizada sem usuário logado. Salva apenas localmente.");
            return null;
        }

        const uid = this.currentUser.uid;
        const nota = payload.percent || 0;
        const habilitado = nota >= 70; // Critério oficial de corte: 70%
        const submissaoId = `SUB_${Date.now()}_${Math.random().toString(36).substring(2, 7).toUpperCase()}`;

        const docSubmissao = {
            submissaoId: submissaoId,
            userId: uid,
            userEmail: this.currentUser.email || '',
            userName: (this.currentProfile && this.currentProfile.nome) || this.currentUser.displayName || 'Participante',
            matricula: (this.currentProfile && this.currentProfile.matricula) || '',
            setor: (this.currentProfile && this.currentProfile.setor) || '',
            funcao: (this.currentProfile && this.currentProfile.funcao) || '',
            perfilMetrologico: payload.profileFilter || 'geral',
            dataEnvio: new Date().toISOString(),
            modo: payload.examMode || 'oficial',
            totalQuestoes: payload.totalQuestions || 0,
            acertos: payload.correctCount || 0,
            erros: payload.wrongCount || 0,
            notaPercentual: nota,
            isHabilitado: habilitado,
            tempoGastoSegundos: payload.timeSpentSeconds || 0,
            codigoAutenticidade: this._gerarCodigoAutenticidade(uid, nota),
            radarPorPerfil: payload.radarProfile || {},
            radarPorSecao: payload.radarSection || {},
            respostas: payload.answersSummary || []
        };

        if (this.db) {
            try {
                // 1. Grava o laudo/submissão na coleção de auditoria
                await this.db.collection('iso17025_submissoes').doc(submissaoId).set(docSubmissao);

                // 2. Atualiza o documento de perfil do usuário com melhor nota e status
                const melhorNotaAtual = (this.currentProfile && this.currentProfile.melhorNota) || 0;
                const totalTentativas = ((this.currentProfile && this.currentProfile.totalTentativas) || 0) + 1;
                const statusHabilitado = (this.currentProfile && this.currentProfile.isHabilitado) || habilitado;

                const userUpdate = {
                    melhorNota: Math.max(melhorNotaAtual, nota),
                    isHabilitado: statusHabilitado,
                    totalTentativas: totalTentativas,
                    ultimaNota: nota,
                    ultimaSubmissaoId: submissaoId,
                    ultimaAtividade: new Date().toISOString()
                };

                if (habilitado && (!this.currentProfile || !this.currentProfile.dataHabilitacao)) {
                    userUpdate.dataHabilitacao = new Date().toISOString();
                }

                await this.db.collection('iso17025_usuarios').doc(uid).set(userUpdate, { merge: true });
                this.currentProfile = { ...this.currentProfile, ...userUpdate };
                this._notifyListeners();
            } catch (e) {
                console.error("[FirebaseSimulado] Erro ao gravar submissão no Firestore:", e);
            }
        }

        return docSubmissao;
    }

    /**
     * Consulta consolidada para o Painel do Gestor / Instrutor
     */
    async carregarPainelGestor() {
        if (!this.db) {
            return this._getMockDashboardData();
        }
        try {
            const snap = await this.db.collection('iso17025_usuarios').get();
            const usuarios = [];
            snap.forEach(doc => {
                usuarios.push({ id: doc.id, ...doc.data() });
            });

            // Ordenar por status habilitado e nota decrescente
            usuarios.sort((a, b) => {
                if (b.isHabilitado !== a.isHabilitado) {
                    return b.isHabilitado ? 1 : -1;
                }
                return (b.melhorNota || 0) - (a.melhorNota || 0);
            });

            return usuarios;
        } catch (e) {
            console.error("[FirebaseSimulado] Erro ao carregar dados do painel do gestor:", e);
            return this._getMockDashboardData();
        }
    }

    /**
     * Verifica se o e-mail logado tem privilégios de Instrutor / Gestor
     */
    isInstrutor() {
        if (!this.currentUser || !this.currentUser.email) return false;
        const email = this.currentUser.email.toLowerCase().trim();
        return INSTRUCTOR_WHITELIST.includes(email) || email.endsWith("@eletronuclear.gov.br");
    }

    _gerarCodigoAutenticidade(uid, nota) {
        const str = `${uid}-${nota}-${Date.now()}`;
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash |= 0;
        }
        const hex = Math.abs(hash).toString(16).toUpperCase().padStart(8, '0');
        return `ISO17025-${hex.substring(0, 4)}-${hex.substring(4, 8)}`;
    }

    // Modo Demonstração / Teste Local (quando sem internet)
    _loginMockDemo() {
        const demoUser = {
            uid: "DEMO_USER_001",
            email: "participante.teste@eletronuclear.gov.br",
            displayName: "Analista de Treinamento (Modo Demonstração)",
            photoURL: "https://ui-avatars.com/api/?name=Analista+Treinamento&background=0f4c81&color=fff"
        };
        this.currentUser = demoUser;
        this.currentProfile = {
            uid: demoUser.uid,
            email: demoUser.email,
            nome: demoUser.displayName,
            matricula: "MAT-94821",
            setor: "LMA - Laboratório de Monitoramento Ambiental",
            funcao: "Analista Metrológico Sênior",
            perfilMetrologico: "tecnico",
            isHabilitado: false,
            melhorNota: 0,
            totalTentativas: 0,
            cadastroCompleto: true
        };
        localStorage.setItem('iso17025_demo_user', JSON.stringify(demoUser));
        this._notifyListeners();
        return { success: true, user: demoUser, profile: this.currentProfile };
    }

    _getMockDashboardData() {
        return [
            {
                uid: "USR_101",
                nome: "Carlos Eduardo Guerra",
                email: "caguerra.uff@gmail.com",
                matricula: "EN-10492",
                setor: "LMA - Química Analítica",
                funcao: "Responsável Técnico Metrológico",
                isHabilitado: true,
                melhorNota: 94,
                totalTentativas: 2,
                dataHabilitacao: "2026-09-14T18:30:00Z"
            },
            {
                uid: "USR_102",
                nome: "Mariana Silveira Ramos",
                email: "mariana.ramos@eletronuclear.gov.br",
                matricula: "EN-20381",
                setor: "Radiometria Ambiental",
                funcao: "Técnica em Radioproteção",
                isHabilitado: true,
                melhorNota: 88,
                totalTentativas: 1,
                dataHabilitacao: "2026-09-15T11:20:00Z"
            },
            {
                uid: "USR_103",
                nome: "Roberto Mendes Ferreira",
                email: "roberto.mendes@eletronuclear.gov.br",
                matricula: "EN-09823",
                setor: "Garantia da Qualidade",
                funcao: "Auditor Interno da Qualidade",
                isHabilitado: false,
                melhorNota: 64,
                totalTentativas: 1
            }
        ];
    }
}

// Instância global única
window.firebaseSimulado = new FirebaseSimuladoService();
document.addEventListener("DOMContentLoaded", () => {
    window.firebaseSimulado.init();
});
