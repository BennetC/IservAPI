import uuid


def generate_draft_id(account_id: str) -> str:
    """
    Generates a DraftId by creating a unique message ID based on the account's domain.

    Args:
        account_id: The email address of the account (e.g., 'user@example.com').

    Returns:
        An instance of the DraftId class containing the original account_id
        and the newly generated message_id.

    Raises:
        ValueError: If the account_id is not a valid email address format.
    """
    try:
        # Split the email address to get the part after the '@'
        host_part = account_id.split('@')[1]
    except IndexError:
        raise ValueError("Invalid account_id format. An email address is expected.")

    # Generate a random UUID (Universally Unique Identifier). [1]
    generated_uuid = uuid.uuid4()

    # Construct the messageId string in the format <uuid@hostpart>. [2, 3]
    message_id = f"<{generated_uuid}@{host_part}>"

    # Return a new DraftId object
    return message_id