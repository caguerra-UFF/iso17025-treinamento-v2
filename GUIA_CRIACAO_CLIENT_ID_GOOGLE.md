# Guia: Criar o Client ID OAuth (Login Google) para o Simulado ISO/IEC 17025

> **Objetivo:** ativar a identificação do participante por conta Google no `simulado.html`,
> vinculando o resultado ao e-mail de quem fez a avaliação (Etapa 1 do plano de autenticação).
>
> **Tempo estimado:** ~10 minutos · **Custo:** R$ 0 · **Nível:** sem programação
>
> ⚠️ **Não confunda:** o arquivo `client_oauth.json` que já existe no projeto
> (`gen-lang-client-0273624757`, tipo **installed/desktop**, usado por `auth_google_tts.py`)
> **não serve** para login web e **não deve ser alterado**. Este guia cria um cliente **novo**,
> do tipo **"Aplicativo da Web"**.

---

## 1. Criar o projeto no Google Cloud

1. Acesse **https://console.cloud.google.com/projectcreate**
2. Faça login com **a sua conta Google** (a que ficará registrada como responsável pelo app).
3. Preencha:
   * **Nome do projeto:** `iso17025-simulado`
   * **Local/organização:** `Sem organização`
4. Clique **CRIAR** e aguarde a notificação de "Projeto criado".
5. Confirme, no **topo da página**, que o projeto selecionado é `iso17025-simulado`.
   *(Esse é o erro nº 1: configurar o app no projeto errado.)*

---

## 2. Google Auth Platform — Começar

1. Acesse **https://console.cloud.google.com/auth/overview** (com o projeto novo selecionado).
2. Se aparecer o botão **"Começar" (Get started)**, siga o assistente:
   * **Nome do app:** `Treinamento ISO/IEC 17025` (é o nome exibido ao participante)
   * **E-mail de suporte do usuário:** seu e-mail
   * **Público-alvo (Audience):** `Externo (External)` ← permite Gmail pessoal
   * **Informações de contato:** seu e-mail
   * **Concluir:** aceite a política e clique **Criar**
3. Se o assistente não aparecer, o projeto já está registrado — siga para o passo 3.

> A antiga "Tela de permissão OAuth" agora se chama **Google Auth Platform** e é organizada em:
> **Visão geral**, **Marca**, **Público-alvo**, **Clientes**, **Acesso a dados** e **Verificação**.

---

## 3. Público-alvo (Audience)

Menu lateral → **Público-alvo** (https://console.cloud.google.com/auth/audience)

| Configuração | Valor recomendado |
| :--- | :--- |
| **Tipo de usuário** | `Externo (External)` |
| **Status de publicação** | `Em produção` (após os primeiros testes) |

* **Em teste (Testing):** só entram as contas listadas em *Usuários de teste* (limite de 100)
  e aparece o aviso de "app não verificado". **Use esta opção no primeiro teste**, cadastrando
  apenas o seu e-mail.
* **Publicado (In production):** qualquer conta Google consegue clicar no botão. Com escopos
  básicos (`openid`, `email`, `profile`) **não é necessário processo de verificação do Google**.
  A trava real de quem pode fazer a prova é a **lista de e-mails autorizados** validada no
  servidor (Etapa 2 — Google Sheets/Apps Script).

Para publicar: **Publicar app (Publish app)** → confirmar que não usa escopos sensíveis.

---

## 4. Criar o Client ID (passo principal)

Menu lateral → **Clientes** (https://console.cloud.google.com/auth/clients) → **CREATE CLIENT**

| Campo | O que preencher |
| :--- | :--- |
| **Tipo de aplicativo** | `Aplicativo da Web` (**Web application**) |
| **Nome** | `Simulado ISO 17025 - Web` |
| **URIs de redirecionamento autorizados** | **deixar vazio** (o login é por botão/popup, não por redirect) |
| **Origens JavaScript autorizadas** | `https://caguerra-uff.github.io` e `http://localhost:8000` |

Clique **CRIAR**. Em seguida:

* **Copie apenas o ID do cliente** (algo como `1234567890-abc123def456.apps.googleusercontent.com`).
* A **chave secreta do cliente** **não é usada** neste projeto (login no navegador é "cliente
  público"). Ela é exibida **uma única vez**; se perder, pode ser rotacionada depois.
* O `client_id` é **público** por natureza — pode ficar dentro do HTML sem problema.
  O **segredo, jamais**.

---

## 5. Regras das origens autorizadas (onde 90% dos erros acontecem)

A origem é **esquema + host**, sem caminho:

| ✅ Correto | ❌ Errado | Motivo |
| :--- | :--- | :--- |
| `https://caguerra-uff.github.io` | `https://caguerra-uff.github.io/iso17025-treinamento-v2/` | não pode conter **path** |
| `https://caguerra-uff.github.io` | `caguerra-uff.github.io` | o esquema **HTTPS** é obrigatório |
| `http://localhost:8000` | `http://localhost` (se servir na porta 8000) | porta ≠ 80 precisa ser declarada |
| `https://caguerra-uff.github.io` | `https://*.github.io` | **wildcard é proibido** |
| `http://localhost:8000` | `http://192.168.0.10:8000` | IP "cru" não é aceito (só localhost) |

* O site publicado fica em `https://caguerra-uff.github.io/iso17025-treinamento-v2/`, portanto a
  origem correta é **`https://caguerra-uff.github.io`** (a origem ignora o caminho do repositório).
* Se um dia usar **domínio próprio** no GitHub Pages, **adicione** essa origem também.
* Mudanças de origem podem levar **de alguns minutos a 1 hora** para propagar.

---

## 6. Teste de validação (antes de mexer no simulado)

1. No PowerShell, dentro da pasta do projeto:

   ```powershell
   cd F:\Transcricoes_Consolidadas_V2
   python -m http.server 8000
   ```

   Abra **http://localhost:8000/** — ⚠️ **não** abra o arquivo com duplo clique: o login Google
   **não funciona** em `file://`.

2. Crie um arquivo `teste_login_google.html` na raiz com o conteúdo abaixo (substitua o
   `client_id`) e abra no navegador:

   ```html
   <!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Teste Login Google</title></head>
   <body style="font-family:sans-serif;padding:40px">
     <h2>Teste de Login Google</h2>
     <div id="btnGoogle"></div>
     <pre id="saida" style="background:#f1f5f9;padding:16px;border-radius:8px;margin-top:16px"></pre>
     <script src="https://accounts.google.com/gsi/client" async defer></script>
     <script>
       window.onload = () => {
         google.accounts.id.initialize({
           client_id: 'COLE_AQUI_SEU_CLIENT_ID.apps.googleusercontent.com',
           callback: (resp) => {
             const p = JSON.parse(atob(resp.credential.split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));
             document.getElementById('saida').textContent =
               'OK! name=' + p.name + '\nemail=' + p.email +
               '\nemail_verified=' + p.email_verified + '\nsub=' + p.sub +
               '\naud=' + p.aud + '\nexp=' + new Date(p.exp*1000).toLocaleString();
           },
           use_fedcm_for_prompt: true
         });
         google.accounts.id.renderButton(document.getElementById('btnGoogle'),
           { type: 'standard', theme: 'outline', size: 'large', text: 'signin_with' });
       };
     </script>
   </body></html>
   ```

3. Resultado esperado: aparece o botão **"Fazer login com o Google"**; após escolher a conta, o
   quadro mostra `name`, `email`, `email_verified: true`, `sub`, `aud` (= seu client ID) e `exp`.
4. Repita abrindo a página publicada no GitHub Pages para confirmar as **duas** origens.
5. Apague o arquivo de teste depois (ele não faz parte do sistema e o repositório é público).

---

## 7. Diagnosticar erros comuns

| Sintoma | Causa provável | Correção |
| :--- | :--- | :--- |
| `Error 400: origin_mismatch` | Origem não cadastrada, com path, ou `http` em vez de `https` | Corrigir no passo 4 e aguardar propagação |
| Botão não aparece (e nenhum erro) | Página aberta por `file://` | Servir por HTTP (passo 6.1) |
| "Acesso bloqueado: app não verificado" / só algumas contas entram | App em modo **Teste** | Incluir o e-mail em *Usuários de teste* ou **Publicar** |
| Botão em branco dentro de iframe | iframe cross-origin com FedCM | Adicionar `allow="identity-credentials-get"` no iframe |
| Popup em branco / nada acontece | Navegador antigo ou COOP/CSP restritivos | Usar Chrome/Edge/Firefox atualizados |

---

## 8. Ativar o login no simulado

1. Abra `scripts_processamento/construir_simulado_html.py` (é o **gerador** — nunca edite o
   `simulado.html` direto, ele é sobrescrito) e localize:

   ```javascript
   const GOOGLE_CLIENT_ID = 'COLE_AQUI_O_CLIENT_ID.apps.googleusercontent.com';
   ```

2. Substitua o valor pelo seu **Client ID** e, se quiser, ajuste:

   | Constante | Padrão | Para que serve |
   | :--- | :--- | :--- |
   | `GOOGLE_CLIENT_ID` | placeholder | Client ID OAuth criado no passo 4 |
   | `REQUIRE_GOOGLE_LOGIN` | `true` | Bloqueia o início da prova sem identificação |
   | `RESULT_ENDPOINT` | `''` (vazio) | Endpoint do Apps Script que enviará os e-mails (Etapa 2) |

3. Regenere a interface e rode a auditoria:

   ```bash
   python scripts_processamento/construir_simulado_html.py
   python test_simulado.py
   ```

4. Publique (commit/push). **Antes** de configurar o Client ID, o simulado continua funcionando
   normalmente e apenas exibe o aviso "login não configurado" — **sem bloquear ninguém**.

### O que já está implementado (Etapa 1)

* Botão oficial **"Fazer login com o Google"** na tela de configuração (Google Identity Services + FedCM).
* **Card de identificação** com foto, nome e e-mail, e botão **"Trocar de Conta"**.
* **Bloqueio do início da prova** sem identificação (quando `GOOGLE_CLIENT_ID` está configurado).
* Nome/e-mail do participante visíveis **durante a prova** e no **laudo de desempenho** (impressão).
* Identidade gravada no histórico local (últimos 30 registros) e enviada no **pacote de resultado**
  (`collectResultPayload`), pronta para a Etapa 2.
* Guarda de regressão em `test_simulado.py` (TEST 2.1), que também detecta erro de escaping do
  template f-string do gerador.

---

## 9. Próximos passos (Etapa 2) e cuidados com dados pessoais

**Etapa 2 — envio por e-mail (ainda não implementado):** publicar um **Google Apps Script**
(Web App) que recebe o pacote de resultado em `RESULT_ENDPOINT`, **valida o ID token** em
`https://oauth2.googleapis.com/tokeninfo?id_token=…`, confere se o e-mail está na **lista de
participantes autorizados** (Google Sheets), recalcula a nota e envia o relatório por e-mail ao
**participante** e ao **gestor** (mapeamento e-mail → gestor). Essa lista deve ficar na
**planilha** e **nunca** no repositório, que é **público**.

**Cuidados:**

* O que o navegador decodifica do JWT serve **apenas para exibição**. A autenticidade só é
  garantida no servidor (Etapa 2).
* O ID token expira em ~1 hora; uma prova longa pode terminar com o token vencido — por isso a
  identidade é capturada no início e o servidor revalida pelo `sub`.
* Gmail pessoal prova controle da caixa postal, **não** vínculo empregatício: o vínculo vem da
  lista de autorizados + matrícula + o gestor recebendo o resultado. Documente esse critério se
  for usar como evidência de competência (ISO/IEC 17025, item 6.2).
* Cota do Apps Script: conta Gmail comum ≈ 100 destinatários/dia (Workspace = 1.500/dia).
* O repositório é **público** e o gabarito está embutido no HTML. Se a intenção for aplicar uma
  **prova oficial** com nota válida, gere uma versão sem gabarito (correção no servidor).
