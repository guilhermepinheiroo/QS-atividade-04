# Atividade 4: Testes Automatizados do LocalEats

**Unidade Curricular:** Qualidade de Software
**Projeto:** LocalEats (https://local-eats-unisenac.vercel.app/)
**Modalidade:** Individual
**Integrante:** Guilherme

## 1. Identificação dos testes e responsáveis

| ID   | Integrante | Tipo       | Comportamento verificado                                   | Arquivo e função |
|------|------------|------------|------------------------------------------------------------|------------------|
| TU01 | Guilherme  | Unitário   | Pedido de R$ 150,00 recebe R$ 15,00 de desconto            | `tests/test_regras_localeats.py::test_pedido_de_150_recebe_desconto_de_15` |
| TU02 | Guilherme  | Unitário   | Pedido abaixo de R$ 100,00 não recebe desconto             | `tests/test_regras_localeats.py::test_pedido_abaixo_de_100_nao_recebe_desconto` |
| TU03 | Guilherme  | Unitário   | Casos de borda (0; 99,99; 100; 129,90 com arredondamento)  | `tests/test_regras_localeats.py::test_desconto_nos_limites_da_regra` |
| TU04 | Guilherme  | Unitário   | Valor negativo gera `ValueError`                           | `tests/test_regras_localeats.py::test_valor_negativo_gera_value_error` |
| TF01 | Guilherme  | Funcional  | Aba "Criar Conta" exibe o formulário de cadastro           | `tests/test_localeats.py::test_aba_criar_conta_exibe_formulario_de_cadastro` |
| TF02 | Guilherme  | Funcional  | Sem login, clicar no logo mantém o usuário na tela de login | `tests/test_localeats.py::test_logo_sem_login_mantem_usuario_na_tela_de_login` |

## 2. TDD de Guilherme

**Regra escolhida:** Regra 2, calcular o desconto do pedido: `calcular_desconto(valor_pedido)`.

**Primeiro teste escrito:** `test_pedido_de_150_recebe_desconto_de_15`, que espera `calcular_desconto(150) == 15`.

**Por que o teste falhou inicialmente:** o módulo `src/regras_localeats.py` e a função `calcular_desconto` ainda não existiam. O pytest interrompeu a coleta com `ModuleNotFoundError: No module named 'src.regras_localeats'`.

**Implementação mínima realizada:**

```python
def calcular_desconto(valor_pedido):
    return valor_pedido * 0.1
```

Com ela, o primeiro teste passou.

**Segundo teste escrito:** `test_pedido_abaixo_de_100_nao_recebe_desconto`, que espera `calcular_desconto(80) == 0`. Ele falhou com `assert 8.0 == 0`, porque a implementação mínima aplicava 10% a qualquer valor. Em seguida incluí a condição `if valor_pedido < 100: return 0`.

**Melhoria ou refatoração realizada:**

- Os números da regra viraram constantes com nome: `VALOR_MINIMO_PARA_DESCONTO = 100` e `PERCENTUAL_DESCONTO = 0.10`.
- A validação de valor negativo foi incluída com `ValueError`, coberta pelo TU04.
- O resultado passou a ser arredondado em centavos com `round(..., 2)`. Sem isso, `129.90 * 0.1` resulta em `12.990000000000002` em ponto flutuante. O TU03 cobre esse caso.

## 3. Explicação individual (Guilherme): TF01

Escolhi o fluxo de alternância entre "Entrar" e "Criar Conta" por ser estável e por não depender de dados cadastrados nem de credenciais. Assim, o teste pode ser executado quantas vezes for necessário sem criar contas no sistema.

Usei locators por papel e por texto (`get_by_role`, `get_by_placeholder`) sempre que o texto identificava o elemento sem ambiguidade. A tela tem dois botões chamados "Entrar" (a aba e o botão de envio do formulário) e dois campos "E-mail". Por isso, os formulários foram localizados pelos IDs `#loginForm` e `#registerForm`, e as buscas por botões e campos foram feitas dentro de cada formulário. Isso evita o erro de *strict mode* do Playwright, que ocorre quando um locator encontra mais de um elemento.

Na primeira execução, o teste falhou ao localizar o campo com `get_by_label("Nome Completo")`. O LocalEats exibe o texto "Nome Completo", mas o `<label>` não está associado ao campo (falta o atributo `for`). Por isso, o nome acessível do campo vem do placeholder "Seu nome", como mostrou o *aria snapshot* do erro. Troquei o locator por `get_by_placeholder("Seu nome")`.

Antes do clique, o teste verifica que o login está visível. Depois do clique, verifica cinco resultados observáveis: aba ativa, formulário de cadastro visível, campo "Nome Completo", botão "Registrar" e login oculto. Com isso, o teste comprova a troca de formulário, e não apenas a existência dos elementos na página.

## 4. Uso de inteligência artificial

**Ferramenta utilizada:** Claude (Anthropic).

**Como a ferramenta foi utilizada:** apoio na exploração da tela de login do LocalEats, na estruturação do projeto, na escrita dos testes seguindo o ciclo TDD e na redação deste relatório.

**Uma sugestão que precisou ser alterada ou rejeitada:**

- A implementação mínima `valor_pedido * 0.1` passava no teste com R$ 150,00, mas retornava `12.990000000000002` para R$ 129,90. A versão final arredonda o desconto em centavos com `round(..., 2)`, e o caso foi incluído no TU03.
- A IA sugeriu `get_by_label("Nome Completo")` com base numa cópia local da página. Essa sugestão falhou na execução contra o site real, porque o `<label>` não tem `for`, e foi trocada por `get_by_placeholder("Seu nome")`.

**Como o código sugerido foi verificado:** executando `python -m pytest -v` contra o LocalEats real (relatório em `relatorio-pytest.txt`), conferindo cada falha esperada no ciclo TDD e comparando os locators com os elementos reais da página de login do LocalEats.
