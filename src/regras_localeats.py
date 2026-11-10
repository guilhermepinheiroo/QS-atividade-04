"""Regras de negócio do LocalEats.

Responsável: Guilherme Pinheiro
Regra 2: calcular o desconto do pedido.
"""

VALOR_MINIMO_PARA_DESCONTO = 100
PERCENTUAL_DESCONTO = 0.10


def calcular_desconto(valor_pedido):
    """Retorna o valor do desconto (não o valor final do pedido).

    - pedidos abaixo de R$ 100,00 não recebem desconto;
    - pedidos de R$ 100,00 ou mais recebem 10% de desconto;
    - valores negativos geram ValueError.
    """
    if valor_pedido < 0:
        raise ValueError("O valor do pedido não pode ser negativo.")

    if valor_pedido < VALOR_MINIMO_PARA_DESCONTO:
        return 0

    return round(valor_pedido * PERCENTUAL_DESCONTO, 2)
