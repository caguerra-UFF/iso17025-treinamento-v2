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
            // Se houver sessão manual salva localmente e nenhum usuário Firebase ativo, restaura
            const savedManual = localStorage.getItem('iso17025_manual_user');
            if (savedManual && !this.currentUser) {
                try {
                    const parsed = JSON.parse(savedManual);
                    this.currentUser = parsed.user;
                    this.currentProfile = parsed.profile;
                } catch (e) {}
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
     * Login em 1 clique com Conta Google (com detecção de protocolo e fallback automático)
     */
    async loginGoogle() {
        // 1. Verificação de protocolo local file://
        if (window.location.protocol === 'file:') {
            const prosseguir = confirm(
                "ℹ️ AVISO SOBRE AMBIENTE LOCAL (protocolo file://):\n\n" +
                "O Google bloqueia a abertura de popups de login seguro quando arquivos HTML são abertos diretamente pelo disco local (file://).\n\n" +
                "• Para usar o login com Conta Google real: abra o simulado via servidor web local (ex: rodando 'python -m http.server 8000' ou 'npx serve' no terminal e acessando http://localhost:8000/simulado.html).\n\n" +
                "Deseja se identificar agora informando seu Nome e Matrícula diretamente para realizar sua prova e emitir o Laudo Oficial?"
            );
            if (prosseguir) {
                return this.loginManualPrompt();
            }
            return null;
        }

        if (!this.auth) {
            alert("Aviso: O SDK do Firebase não pôde ser carregado (possível bloqueio de rede ou offline). Ativando identificação direta.");
            return this.loginManualPrompt();
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
            
            if (error.code === 'auth/operation-not-supported-in-this-environment') {
                const prosseguir = confirm(
                    "O ambiente atual não suporta popup do Google (ambiente restrito ou protocolo local).\n\n" +
                    "Deseja se identificar informando seu Nome e Matrícula diretamente?"
                );
                if (prosseguir) return this.loginManualPrompt();
                return null;
            }
            if (error.code === 'auth/unauthorized-domain') {
                const prosseguir = confirm(
                    "Domínio Não Autorizado no Firebase:\n\n" +
                    "O domínio '" + window.location.hostname + "' precisa ser incluído em 'Authorized Domains' no Firebase Console do projeto 'duapp-ea6a8'.\n\n" +
                    "Deseja prosseguir informando seu Nome e Matrícula diretamente?"
                );
                if (prosseguir) return this.loginManualPrompt();
                return null;
            }
            if (error.code === 'auth/popup-blocked') {
                const prosseguir = confirm(
                    "O navegador bloqueou o popup do Google.\n\n" +
                    "Deseja se identificar informando seu Nome e Matrícula diretamente?"
                );
                if (prosseguir) return this.loginManualPrompt();
                return null;
            }
            if (error.code === 'auth/popup-closed-by-user') {
                console.log("[FirebaseSimulado] Popup fechado pelo usuário.");
                return null;
            }
            
            const fallback = confirm(
                "Falha ao autenticar com o Google (" + (error.message || error.code) + ").\n\n" +
                "Deseja prosseguir informando seu Nome e Matrícula diretamente?"
            );
            if (fallback) return this.loginManualPrompt();
            throw error;
        }
    }

    /**
     * Identificação Manual Direta (Nome, Matrícula e Setor)
     * Permite identificação oficial mesmo offline ou sob file://
     */
    loginManualPrompt(nomePadrao, emailPadrao) {
        let nome = prompt("Informe seu Nome Completo para registro oficial na ISO/IEC 17025:", nomePadrao || "");
        if (!nome || !nome.trim()) return null;
        nome = nome.trim();

        let email = prompt("Informe seu E-mail Institucional:", emailPadrao || "participante@eletronuclear.gov.br");
        if (!email || !email.trim()) return null;
        email = email.trim();

        let matricula = prompt("Informe sua Matrícula / Registro Funcional (ex: EN-10492):", "");
        matricula = matricula ? matricula.trim() : "";

        let setor = prompt("Informe seu Setor / Laboratório (ex: LMA, Química Analítica, SGQ):", "LMA - Laboratório de Monitoramento Ambiental");
        setor = setor ? setor.trim() : "LMA";

        const uid = "USR_" + Math.abs(this._hashString(email)).toString(36).toUpperCase();
        const manualUser = {
            uid: uid,
            email: email,
            displayName: nome,
            photoURL: "https://ui-avatars.com/api/?name=" + encodeURIComponent(nome) + "&background=0f4c81&color=fff"
        };
        this.currentUser = manualUser;
        this.currentProfile = {
            uid: uid,
            email: email,
            nome: nome,
            matricula: matricula,
            setor: setor,
            funcao: "Analista / Técnico",
            perfilMetrologico: "geral",
            isHabilitado: false,
            melhorNota: 0,
            totalTentativas: 0,
            cadastroCompleto: !!matricula,
            dataCriacao: new Date().toISOString(),
            ultimaAtividade: new Date().toISOString()
        };

        if (this.db) {
            try {
                this.db.collection('iso17025_usuarios').doc(uid).set(this.currentProfile, { merge: true }).catch(err => {
                    console.warn("[FirebaseSimulado] Aviso ao sincronizar com Firestore:", err);
                });
            } catch (e) {}
        }

        localStorage.setItem('iso17025_manual_user', JSON.stringify({ user: manualUser, profile: this.currentProfile }));
        this._notifyListeners();
        return { success: true, user: manualUser, profile: this.currentProfile };
    }

    _hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash |= 0;
        }
        return hash;
    }

    /**
     * Logout
     */
    async logout() {
        if (this.auth) {
            try { await this.auth.signOut(); } catch (e) {}
        }
        this.currentUser = null;
        this.currentProfile = null;
        localStorage.removeItem('iso17025_demo_user');
        localStorage.removeItem('iso17025_manual_user');
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
