from fastapi.routing import APIRoute
from config import VALID_AMINO_ACIDS, MAX_SEQUENCE_LENGTH

# https://github.com/zeno-ml/zeno/blob/main/zeno/server.py#L52
def custom_generate_unique_id(route: APIRoute):
    return route.name

# https://github.com/zeno-ml/zeno-hub/blob/9d2f8b5841d99aeba9ec405b0bc6a5b1272b276f/backend/zeno_backend/classes/base.py#L20
def to_camel(string: str) -> str:
    """Converter for variables from snake_case to camelCase.

    Args:
        string (str): the variable to convert to camelCase.

    Returns:
        str: camelCase representation of the variable.
    """
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def validate_protein_sequence(sequence: str) -> tuple[bool, str | None]:
    """Validate a protein sequence.

    Args:
        sequence (str): the protein sequence to validate.

    Returns:
        tuple[bool, str | None]: (is_valid, error_message).
            If valid, error_message is None. Otherwise, contains the error.
    """
    if not sequence:
        return False, "Sequence cannot be empty"

    if len(sequence) > MAX_SEQUENCE_LENGTH:
        return False, f"Sequence too long (max {MAX_SEQUENCE_LENGTH} amino acids)"

    # check for invalid characters (allowing * for mask tokens)
    invalid_chars = set(sequence.upper()) - VALID_AMINO_ACIDS - {"*"}
    if invalid_chars:
        return False, f"Invalid amino acids: {', '.join(sorted(invalid_chars))}"

    return True, None
