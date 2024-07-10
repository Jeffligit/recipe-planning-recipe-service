from src.user.crud import create_user, get_user, get_users, get_user_by_email, get_user_by_username, edit_username
from src.models import User
from src.schemas import UserCreate

class TestUser:
    
    def test_create_user(self, session):
        test_user = UserCreate(
            email="test@email.com",
            username="test",
            password="test_password"
        )
        create_user(session, test_user)
        expected = session.query(User).filter(User.username == "test").first()
        assert expected.username == "test"

    def test_get_user(self, session):
        expected = get_user(session, 1)
        assert expected.username == "test"

    def test_get_user_by_email(self, session):
        expected = get_user_by_email(session, "test@email.com")
        assert expected.email == "test@email.com"

    def test_get_user_by_username(self, session):
        expected = get_user_by_username(session, "test")
        assert expected.username == "test"

    def test_get_users(self, session):
        test2_user = UserCreate(
            email="test2@email.com",
            username="test2",
            password="test2_password"
        )
        create_user(session, test2_user)
        expected_users = get_users(session)
        assert len(expected_users) == 2

    def test_edit_username(self, session):
        user = get_user_by_username(session, "test")
        edit_username(session, user.id, "changed name")

        expected = session.query(User).filter(User.email == "test@email.com").first()
        print(f"{expected.id}, {expected.username}, {expected.email}")
        assert expected.username == "changed name"