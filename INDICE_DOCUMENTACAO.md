# 📚 ÍNDICE GERAL DE DOCUMENTAÇÃO - Sistema de Monitoramento BACEN

Este índice organiza toda a documentação disponível do sistema para facilitar a navegação.

---

## 📖 Documentos Principais

### 🎯 Para Desenvolvedores e Equipe de TI

**[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Documentação Técnica Completa

Documentação completa para desenvolvedores, arquitetos e equipe de TI, incluindo:
- Arquitetura do sistema
- Detalhamento de todos os componentes e módulos
- Fluxo de dados completo
- Estrutura de código
- Dependências e bibliotecas
- Sistema de logging
- Tratamento de erros
- Segurança
- Extensibilidade e manutenção

**Quando usar:** Para entender a arquitetura, fazer modificações, extensões ou troubleshooting técnico avançado.

---

### 👤 Para Usuários Finais

**[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Manual do Usuário Completo

Manual passo a passo detalhado para usuários finais, incluindo:
- Apresentação do sistema
- Requisitos e instalação detalhada
- Configuração passo a passo (com exemplos visuais)
- Primeira execução e testes
- Uso diário
- Interpretação de resultados
- Solução de problemas comuns
- Manutenção básica
- Dúvidas frequentes

**Quando usar:** Para instalar, configurar e usar o sistema sem conhecimento técnico avançado.

---

## 📋 Documentos de Referência Rápida

### ⚡ Instalação Rápida

**[INSTRUCOES_RAPIDAS.md](./INSTRUCOES_RAPIDAS.md)** - Instruções Rápidas

Guia resumido para instalação e uso básico:
- Instalação em 3 passos
- Execução rápida
- Configuração essencial
- Checklist de instalação
- Solução rápida de problemas

**Quando usar:** Para uma referência rápida ou para usuários experientes que já conhecem o sistema.

---

### 📖 Visão Geral

**[README.md](./README.md)** - README Principal

Documentação geral do projeto com:
- Características principais
- Pré-requisitos
- Instalação e configuração básica
- Estrutura do projeto
- Módulos principais
- Funcionamento geral

**Quando usar:** Para uma visão geral inicial do projeto ou referência rápida.

---

### 📝 Histórico de Mudanças

**[ATUALIZACOES.md](./ATUALIZACOES.md)** - Atualizações e Mudanças

Documenta as mudanças e atualizações recentes do sistema:
- Mudanças implementadas
- Configurações atualizadas
- Arquivos modificados
- Como usar novas funcionalidades
- Benefícios das mudanças

**Quando usar:** Para entender o que mudou no sistema e como usar novas funcionalidades.

---

## 🔍 Guia de Uso por Situação

### 🚀 Primeira Instalação

1. Comece com: **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Seção "Instalação Passo a Passo"
2. Configure: **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Seção "Configuração Inicial"
3. Teste: **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Seção "Primeira Execução"

### ⚙️ Configuração do Email

1. Gmail: **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Seção "Configurar Gmail"
2. Outlook: **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Seção "Configurar Outlook"
3. Detalhes técnicos: **[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Seção "Integração com Serviços Externos"

### 🔧 Solução de Problemas

1. **Problemas básicos:** **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Seção "Problemas Comuns e Soluções"
2. **Problemas técnicos:** **[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Seção "Manutenção e Troubleshooting"
3. **Referência rápida:** **[INSTRUCOES_RAPIDAS.md](./INSTRUCOES_RAPIDAS.md)** - Seção "Solução de Problemas Rápidos"

### 🏗️ Desenvolvimento e Extensão

1. **Arquitetura:** **[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Seção "Arquitetura do Sistema"
2. **Componentes:** **[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Seção "Componentes e Módulos"
3. **Extensibilidade:** **[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Seção "Extensibilidade"

### 📊 Entendendo o Funcionamento

1. **Visão geral:** **[README.md](./README.md)** - Seção "Funcionamento"
2. **Fluxo detalhado:** **[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Seção "Fluxo de Dados"
3. **Para usuários:** **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Seção "O que é o Sistema"

---

## 📂 Estrutura de Documentação

```
webcrawler_bacen/
│
├── 📚 Documentação Completa
│   ├── DOCUMENTACAO_TECNICA.md      (Para desenvolvedores/TI)
│   ├── MANUAL_USUARIO.md            (Para usuários finais)
│   ├── INDICE_DOCUMENTACAO.md       (Este arquivo)
│   ├── README.md                    (Visão geral)
│   ├── INSTRUCOES_RAPIDAS.md        (Referência rápida)
│   └── ATUALIZACOES.md              (Histórico de mudanças)
│
├── 📝 Configuração
│   ├── config_example.env           (Exemplo de configuração)
│   └── config_outlook.env           (Exemplo específico Outlook)
│
└── 💻 Código (documentação inline)
    ├── main.py
    ├── webcrawler.py
    ├── sumarizador.py
    ├── enviador_email.py
    └── config.py
```

---

## 🎯 Recomendações de Leitura

### Para Usuários Finais (Sem Conhecimento Técnico)

**Ordem recomendada:**
1. **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Leia completamente
2. **[INSTRUCOES_RAPIDAS.md](./INSTRUCOES_RAPIDAS.md)** - Mantenha como referência
3. **[README.md](./README.md)** - Para entender melhor o sistema

**Não precisa ler:**
- DOCUMENTACAO_TECNICA.md (a menos que queira entender detalhes técnicos)

---

### Para Desenvolvedores e TI

**Ordem recomendada:**
1. **[README.md](./README.md)** - Visão geral rápida
2. **[DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md)** - Leitura completa
3. **[ATUALIZACOES.md](./ATUALIZACOES.md)** - Entender mudanças recentes
4. **[MANUAL_USUARIO.md](./MANUAL_USUARIO.md)** - Entender como usuários veem o sistema

---

## 🔄 Manutenção da Documentação

### Quando Atualizar

A documentação deve ser atualizada quando:
- ✅ Nova funcionalidade é adicionada
- ✅ Mudança significativa no funcionamento
- ✅ Mudança na configuração
- ✅ Novo requisito ou dependência
- ✅ Problema comum identificado (adicionar à seção de troubleshooting)

### Padrões de Documentação

- **Linguagem:** Português claro e objetivo
- **Formato:** Markdown (.md)
- **Estrutura:** Índice sempre no início
- **Exemplos:** Sempre incluir exemplos práticos
- **Código:** Sempre usar blocos de código formatados

---

## 📞 Suporte

### Recursos Disponíveis

1. **Documentação:** Este índice e os documentos listados
2. **Logs:** Arquivos .log na pasta do sistema
3. **Código:** Comentários inline no código-fonte
4. **Equipe de TI:** Para questões não cobertas pela documentação

### Como Contribuir com a Documentação

Se encontrar:
- ❌ Informação desatualizada
- ❌ Falta de clareza
- ❌ Procedimento que não funciona
- ➕ Sugestão de melhoria

Entre em contato com a equipe responsável pela documentação.

---

## 📊 Estatísticas da Documentação

- **Total de documentos:** 6
- **Páginas de documentação técnica:** ~500 linhas
- **Páginas de manual do usuário:** ~600 linhas
- **Idioma:** Português (BR)
- **Última atualização:** 2024

---

**Índice de Documentação - Sistema de Monitoramento BACEN**  
Mantenha este arquivo atualizado quando adicionar novos documentos!

---

## 🗺️ Navegação Rápida

| Documento | Público-Alvo | Tamanho | Quando Usar |
|-----------|--------------|---------|-------------|
| [DOCUMENTACAO_TECNICA.md](./DOCUMENTACAO_TECNICA.md) | Desenvolvedores/TI | Grande | Modificações, troubleshooting avançado |
| [MANUAL_USUARIO.md](./MANUAL_USUARIO.md) | Usuários Finais | Grande | Instalação, uso diário, problemas básicos |
| [README.md](./README.md) | Todos | Médio | Visão geral, referência rápida |
| [INSTRUCOES_RAPIDAS.md](./INSTRUCOES_RAPIDAS.md) | Usuários Experientes | Pequeno | Referência rápida |
| [ATUALIZACOES.md](./ATUALIZACOES.md) | Todos | Médio | Entender mudanças recentes |
| [INDICE_DOCUMENTACAO.md](./INDICE_DOCUMENTACAO.md) | Todos | Pequeno | Navegação entre documentos |

---

**Boa leitura! 📚**


