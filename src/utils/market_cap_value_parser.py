import re


class CurrencyValueAdapter:
    _currency_map = {"$": "USD", "€": "EUR", "R$": "BRL"}

    _multiplier_map = {
        "T": 1_000_000_000_000,
        "B": 1_000_000_000,
        "M": 1_000_000,
        "K": 1_000,
    }

    @classmethod
    def convert(cls, value_str: str) -> dict:
        """
        Output:
        - dict: {'currency': str, 'value': float}
        """
        pattern = r"(\$|€|R\$)?([\d\.]+)([TBMK])?"
        match = re.match(pattern, value_str)

        if not match:
            raise ValueError(f"Valor inválido: {value_str}")

        currency_symbol, number, multiplier_symbol = match.groups()

        # Define a moeda, default para USD se o símbolo não for reconhecido
        currency = cls._currency_map.get(currency_symbol, "USD")

        # Converte o número para float
        number_value = float(number)

        # Define o multiplicador, default para 1 se não houver símbolo
        multiplier = cls._multiplier_map.get(multiplier_symbol, 1)

        # Calcula o valor final
        final_value = number_value * multiplier

        return {"currency": currency, "value": final_value}
