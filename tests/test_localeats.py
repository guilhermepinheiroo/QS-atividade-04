# Responsável: Guilherme Pinheiro
# Testes funcionais do LocalEats com Playwright (pytest-playwright).
#
# A fixture `page` é fornecida pelo plugin pytest-playwright.
# Nenhum teste usa time.sleep: as assertions do `expect` aguardam
# automaticamente até o elemento atingir o estado esperado.
import os
import re

from playwright.sync_api import Page, expect

URL_LOCALEATS = os.getenv("LOCALEATS_URL", "https://local-eats-unisenac.vercel.app/")


# TF01 - alternar da aba "Entrar" para a aba "Criar Conta"
def test_aba_criar_conta_exibe_formulario_de_cadastro(page: Page):
    page.goto(URL_LOCALEATS)

    formulario_login = page.locator("#loginForm")
    formulario_cadastro = page.locator("#registerForm")

    # Situação inicial: o formulário de login é o que aparece
    expect(formulario_login).to_be_visible()

    # Interação: clicar na aba "Criar Conta"
    aba_criar_conta = page.get_by_role("button", name="Criar Conta")
    aba_criar_conta.click()

    # Resultados observáveis
    expect(aba_criar_conta).to_have_class(re.compile(r"\bactive\b"))
    expect(formulario_cadastro).to_be_visible()
    # O <label> "Nome Completo" não está associado ao campo no LocalEats,
    # então o campo é localizado pelo placeholder real ("Seu nome").
    expect(formulario_cadastro.get_by_placeholder("Seu nome")).to_be_visible()
    expect(formulario_cadastro.get_by_role("button", name="Registrar")).to_be_visible()
    expect(formulario_login).to_be_hidden()


# TF02 - sem login, clicar no logo não dá acesso à área interna
def test_logo_sem_login_mantem_usuario_na_tela_de_login(page: Page):
    page.goto(URL_LOCALEATS)

    # A página inicial redireciona visitantes não autenticados para o login
    expect(page).to_have_url(re.compile(r"/static/login\.html$"))

    # Interação: clicar no logo "LocalEats", que aponta para index.html
    page.get_by_role("link", name="Local").click()

    # Resultados observáveis: continua na tela de login
    expect(page).to_have_url(re.compile(r"/static/login\.html$"))
    expect(page).to_have_title("Entrar | Local Eats")
    expect(page.locator("#loginForm").get_by_role("button", name="Entrar")).to_be_visible()
