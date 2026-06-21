from src.database.session import get_db


def test_get_db_lifecycle_yields_and_closes(mocker, mock_db):
    mocker.patch(
        "src.database.session.get_session_local",
        return_value=mocker.MagicMock(return_value=mock_db),
    )

    db_generator = get_db()
    yielded_session = next(db_generator)
    assert yielded_session == mock_db

    mock_db.close.assert_not_called()

    try:
        next(db_generator)
    except StopIteration:
        pass

    mock_db.close.assert_called_once()
