# Responsável: Guilherme Pinheiro
# Regra 2: calcular o desconto do pedido
import pytest

from src.regras_localeats import calcular_desconto


# TU01 - comportamento esperado: pedido com direito a desconto
def test_pedido_de_150_recebe_desconto_de_15():
    resultado = calcular_desconto(150)
    assert resultado == 15


# TU02 - situação alternativa: pedido abaixo do valor mínimo
def test_pedido_abaixo_de_100_nao_recebe_desconto():
    resultado = calcular_desconto(80)
    assert resultado == 0


# TU03 - casos de borda em torno de R$ 100,00 e arredondamento em centavos
@pytest.mark.parametrize(
    "valor_pedido, desconto_esperado",
    [
        (0, 0),
        (99.99, 0),
        (100, 10),
        (129.90, 12.99),
    ],
)
def test_desconto_nos_limites_da_regra(valor_pedido, desconto_esperado):
    assert calcular_desconto(valor_pedido) == desconto_esperado


# TU04 - comportamento inválido: valor negativo gera exceção
def test_valor_negativo_gera_value_error():
    with pytest.raises(ValueError, match="não pode ser negativo"):
        calcular_desconto(-10)
